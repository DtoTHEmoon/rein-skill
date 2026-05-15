# Harness Engineering 知识库

> 本知识库整合了以下作者的公开文章中的核心洞察，所有内容均已注明原始来源。
> Rein六层模型主要来源：万字Harness Engineering工程化落地文章（作者：白家杰，腾讯云开发者）
> 如有异议请提Issue。

市面上Harness Engineering核心知识的精华整理。持续更新。
最后更新：2026-05-15

---

## 核心概念速查

### 什么是Harness Engineering
AI模型本身不是Agent，Agent = 模型 + Harness。Harness是围绕模型的完整基础设施：它能访问的工具、约束它行为的规则、帮它自我纠正的反馈闭环、让人类在关键节点介入的机制。

> "If you're not the model, you're the harness." — Addy Osmani

### Harness vs Prompt Engineering vs Context Engineering
- Prompt Engineering：优化单次输入
- Context Engineering：优化给模型的所有信息（更大范围）
- Harness Engineering：设计整个系统——约束、工具、反馈、分工（最大范围）

三者是包含关系，Harness Engineering包含另外两者。

### 为什么Harness比模型更重要
LangChain的案例：同一个模型，改变Harness配置，Terminal Bench 2.0得分从52.8%提升到66.5%（Top 30→Top 5）。模型没变，Harness变了，结果差异巨大。

---

## 关键原则

### 原则一：Relocating Rigor（严格性迁移）
来源：Martin Fowler / Birgitta Böckeler

工程严格性从没有消失，只是在迁移：
- 设计文档时代 → 自动化测试时代 → Harness时代
- 人工代码审查 → 自动化检查脚本
- 经验和直觉 → Rule和Skill

好的Harness不是限制AI，而是把人类经验转化为可执行的约束。

### 原则二：Bias Towards Shipping（偏向出货）
来源：HumanLayer

不要为了优化Harness而优化Harness。只在以下情况投入：
- AI出了问题，花时间确保它不再以同样方式出问题
- 不要预防性地去找问题然后解决

每次Agent失败，才是加Rule/Script的时机。

### 原则三：Build Rippable Harnesses（可拆除的Harness）
来源：NxCode

模型在快速进化。今天需要复杂配置才能做到的事，6个月后可能模型直接就能做好。

设计Harness时保留"可以删掉"的能力：
- 哪些Rule是因为模型不够好才加的？标记出来
- 每次主要模型升级后，评估哪些配置可以删掉

### 原则四：Computational vs Inferential Controls
来源：Birgitta Böckeler

两类控制机制，都需要：
- **计算性控制**：确定性的，如linter、测试、格式检查。快、准、可靠
- **推理性控制**：用AI评判AI，如LLM-as-judge。灵活但有不确定性

优先用计算性控制，推理性控制作为补充。

---

## 常见误区

### 误区一：Multi-Agent = 更好的结果
Multi-Agent增加复杂度，不一定增加质量。每增加一个Agent：
- 上下文消耗乘以倍数
- 协调成本增加
- 失败点增加

**什么时候才用Multi-Agent：** 单Agent在长链路任务里明显失稳，而且你已经把L1-L4都做好了。

### 误区二：Rule越多越安全
超过15条Rule，AI开始选择性遵守。超过20条，基本上是自我安慰。

**更好的做法：** 把重要的Rule变成Script——不是告诉AI"应该"，而是让脚本判定"通不通过"。

### 误区三：MCP越多越强大
每个MCP server都往系统提示里注入工具列表。工具越多，上下文越重，AI选择越混乱。

**更好的做法：** 只接真正需要的MCP。已有CLI工具的（如GitHub、Docker），直接用CLI，AI的训练数据里有这些工具。

### 误区四：CLAUDE.md越详细越好
CLAUDE.md超过150行，AI开始跳过不重要的部分。

**更好的做法：** CLAUDE.md只留核心红线。详细的操作步骤下沉到Skill。

---

## 参考资料

### 必读
- Martin Fowler / Birgitta Böckeler, "Harness Engineering for Coding Agent Users" (2026.04)
- HumanLayer, "Skill Issue: Harness Engineering for Coding Agents" (2026.03)
- Addy Osmani, "Agent Harness Engineering" (2026.04)
- Mitchell Hashimoto, "My AI Adoption Journey" (2026.02) — Harness Engineering这个词的起源

### 进阶
- awesome-harness-engineering (GitHub: ai-boost/awesome-harness-engineering) — 持续更新的资料清单
- Red Hat Developer, "Harness Engineering: Structured Workflows for AI-Assisted Development" (2026.04)
- Software Mansion Agentic Engineering Guide

### 工具
- AutoHarness (GitHub: aiming-lab/AutoHarness) — 自动化Harness验证框架
- everything-claude-code (GitHub: affaan-m/everything-claude-code) — 综合Harness优化系统

---

*本知识库每周更新。发现有价值的新资料，欢迎提PR。*
