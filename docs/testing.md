# Evidence and testing matrix

## Owner history, not newly repeated tests

The owner states the installation has been in use since Saturday, with **several successful reboots**. This is **owner-reported** successful startup persistence, not an untested feature. Exact calendar date/count and cold-power-cycle coverage were not inferred. The owner also reports prior successful service start/stop policy restoration, unprivileged-app root under the Magisk context, durable grants across daemon restart, and a fail-closed diagnostic test. Those tests were not repeated during publication, and the old app-specific identity monitor is not included.

## Read-only inspection in this assignment

Observed Android 14 ARM64; root ADB in the su domain; enforcing SELinux; Magisk 30.7/SU 30.7; running runit Magisk service, daemon, ADB and AP processes; shared product/runtime/overlay mounts; SU symlink resolving to the same device and inode as the runtime executable; completion properties set; absence of failure/disable/armed markers at inspection. Five current scripts were captured privately and byte-hash checked against the device. Installed boot receiver and detached launch code were inspected off device. Official Magisk APK digest and contained executable hashes match local prerequisites and live hashes.

No reboot was performed during this assignment. No root grant, service restart, mount operation, policy load, package installation, settings edit, lock clear or destructive test was performed on the device. Inspection of package metadata/installed code is not app-data collection.

## Reproducible off-device tests

`python3 -m unittest discover -s tests -v` exercises deterministic install/uninstall plans, rejected apply mode, a fake-ADB no-execution marker, default-inert references, POSIX shell parsing, policy-pin removal, observational doctor checks, mocked private export with fixed allowlist and private modes, duplicate/export-destination refusal, documentation links and privacy/binary exclusions. These are packaging tests, **not** proof of kernel/mount recovery or native Magisk correctness.

CI repeats the same tests, whitespace checks and ShellCheck when available. Exact locally executed results are in the release packaging report; do not infer a passing CI run merely from a workflow file.

## Still not established

Unexpected supervisor or daemon crash cleanup, hard-kill behavior, bounded recovery under blocked unmount/policy operations, other firmware/hardware and a portable unattended installer. Native runit/library binary-to-source correspondence remains incomplete. Permission grant acceptance was not retested here. No universal modules/Zygisk support, boot-image installation, or global SELinux bypass claim is made.

## Sacrificial-device acceptance, requires separate authorization

Record build and namespace baseline, obtain independent recovery, capture pristine target policy, validate start/stop restoration, TERM/HUP and startup-failure cleanup, stalled package-manager deadlines and fail-lock respawn behavior, real app-grant isolation, pre-existing app namespaces, ownership collisions, power-cycle startup and supervisor crash recovery. Change one boundary at a time, with tested rollback and bounded observation. Never execute these fault injections on the owner's production car device for documentation.
