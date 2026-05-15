# Rein

> The silent Harness Engineering advisor that knows when to shut up.

Rein is an always-on Harness Engineering skill for AI coding agents. It lives in your project, watches your conversations, and speaks up *only* when it detects a real gap — not when you're just writing code.

**Core philosophy: Less is more.** Don't add harness layers you don't need. Know when to subtract.

---

## Install


```bash
# Claude Code
git clone https://github.com/DtoTHEmoon/rein-skill.git ~/.claude/skills/rein

# OpenClaw
git clone https://github.com/DtoTHEmoon/rein-skill.git ~/.openclaw/skills/rein

# Codex CLI
git clone https://github.com/DtoTHEmoon/rein-skill.git ~/.codex/skills/rein
```


Restart your agent. Rein activates automatically — no commands needed.

---

## What it does

Rein watches for patterns, not keywords. It detects:

- **Repeated failures** — same bug fixed twice → missing Rule or regression test
- **Context loss** — re-explaining background every session → incomplete CLAUDE.md or dev-map
- **Scale shifts** — internal tool going external → time to harden your harness
- **Cost spikes** — API bill higher than expected → identifies token waste sources
- **Over-engineering** — more config, slower shipping → tells you what to delete

**What it never does:** comment on business decisions, review code quality, or speak up when everything's fine. Silence is a feature.

---

## The Six-Layer Model

Rein diagnoses your project against six harness layers:

| Layer | Name | Solves |
|-------|------|--------|
| L1 | **SPEC** | AI knows what to build |
| L2 | **Rules** | AI knows what never to do |
| L3 | **Skills** | Repetitive workflows standardized |
| L4 | **Scripts** | Objective "done" definition |
| L5 | **Multi-Agent** | Role separation for complex tasks |
| L6 | **dev-map** | AI understands the full project |

Solo projects are solid at L4. Don't add L5-L6 just because they exist.

---

## Works with

Claude Code · OpenClaw · Codex CLI · Gemini CLI · Cursor · Hermes Agent · any agent supporting the SKILL.md standard

---

## Quantitative Evaluation

10 scenarios, 3-5 assertions each. Real comparison: Rein enabled vs disabled (separate sessions).

| | With Rein | Without Rein |
|--|-----------|--------------|
| **Overall** | **95%** (39/41) | **52%** (21/41) |
| Root cause diagnosis | 92% | 25% |
| Silence test (should not trigger) | 100% | 100% |
| Subtraction advice | 100% | 62% |
| Multi-signal prioritization | 75% | 0% |
| Cost estimation | 100% | 25% |

Key findings:
- Silence works perfectly: Rein never speaks up during normal development or pure bug fixes
- Biggest gap: Multi-Agent diagnosis (75% vs 0%)
- Both groups score 100% on silence tests — Rein doesn't add noise when it shouldn't

Methodology: 10 prompts run in separate Claude Code sessions (Rein enabled/disabled).
T06/T07/T08 re-tested after SKILL.md fixes. T03 has a known boundary case
(CLAUDE.md vs dev-map distinction). T07 uses a two-turn diagnostic protocol;
single-turn assertions undercount its actual performance.
Full results: [evals/test-results-v2-real.md](evals/test-results-v2-real.md)

---

## Real case

**Internal AI quoting system** — solo developer, non-technical background, 3 months from zero to production.

What Rein caught:
- No verification after deployment → added `verify.sh`, zero-guess deploys
- CLAUDE.md ballooning past 150 lines → moved deploy rules to a dedicated Skill
- Multi-Agent temptation → diagnosed as unnecessary, saved weeks of over-engineering

Full case: [references/04-cases.md](references/04-cases.md)

---

## When Rein speaks up

Rein activates on patterns — not on you asking for it:

- AI repeating the same mistake twice
- You re-explaining context that should already be documented
- Project scope expanding (new users, external delivery, new team members)
- Harness complexity growing faster than shipping speed
- API costs climbing without obvious reason

Rein stays silent during normal development. A good session with Rein is often one where it said nothing.

---

## When Rein tells you to *remove* things

Rein monitors for over-engineering signals:

| Signal | Action |
|--------|--------|
| CLAUDE.md > 150 lines, AI still ignores rules | Move rules to Scripts |
| Rules keep growing, problems don't shrink | Upgrade to verification scripts |
| 5+ Skills with overlapping functions | Merge and delete |
| Multi-Agent slower than single agent | Roll back |
| Harness maintenance > feature shipping | Start subtracting |

> If your harness is slowing you down, it's time to cut.

---

## Knowledge base

Rein's diagnostic logic is distilled from:

- Anthropic Harness Engineering research
- Martin Fowler — "Relocating Rigor"
- HumanLayer — "Skill Issue" series
- Addy Osmani — "Agent Harness Engineering"
- Real production failures from a 3-month solo build

Updated weekly with the latest harness engineering practices.

---

## Contribute

PRs welcome, especially:
- Real project Harness configs (anonymized is fine)
- New pattern triggers you've discovered
- Cost estimation corrections

[中文版](README.zh.md)

---

*No-bullshit Harness Engineering for real projects.*
