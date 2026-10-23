# Architecture and lifecycle

```text
trusted boot entry -> detached supervisor + lifetime flock
                     -> runsvdir -> runsv -> readiness gate
                                           -> foreground Magisk wrapper
/data/local/screenmate-services/           /debug_ramdisk (tmpfs)
  bin/{busybox,runsvdir,runsv,sv}            magisk + .magisk state
  lib/librunit.so                         /product/bin (overlay)
  magisk/bin/{magisk,magiskpolicy,...}       su -> /debug_ramdisk/magisk
  services/magisk/run
  run/ and logs/                          /dev/screenmate-magisk-su/{upper,work}
```

The supervisor exports the local bin PATH and LD_LIBRARY_PATH for librunit.so. BusyBox flock holds a single lock across runsvdir's lifetime. The runit entry execs the readiness gate; the gate checks both completion properties, zygote and the package manager's Android package record. The query is timeout-bounded; the overall gate currently is not.

The wrapper checks root, enforcing mode, pristine local policy hash, original policy backup, absence of runtime mounts/daemon/SU, and shared product mount propagation. Only after preflight does its EXIT cleanup trap become active. It mounts a tmpfs on `/debug_ramdisk`, stages Magisk and `.magisk` directories, loads narrow Magisk rules with `magiskpolicy --magisk --live`, requests a `magisk_file` label, and starts the daemon.

It stages the matching Manager stub, invokes `--post-fs-data`, checks that the stub was consumed, invokes `--boot-complete`, and verifies the public upstream Manager is installed and daemon exists. It creates the upper/work directories, a symlink to the runtime binary, clones product directory attributes, and overlays `/product/bin`. A copy/hardlink is not the same mount/inode arrangement and must not replace the symlink. Shared propagation is required for pre-existing application mount namespaces.

The foreground wrapper checks daemon presence, overlay ownership and enforcing mode every five seconds. It does not create root grants. TERM/INT/HUP lead to EXIT cleanup: owned overlay unmount, daemon stop, runtime unmount, original target policy reload, and checksum/mount checks. Backing files are removed only when no owned runtime/overlay remains. There are important ownership, boundedness and failure-lock gaps: see [security](security.md).

The live binary label was observed as `system_file`, despite the wrapper requesting `magisk_file` earlier. This is a documented discrepancy; no relabeling or attribution to a particular stage was performed.

## Maintainer reference

These implementation and release notes previously appeared in the README. Commands assume the repository root. Start with the [project overview](../README.md) if you are deciding whether to use the project.

**Experimental reference integration and plan-only packaging, not a one-click root tool.**

A documented technique for ordinary apps to use MagiskSU on an already-rooted Screenmate One: Android 14, ARM64, enforcing SELinux, immutable `/system` and `/product`, with an existing authorized root ADB shell. No boot-image patch or bootloader unlock is part of this technique. This does not create initial root or promise universal device compatibility.

The owner reports the installation has worked since Saturday through **several successful reboots**. Current read-only inspection corroborated a running Magisk 30.7 service, enforcing SELinux, and the SU symlink's shared device/inode identity. No reboot, app grant, service restart or mount/policy change was performed for this publication.

### Quick start (off device)

Requires Python 3.9+ and a POSIX shell (including macOS). No third-party binaries or APKs are included.

```sh
python3 -m unittest discover -s tests -v
sh scripts/install.sh       # prints a review plan; NEVER installs
sh scripts/uninstall.sh     # prints a review plan; NEVER uninstalls
python3 scripts/adb-doctor.py --serial YOUR_AUTHORIZED_DEVICE
```

The doctor is optional and read-only. It does not reconnect, start services, request root grants or prove an application can obtain root. An offline device is a transport blocker, not evidence of broken Magisk.

### What is captured

- [Boot chain and exact narrow launch hook](boot-integration.md), including the standard Android boot-broadcast entry and existing authenticated loopback ADB bootstrap.
- Five [sanitized current-live references](../reference/source-manifest.json), disabled by default. A device-specific kernel-policy pin is replaced by a mandatory local placeholder.
- [Architecture](architecture.md), [installation plan](install.md), [configuration](configuration.md), [recovery](recovery.md), [security](security.md), and [test evidence/limits](testing.md).
- An explicit-allowlist [private export tool](../scripts/private-export.py), with no policy/database/APK/key/log collection.

### Essential warnings

The existing boot caller's parent directory was world-writable. **Do not reproduce that trust boundary.** Root scripts and their complete parent chain must be controlled by root; review a safer independent boot entry before deployment. This publication does not change the original installation.

The live readiness gate has no total deadline; cleanup can block; cleanup failure does not automatically latch a failure lock; the recovery guard is inert unless explicitly armed. Unexpected supervisor-crash recovery and cross-firmware behavior are not established. See [security](security.md).

`/product/bin/su` must remain a **symlink to `/debug_ramdisk/magisk`**, not a copied binary or hardlink. Native Magisk client authentication requires the runtime identity; a visible path alone is insufficient.

No vehicle application, telemetry service, SSH or Termux application installation is required by the Magisk service itself. The legacy boot adapter is documented, not made a mandatory redistributable dependency. No private boot-helper APK, package identifier, ADB key or root authorization is published.

### License and attribution

Custom integration scripts, documentation and tools: [MIT](../LICENSE). Magisk, runit, BusyBox, Android and Termux remain their authors' work under their own licenses; see [third-party notices](../THIRD_PARTY_NOTICES.md) and [pinned provenance](../dependencies.json). No certification, security guarantee, or third-party relicensing right is implied.
