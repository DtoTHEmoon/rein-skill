# 推荐运行方式：
# 手动：python3 scripts/fetch-updates.py
# 每周自动（Mac/Linux crontab）：
# 0 9 * * 1 cd ~/projects/rein-skill && python3 scripts/fetch-updates.py
# 意思是：每周一早上9点自动运行
# 设置方法：终端输入 crontab -e，把上面那行加进去
#
# 依赖安装：pip3 install requests feedparser beautifulsoup4

import requests
import feedparser
import json
import os
from datetime import date
from bs4 import BeautifulSoup

# ── 路径配置 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
LAST_FETCH_PATH = os.path.join(SCRIPT_DIR, "last-fetch.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "weekly-review.md")

# ── 来源配置 ──────────────────────────────────────────────
GITHUB_RAW_SOURCES = [
    {
        "name": "awesome-harness-engineering (ai-boost)",
        "url": "https://raw.githubusercontent.com/ai-boost/awesome-harness-engineering/main/README.md",
    },
    {
        "name": "awesome-harness-engineering (walkinglabs)",
        "url": "https://raw.githubusercontent.com/walkinglabs/awesome-harness-engineering/main/README.md",
    },
    {
        "name": "learn-harness-engineering (walkinglabs)",
        "url": "https://raw.githubusercontent.com/walkinglabs/learn-harness-engineering/main/README.md",
    },
]

RSS_SOURCES = [
    {
        "name": "Martin Fowler",
        "url": "https://martinfowler.com/feed.atom",
    },
    {
        "name": "HumanLayer Blog",
        "url": "https://www.humanlayer.dev/blog/rss.xml",
    },
]

GITHUB_TOPICS_URL = (
    "https://api.github.com/search/repositories"
    "?q=topic:harness-engineering&sort=updated&per_page=10"
)

PAGE_SOURCES = [
    {
        "name": "Software Mansion Agentic Engineering",
        "url": "https://agentic-engineering.swmansion.com",
    },
    {
        "name": "Hands-on Architects Blog",
        "url": "https://handsonarchitects.com/blog",
    },
]

HEADERS = {"User-Agent": "rein-skill-fetcher/1.0"}
TIMEOUT = 15


# ── 工具函数 ──────────────────────────────────────────────
def load_last_fetch():
    if os.path.exists(LAST_FETCH_PATH):
        with open(LAST_FETCH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"seen": []}


def save_last_fetch(data):
    with open(LAST_FETCH_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_new(item_id, seen_ids):
    return item_id not in seen_ids


# ── 抓取函数 ──────────────────────────────────────────────
def fetch_github_raw(source):
    """抓取 GitHub raw 文件，提取链接行（以 http 开头的行）。"""
    results = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        for line in resp.text.splitlines():
            line = line.strip()
            if line.startswith("http"):
                results.append({
                    "id": line,
                    "title": line,
                    "link": line,
                    "source": source["name"],
                })
            elif "](http" in line:
                # Markdown 格式：[title](url)
                try:
                    title = line.split("](")[0].lstrip("- [").strip()
                    url = line.split("](")[1].rstrip(")").strip()
                    results.append({
                        "id": url,
                        "title": title or url,
                        "link": url,
                        "source": source["name"],
                    })
                except IndexError:
                    pass
    except Exception as e:
        print(f"  [跳过] {source['name']}: {e}")
    return results


def fetch_rss(source):
    """抓取 RSS/Atom Feed，提取文章条目。"""
    results = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            link = getattr(entry, "link", "")
            title = getattr(entry, "title", link)
            if link:
                results.append({
                    "id": link,
                    "title": title,
                    "link": link,
                    "source": source["name"],
                })
    except Exception as e:
        print(f"  [跳过] {source['name']}: {e}")
    return results


def fetch_github_topics():
    """通过 GitHub API 抓取最新 harness-engineering 话题仓库。"""
    results = []
    try:
        resp = requests.get(
            GITHUB_TOPICS_URL,
            headers={**HEADERS, "Accept": "application/vnd.github.v3+json"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        for repo in data.get("items", []):
            url = repo.get("html_url", "")
            name = repo.get("full_name", url)
            desc = repo.get("description", "")
            title = f"{name} — {desc}" if desc else name
            if url:
                results.append({
                    "id": url,
                    "title": title,
                    "link": url,
                    "source": "GitHub Topics: harness-engineering",
                })
    except Exception as e:
        print(f"  [跳过] GitHub Topics API: {e}")
    return results


def fetch_page_titles(source):
    """抓取页面，提取 <title> 和所有 <h1> 及 <a> 标签。"""
    results = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # 页面标题
        title_tag = soup.find("title")
        page_title = title_tag.get_text(strip=True) if title_tag else source["url"]
        results.append({
            "id": source["url"],
            "title": page_title,
            "link": source["url"],
            "source": source["name"],
        })

        # 页面内所有外链文章
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if href.startswith("http") and text:
                results.append({
                    "id": href,
                    "title": text,
                    "link": href,
                    "source": source["name"],
                })
    except Exception as e:
        print(f"  [跳过] {source['name']}: {e}")
    return results


# ── 主流程 ────────────────────────────────────────────────
def main():
    today = date.today().strftime("%Y-%m-%d")
    print(f"=== Rein 知识库更新爬取 — {today} ===\n")

    last = load_last_fetch()
    seen_ids = set(last.get("seen", []))
    all_items = []

    print("[1/4] 抓取 GitHub raw 文件...")
    for source in GITHUB_RAW_SOURCES:
        items = fetch_github_raw(source)
        print(f"  {source['name']}: {len(items)} 条")
        all_items.extend(items)

    print("[2/4] 抓取 RSS Feed...")
    for source in RSS_SOURCES:
        items = fetch_rss(source)
        print(f"  {source['name']}: {len(items)} 条")
        all_items.extend(items)

    print("[3/4] 抓取 GitHub Topics API...")
    items = fetch_github_topics()
    print(f"  GitHub Topics: {len(items)} 条")
    all_items.extend(items)

    print("[4/4] 抓取页面标题...")
    for source in PAGE_SOURCES:
        items = fetch_page_titles(source)
        print(f"  {source['name']}: {len(items)} 条")
        all_items.extend(items)

    # 过滤新增
    new_items = [item for item in all_items if is_new(item["id"], seen_ids)]

    # 去重（同一 id 只保留第一次出现）
    seen_this_run = set()
    deduped = []
    for item in new_items:
        if item["id"] not in seen_this_run:
            seen_this_run.add(item["id"])
            deduped.append(item)

    print(f"\n共发现 {len(deduped)} 条新内容（总抓取 {len(all_items)} 条）\n")

    # 写输出文件
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(f"## 待审阅内容 - {today}\n\n")
        f.write("### 新增资料\n")
        if deduped:
            for item in deduped:
                f.write(f"- [{item['source']}] {item['title']} — {item['link']}\n")
        else:
            f.write("- （本次无新增内容）\n")
        f.write(f"\n### 本次新增数量：{len(deduped)} 条\n")
        f.write("\n### 说明\n")
        f.write(
            "请人工审阅，有价值的手动整合进 references/06-knowledge-base.md\n"
        )

    print(f"输出已写入：{OUTPUT_PATH}")

    # 更新 last-fetch.json
    all_seen = list(seen_ids | seen_this_run)
    save_last_fetch({"date": today, "seen": all_seen})
    print(f"状态已保存：{LAST_FETCH_PATH}")


if __name__ == "__main__":
    main()
