# Configuration and app authorization

The reference layout uses `/data/local/screenmate-services`. Its supervisor supplies PATH and LD_LIBRARY_PATH; changing the base requires coordinated review of every reference, service entry and recovery path. [Example local configuration](../examples/local-config.json) is descriptive, not automatically loaded by the extracted scripts.

- `run/disable-boot`: suppresses the added boot launch, not a currently running supervisor.
- `services/magisk/down`: persistent runit automatic-start control. A live service must be stopped separately under approved maintenance; creating the marker alone is not shutdown.
- `run/magisk-failure.lock`: blocks startup; recovery intentionally retains it. Do not clear it automatically.
- `run/magisk-test.armed`: explicit recovery-test gate, not evidence that an independent recovery process is running.

Use the installed, trusted upstream Magisk Manager to decide each app's root authorization. No package/UID grants are supplied here. UID numbers can be reassigned after uninstall/reinstall and differ across Android users; a durable numeric grant can accidentally authorize a different app. Recheck actual package identity, user and signer whenever granting root.

Direct Magisk SQLite policy edits are advanced, schema/version-specific, destructive authorization changes. They require a separate user-approved grant scope, secure backup and inspection of the actual schema; no portable SQL grant command is provided. Never publish the database or copy another owner's authorization table. App root grants are separate from the existing root ADB bootstrap.

SSH and terminal-app setup are separate projects, not prerequisites for this service.
