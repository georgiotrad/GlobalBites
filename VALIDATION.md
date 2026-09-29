# Package Validation Record

Validation performed while assembling this ZIP:

- Python source compilation: PASS (`compileall`).
- Inline browser JavaScript syntax: PASS (`node --check`).
- ML evaluation suite: PASS — 8/8 cases using the final `ml_system.py`.
- Supplied scikit-learn model load: PASS in an environment with scikit-learn 1.8.0.
- Core SQLite reservation logic: PASS for create, duplicate-slot rejection, diner/staff authorization boundary, confirm, complete, and persisted listing.
- `railway.json` syntax: PASS.
- Original restaurant images retained: 52 image files.
- Legacy localStorage user/reservation authority references: none in the final app.
- Committed SQLite database files: none.

## Environment limitation during package assembly

The sandbox could not download Flask/Werkzeug because outbound package installation was unavailable. Therefore the complete Flask HTTP test suite could not be executed in this assembly environment. The suite is included and is part of the required release gate.

Before freezing a submission SHA, install `requirements.txt` and run:

```bash
python scripts/release_gate.py
```

Do not mark the release `GO` unless that command passes on the real candidate environment and the live health/smoke/UI checks also pass.
