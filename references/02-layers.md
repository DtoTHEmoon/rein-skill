# 六层模型详细配置模板

每层包含：定义、起步命令、最小可用版本、进阶版本、减法临界点。

---

## L1 规格 SPEC

**解决什么：** AI知道这次要做什么、边界在哪、做完怎么验收。

**缺失症状：** 每次理解不同；做完了但和预期对不上；AI自己发挥填补了没说清楚的部分。

**起步：三个问题，写进CLAUDE.md或任务开头**
```
这次要做什么？（目标）
不做什么？（边界）
做完怎么验证？（验收标准）
```

**好的SPEC的特征：**
- 没有"建议"、"可以"、"推荐"等模糊词
- 有明确的验收条件，不是"做好"而是"能通过XX测试"
- 边界说清楚了，AI不需要猜

---

## L2 规则 Rule

**解决什么：** AI知道什么绝对不能做，减少反复犯的同类错误。

**缺失症状：** 说过的规矩下次又忘；AI自己改了不该改的地方；反复出现同一类错误。

**起步：从最近3次崩溃出发**
```markdown
# CLAUDE.md 里的Rule示例

## 绝对禁止
- 禁止修改 .env 文件
- 禁止删除任何已有测试
- 改动部署相关文件前必须先问我

## 必须做
- 每次改完代码必须跑 verify.sh
- 改了价格相关逻辑必须更新单元测试
```

**Rule的原则：**
- 针对反复出现的错误，不是泛泛的"要认真"
- Rule解决"绝对不能"，不解决"怎么做"（那是Skill的事）
- 每条Rule背后要有真实踩坑的原因

**减法临界点：** Rule超过15条且AI仍不遵守 → 说明该升级成Script了，加Rule没用。

### 安全红线（必须写进CLAUDE.md）
```
## 绝对禁止
- 禁止API Key、密码硬编码进代码
- 禁止.env文件提交到Git
- 禁止日志打印用户原始输入
- 修改部署配置前确认端口暴露范围
```

---

## L3 技能 Skill

**解决什么：** 把高频的、步骤固定的动作标准化，不让AI临场发挥。

**缺失症状：** 每次部署步骤不一样；验证方式每次不同；AI自己拼命令总有细节出错。

**什么值得做成Skill：**
- 步骤固定（不需要临场判断）
- 每次都要做（高频）
- 做错了很麻烦（高代价）
- 不希望AI自己发挥

**常见Skill候选：**
- 部署流程（打包→传输→验证）
- 代码格式检查
- 特定格式文件生成（Excel报价单、周报模板）
- 数据库操作规范

**Skill文件结构：**
```
项目/.claude/skills/deploy/
├── SKILL.md    # 步骤说明
└── scripts/
    └── deploy.sh  # 具体命令
```

**减法临界点：** Skill超过5个且有功能重叠 → 合并，删掉冗余。

---

## L4 验证脚本 Scripts ⭐

> 这是整个Harness里最被低估、实际价值最高的一层。

> ⚠️ L4是地基，不是终点。
> L5、L6建在L4上面，不是替代L4。
> 没有L4的L5/L6，是在沙地上盖楼。
> 不管你用了几层，验证脚本必须存在。

**解决什么：** 把"AI说做完了"变成"脚本判定通过了"。建立客观的完成标准。

**缺失症状：** 不知道改完有没有出问题；AI说没问题但实际有bug；"这是历史遗留问题"成为借口。

### 最小可用版本（今天就能做）

```bash
#!/bin/bash
# verify.sh

# 1. 服务能启动
curl -f http://localhost:8001/health || { echo "❌ 服务启动失败"; exit 1; }

# 2. 核心接口能响应
curl -f http://localhost:8001/核心接口 || { echo "❌ 核心接口失败"; exit 1; }

echo "✅ 验证通过"
```

### 标准版：基线对比

```bash
#!/bin/bash
# verify-with-baseline.sh
# 改动前跑一次，改动后再跑一次，对比差异

REPORT_FILE="/tmp/verify-$(date +%Y%m%d-%H%M%S).log"

run_checks() {
    curl -s http://localhost:8001/health
    # 加入更多检查...
}

run_checks > "$REPORT_FILE"
echo "验证报告已保存到 $REPORT_FILE"
```

