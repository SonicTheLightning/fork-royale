# Bot Security

Bot code is untrusted code. Parsing JSON and applying an execution timeout does not make arbitrary Python code safe.

## Current prototype limitations

The included `SubprocessBot` uses `subprocess.run` with `shell=False`, a timeout, captured output and JSON validation. It does not provide operating-system isolation, a filesystem sandbox, network restrictions, CPU quotas or memory limits.

Use it only with code you trust, on a development machine without sensitive files or credentials exposed to the bot.

## Requirements before public submissions

A production tournament runner must define and test:

- Per-bot process or container isolation.
- A minimal filesystem view with no host secrets.
- Network denial by default.
- CPU, memory, process-count and wall-clock limits.
- Maximum input and output sizes.
- Strict JSON schema validation.
- Cleanup after crashes, timeouts and forced termination.
- Logs that do not leak secrets from the host.

A pull request review is not a substitute for a sandbox.
