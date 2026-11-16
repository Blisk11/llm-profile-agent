# Drift report — 2026-11-16

Repository: `llm-profile-agent`. Source HEAD: `8f031efe057357bc89c26d1254405d0f568cd9da`.

Scope: README claims compared with application, model wrapper and packaging. No API calls, secrets or private profile data read; deterministic temperature is not treated as a proof of factual correctness.

Inspected source: `src/agent.py`, `src/llm_wrapper.py`, `src/profile_loader.py`, `web/app.py`, `web/components.py`, `pyproject.toml`.

## README.md

- [P2] The README promises profile-driven answers with no hallucination and deterministic profile enforcement. `src/llm_wrapper.py:61–111` only checks banned input substrings, sets a system prompt/temperature, and returns model output without factual validation. Replace the guarantee with the actual best-effort prompting boundary, or add the claimed output enforcement.
- [P3] The security claim that no sensitive data is stored in session state is too broad: `web/app.py:46–47,138–143` retains arbitrary submitted questions and answers in `st.session_state.history`, and `web/components.py:237–246` stores generated CV text. Document the actual session retention and user-input boundary.
- [P3] Quick Start still uses `github.com/username/llm-profile-agent.git`, a placeholder that cannot identify this repository.

## Resolution of cross-repository findings (2026-11-16)

The findings above describe the audited baseline. Replaced unsupported no-hallucination/determinism and session-retention guarantees with the actual prompting/storage boundaries, and corrected the clone URL.

Verification route: README-to-source comparison and repository URL/path checks; no model calls.
The original coverage limits remain in force.
