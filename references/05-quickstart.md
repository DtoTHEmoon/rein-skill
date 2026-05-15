# 一键配置模板

根据Rein诊断结果，按层级选择对应模板。复制修改，5分钟内可用。

---

## 模板A：从零起步（L1-L2）

适合：刚开始用AI开发、内部小工具、低频迭代

```markdown
# CLAUDE.md

## 项目背景
[一句话说明这个项目是做什么的]
[主要技术栈]
[关键业务规则或限制]

## 绝对禁止
- 禁止修改 [列出核心文件，如配置文件、价格逻辑]
- 禁止删除已有测试
- [你最近一次被AI坑到的那件事，写成禁止]

## 必须做
- 改完代码先在本地测试，再说做完了
- [你希望AI每次都做但经常忘的事]

## 项目结构（简版）
[关键文件路径和作用，3-5行]
```

---

## 模板B：加验证层（L1-L4）

适合：对外交付、高频迭代、出错成本中等以上

在模板A基础上，增加：

```markdown
# CLAUDE.md 新增部分

## 完成标准（重要）
任何代码改动完成后，必须运行 `bash verify.sh` 通过才算完成。
verify.sh 不通过，不允许说"已完成"，不允许切换到下一个任务。
```

```bash
#!/bin/bash
# verify.sh - 根据你的项目修改

echo "=== 开始验证 ==="

# 1. 服务能启动（修改为你的端口和接口）
if curl -sf http://localhost:8000/health > /dev/null; then
    echo "✅ 服务启动正常"
else
    echo "❌ 服务启动失败"
    exit 1
fi

# 2. 核心功能能用（修改为你的核心接口）
if curl -sf http://localhost:8000/核心接口 > /dev/null; then
    echo "✅ 核心功能正常"
else
    echo "❌ 核心功能异常"
    exit 1
fi

# 3. 测试通过（如果有测试）
# if python -m pytest tests/ -q; then
#     echo "✅ 测试通过"
# else
#     echo "❌ 测试失败"
#     exit 1
# fi

echo "=== ✅ 验证通过 ==="
```

---

## 模板C：加部署Skill（L3）

适合：有固定部署流程、部署经常出问题

```markdown
# .claude/skills/deploy/SKILL.md
---
name: deploy
description: 标准部署流程。每次部署时使用，包含打包、传输、验证三步。
---

# 部署流程

## 步骤一：打包
```bash
cd [项目路径]
tar --exclude='.git' --exclude='.next' --exclude='node_modules' \
    -czf ~/Desktop/项目名-latest.tar.gz .
```

## 步骤二：验证包内容
```bash
tar -tzf ~/Desktop/项目名-latest.tar.gz | grep [关键文件]
```

## 步骤三：部署到服务器
[你的传输方式和服务器上的部署命令]

## 步骤四：验证部署结果
```bash
bash verify.sh
```

## 部署铁律
- 后端有修复时：先更新后端，再部署前端
- 改了环境变量：必须重新build，不能只restart
- 部署后必须跑verify.sh，不能靠感觉判断
```

---

## 模板D：完整配置（L1-L5，多人团队）

适合：多人协作、对外交付、复杂链路

在模板B基础上，增加：

```markdown
# CLAUDE.md 新增部分

## 角色分工（Multi-Agent）
这个项目使用两层Agent分工：
- 需求分析Agent：负责把模糊需求整理成结构化任务
- 实现Agent：只负责按照结构化任务实现，不修改需求

需求分析Agent完成后，必须输出：
- 目标是什么
- 不做什么
- 验收标准

实现Agent不允许修改需求定义，有疑问必须返回给需求分析层。
```

```markdown
# dev-map.md

## 项目地图
[关键模块和对应文件]
[已有实现，不要重复造]
[代码惯例]
```
