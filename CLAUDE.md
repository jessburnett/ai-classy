# CLAUDE.md: Brainchild Project Guide

## 1. Project Context
- **Name:** brainchild
- **Tech Stack:** Python 3.12+, Node.js 25.8 (Termux), SQLite/Supabase.
- **Goal:** Policy-driven agentic orchestration using local MCP servers.

## 2. Rules of Engagement (Governance)
- **Identity:** Always verify identity via `verify_identity()` before major PRs.
- **Privacy:** ALL external data must be scrubbed using `shield.py`.
- **Compliance:** Adhere to instructions in @SB24-205_NOTICE.md and @AGENT_POLICY.md.

## 3. Technical Conventions
- **Commands:** Prefer `just <command>` for common tasks (see `justfile`).
- **Tests:** Always run `reproduce.sh` in a clean environment before proposing fixes.
- **Paths:** Use `$PREFIX/tmp` for sockets; never hardcode `/tmp`.
- **Imports:** Ensure top-level imports in Python to maintain modularity.

## 4. Useful Commands
- Audit Project: `python shield.py`
- Run Agent Tests: `./reproduce.sh`
- Clean Temp Files: `rm -rf $PREFIX/tmp/*`

---
*Reference: @AIBOM.json for model architecture.*

