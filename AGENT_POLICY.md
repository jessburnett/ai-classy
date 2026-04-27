# AGENT_POLICY.md: Orchestration Governance

## 1. Scope of Authority
[span_6](start_span)[span_7](start_span)This policy governs all Automated Decision-Making Technology (ADMT) and agentic entities (e.g., Claude, Gemini) operating within the `~/development/ai-classified` and `~/development/brainchild` directories[span_6](end_span)[span_7](end_span).

## 2. Mandatory Constraints (The "Classy" Rules)
- **[span_8](start_span)[span_9](start_span)Privacy First:** Every agentic output intended for external transmission MUST be piped through `shield.py` to ensure local Termux paths and PII are redacted[span_8](end_span)[span_9](end_span).
- **[span_10](start_span)Instruction Literalism:** Agents shall not deviate from the core logic defined in `CLAUDE.md` without an explicit Human-in-the-Loop override[span_10](end_span).
- **No Native Binaries:** Due to current platform limitations (Android/Bionic), agents are prohibited from attempting to install or execute glibc-dependent native binaries.

## 3. Colorado SB 24-205 Compliance
- **[span_11](start_span)[span_12](start_span)Meaningful Human Review:** An agent may propose code changes, but it cannot `git commit` or `npm publish` without a designated human reviewer approving the output[span_11](end_span)[span_12](end_span).
- **[span_13](start_span)[span_14](start_span)Adverse Outcome Protocol:** If an agentic action results in a system failure or data corruption, the agent must generate an "Adverse Outcome Report" within the `.agent/logs/` directory[span_13](end_span)[span_14](end_span).

## 4. Resource Management
- **Environment:** Agents must utilize the `CLAUDE_CODE_TMPDIR` defined in the environment for all socket and temporary file operations.
- **Carbon Efficiency:** Agents should favor local scripts (`shield.py`, `ripgrep`) over high-token API calls whenever possible to maintain compute sustainability.

---
*Status: Active | Version: 2026.Kilo | Enforcement: Strictly Local*
