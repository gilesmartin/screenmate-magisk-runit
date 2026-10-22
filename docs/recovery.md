# Recovery and uninstall

All stop, unmount, live-policy reload, marker writes, service changes and deletion below are **future approved maintenance actions**, not actions performed by the plan tools. `sh scripts/uninstall.sh` prints the sequence without executing it.

1. Preserve independent already-authorized root ADB before relying on MagiskSU. When disconnected, do not assume any remote recovery is possible; physical access may be required.
2. Disable only the added launch using `run/disable-boot`, and hold the Magisk service down through its reviewed runit controls. Neither operation is included in the observational doctor.
3. Request graceful runit service stop, and verify the wrapper completes exact original policy restoration, daemon termination and removal of only its overlay/runtime mounts. Examine the relevant mount namespace; absence in one shell is not proof of absence everywhere.
4. The extracted recovery script is inert unless `run/magisk-test.armed` exists. Do not arm/run it casually. It latches failure/down state, attempts bounded runit and daemon stops, then ownership-specific cleanup and policy restoration. Its mount/policy calls are not all bounded. It does not prove independent automatic recovery after crashes.
5. If ownership is ambiguous, a mount remains, policy restoration fails or enforcing mode differs, stop and retain backups/failure lock. Never delete an active overlay backing directory, force-unmount blindly, kill unknown daemons or load another build's policy. The current cleanup predicates need further hardening before automated reuse.
6. Only after verified cleanup restore this integration's backed-up narrow hook, without changing unrelated AP/network startup, then remove only manifest-owned files. Do not uninstall Manager, erase app data or revoke grants as an implicit uninstall step.

The private export tool excludes policy blobs deliberately. An owner needs an independently safeguarded pristine target policy for real recovery. Script backups alone are not a complete system rollback. Unexpected runsvdir death can bypass service EXIT cleanup and leave runtime state; no crash test was performed here.