**使用方式：**
```bash
# 改动前
bash verify.sh > baseline.log

# 做改动...

# 改动后
bash verify.sh > current.log

# 对比
diff baseline.log current.log
```

### 完整版：总验证脚本

覆盖四类检查，统一入口，任何一项不过就拒绝"完成"：

```bash
#!/bin/bash
# verify-full.sh

PASS=0
FAIL=0

check() {
    local name=$1
    local cmd=$2
    if eval "$cmd" > /dev/null 2>&1; then
        echo "✅ $name"
        ((PASS++))
    else
        echo "❌ $name"
        ((FAIL++))
    fi
}

echo "=== 静态规范检查 ==="
check "无硬编码密钥" "! grep -r 'sk-' --include='*.py' ."
check "无中文注释在关键文件" "! grep -rn '[^\x00-\x7F]' main.py"

echo "=== 服务验证 ==="
check "服务启动" "curl -sf http://localhost:8001/health"
check "核心接口" "curl -sf http://localhost:8001/核心接口"

echo "=== 功能验证 ==="
check "单元测试" "python -m pytest tests/ -q"

echo "=== 安全基线 ==="
check "无硬编码密钥" "! grep -rn 'sk-\|password\s*=\s*['\''\"]\
  --include='*.py' --include='*.ts' \
  --exclude-dir='.git' --exclude-dir='node_modules' ."
check ".env未入版本库" "! git ls-files | grep -E '^\.env$'"
check "Dockerfile有USER指令" \
  "! find . -name 'Dockerfile' | xargs grep -L 'USER' 2>/dev/null | grep ."

echo "=== 结果 ==="
echo "通过: $PASS / 失败: $FAIL"
[ $FAIL -eq 0 ] || exit 1
```

**Rule配合使用：**
```markdown
# CLAUDE.md
## 绝对禁止
- 任何代码改动完成后，必须运行 bash verify.sh 通过才算完成
- verify.sh 不通过，不允许说"已完成"
```

**减法临界点：** 检查项超过20条且有明显从未触发过的项 → 删掉，保持精简。

---

## L5 分工 Multi-Agent

**解决什么：** 把长链路任务拆成角色分工，防止单Agent自说自话。

**什么时候真的需要：**
- 任务链路超过 需求→方案→开发→验证 四个阶段
- 单Agent频繁在长任务里失稳、前后矛盾
- 有明确的"不同角色不能互相评审自己的工作"需求

**什么时候不需要（大多数情况）：**
- 单人项目，任务链路不超过3步
- 加了Multi-Agent反而比单Agent慢
- 团队还没有稳定的工作流定义

**最小分工：先拆两层**
```
需求分析Agent → 实现Agent
（不要一上来就搭7个Agent）
```

**减法临界点：** Multi-Agent跑起来比单Agent更慢或更乱 → 退回单Agent，重新评估。

---

## L6 知识库 dev-map

**解决什么：** 让AI在长期项目里不重复造轮子，知道整个项目的结构和惯例。

**什么时候需要：**
- 项目持续迭代超过2个月
- AI开始重复造轮子，不知道已有实现
- 旧设计被新设计莫名其妙冲掉

**最小可用版本：**
```markdown
# dev-map.md

## 项目结构
- 报价逻辑在 ark-engine/rules.py
- 前端API代理在 ark-platform/app/api/
- 数据库操作在 lib/db.ts

## 已有实现，不要重复造
- Excel生成：用 openpyxl，不要用其他库
- 价格计算：统一走 pricer.py，不要在别处算

## 惯例
- 新增接口必须在 /health 接口里更新版本号
- 部署前必须跑 verify.sh
```

**dev-map vs CLAUDE.md：**
- CLAUDE.md：规则和禁止（AI必须遵守的）
- dev-map：项目地图（AI应该了解的）

**减法临界点：** dev-map和实际代码结构脱节超过1个月 → 说明没人维护，考虑删掉或大幅精简。
