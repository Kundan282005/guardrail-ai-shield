# TODO - Guardrail Email Assistant Review/Fixes

- [ ] Update `main.py` backend to enforce fraud protocol lock (skip reply generation when fraud).
- [ ] Update `main.py` to request strict JSON from LLM and parse/validate safely.
- [ ] Harden `main.py` request payload handling (handle missing/invalid JSON).
- [ ] Fix XSS risk in `templates/index.html` by removing `innerHTML` usage for LLM outputs.
- [ ] Ensure returned API schema remains compatible with both React and template UIs.
- [ ] Start backend server and verify website behavior for safe vs fraud emails.

