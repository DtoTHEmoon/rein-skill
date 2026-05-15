# Rein

> 让AI在你的项目里跑得快、跑得准、跑得稳。

Rein是一个随项目全程的Harness Engineering顾问。它不是框架，不是工具——它是一个Skill，安装后在你的AI编程助手里持续感知项目的Harness状态，在刚好需要的时候给出刚好够用的建议。

**核心理念：大道至简。** 不乱加，够用就好。加法之前先问够不够，到一定程度了就考虑减。

---

## 安装

```bash
# Claude Code
git clone https://github.com/DtoTHEmoon/rein.git ~/.claude/skills/rein

# OpenClaw
git clone https://github.com/DtoTHEmoon/rein.git ~/.openclaw/skills/rein

# Codex CLI
git clone https://github.com/DtoTHEmoon/rein.git ~/.codex/skills/rein
```

重启Agent后生效。

---

## 它做什么

**不需要你主动问。** Rein在对话中自动感知以下信号：

- AI反复犯同类错误 → 诊断缺哪一层Rule或Script
- 改完东西不知道有没有出问题 → 建议加验证脚本
- 每次都要重新交代背景 → 建议完善CLAUDE.md或dev-map
- 项目从内部工具变成对外交付 → 评估Harness是否需要升级
- 配置越来越多但项目没变快 → 提示该做减法了
- 问API成本为什么这么高 → 给出成本估算和节省建议

**它不做的事：** 不评业务需求，不给架构意见，不在你正常推进项目时插嘴。没有明显缺口，Rein保持沉默。

---

## Harness六层模型

Rein基于六层模型诊断你的项目：

| 层 | 名称 | 解决什么 |
|----|------|---------|
| L1 | 规格 SPEC | AI知道做什么 |
| L2 | 规则 Rule | AI知道不能做什么 |
| L3 | 技能 Skill | 高频动作标准化 |
| L4 | 验证 Scripts | 客观判断"做完了" |
| L5 | 分工 Multi-Agent | 复杂任务角色分工 |
| L6 | 知识库 dev-map | AI了解整个项目 |

单人内部项目做到L4已经很扎实。不需要为了"完整"而上L5-L6。

---

## 兼容平台

Claude Code · OpenClaw · Codex CLI · Gemini CLI · Cursor · Hermes Agent · 及所有支持SKILL.md标准的Agent

---

## 案例

**方舟AI项目（脱敏）**
单人非技术背景，内部体检报价系统，从Dify迁移到FastAPI，3个月从0到生产。

Rein在这个项目里起到的作用：
- 发现部署流程缺乏验证层（L4），每次部署后要手动curl检查 → 加了verify.sh
- 识别到CLAUDE.md开始膨胀 → 把部署铁律下沉到独立Skill
- 评估Multi-Agent需求 → 判断当前规模不需要，节省了过度设计的时间

> 更多案例见 `references/04-cases.md`

---

## 知识库来源

Rein的诊断逻辑整合自：
- Anthropic Harness Engineering最佳实践
- Martin Fowler "Relocating Rigor"
- HumanLayer "Skill Issue"系列
- 万字Harness Engineering工程化落地指南
- 方舟AI项目真实踩坑记录

持续更新，每周同步市面最新Harness实践。

---

## 贡献

欢迎提Issue或PR，尤其是：
- 真实项目的Harness配置案例（可脱敏）
- 发现的新触发模式
- 成本估算数据校正

---

*No-bullshit Harness Engineering for real projects.*
