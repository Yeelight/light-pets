# Validation Record

Date: 2026-07-04

## Local Build

```bash
make smoke PYTHON="/Users/yeelight/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
```

Result:

```text
built 82 pets across 3 collections
validation passed: 82 pets, 3 collections
```

## Public Clone Smoke

The public smoke test copied the repository without ignored `resources/`, `.playwright-cli`, `output`, `.git`, or `.DS_Store`, then rebuilt and validated from committed public files only.

Result:

```text
built 82 pets across 3 collections
validation passed: 82 pets, 3 collections
```

## HTTP Static Asset Check

The static demo was served through `python -m http.server`. All relative `href` and `src` links in `demo/index.html` were checked with HTTP `HEAD`.

Result:

```text
checked: 1151
missing: 0
contains_resources: false
```

## Browser Automation Note

Playwright CLI and MCP both attempted to launch local Chrome for screenshot validation, but the operating system terminated the Chrome process with `SIGKILL`. Static file validation, full catalog validation, public-clone smoke, and HTTP link validation all passed.
