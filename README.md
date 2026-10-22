# Screenmate MagiskSU + runit

**Experimental reference integration and plan-only packaging, not a one-click root tool.**

A documented technique for ordinary apps to use MagiskSU on an already-rooted Screenmate One: Android 14, ARM64, enforcing SELinux, immutable `/system` and `/product`, with an existing authorized root ADB shell. No boot-image patch or bootloader unlock is part of this technique. This does not create initial root or promise universal device compatibility.

The owner reports the installation has worked since Saturday through **several successful reboots**. Current read-only inspection corroborated a running Magisk 30.7 service, enforcing SELinux, and the SU symlink's shared device/inode identity. No reboot, app grant, service restart or mount/policy change was performed for this publication.

## Quick start (off device)

Requires Python 3.9+ and a POSIX shell (including macOS). No third-party binaries or APKs are included.

```sh
python3 -m unittest discover -s tests -v
sh scripts/install.sh       # prints a review plan; NEVER installs
sh scripts/uninstall.sh     # prints a review plan; NEVER uninstalls
python3 scripts/adb-doctor.py --serial YOUR_AUTHORIZED_DEVICE
```

The doctor is optional and read-only. It does not reconnect, start services, request root grants or prove an application can obtain root. An offline device is a transport blocker, not evidence of broken Magisk.

## What is captured

- [Boot chain and exact narrow launch hook](docs/boot-integration.md), including the standard Android boot-broadcast entry and existing authenticated loopback ADB bootstrap.
- Five [sanitized current-live references](reference/source-manifest.json), disabled by default. A device-specific kernel-policy pin is replaced by a mandatory local placeholder.
- [Architecture](docs/architecture.md), [installation plan](docs/install.md), [configuration](docs/configuration.md), [recovery](docs/recovery.md), [security](docs/security.md), and [test evidence/limits](docs/testing.md).
- An explicit-allowlist [private export tool](scripts/private-export.py), with no policy/database/APK/key/log collection.

## Essential warnings

The existing boot caller's parent directory was world-writable. **Do not reproduce that trust boundary.** Root scripts and their complete parent chain must be controlled by root; review a safer independent boot entry before deployment. This publication does not change the original installation.

The live readiness gate has no total deadline; cleanup can block; cleanup failure does not automatically latch a failure lock; the recovery guard is inert unless explicitly armed. Unexpected supervisor-crash recovery and cross-firmware behavior are not established. See [security](docs/security.md).

`/product/bin/su` must remain a **symlink to `/debug_ramdisk/magisk`**, not a copied binary or hardlink. Native Magisk client authentication requires the runtime identity; a visible path alone is insufficient.

No vehicle application, telemetry service, SSH or Termux application installation is required by the Magisk service itself. The legacy boot adapter is documented, not made a mandatory redistributable dependency. No private boot-helper APK, package identifier, ADB key or root authorization is published.

## License and attribution

Custom integration scripts, documentation and tools: [MIT](LICENSE). Magisk, runit, BusyBox, Android and Termux remain their authors' work under their own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md) and [pinned provenance](dependencies.json). No certification, security guarantee, or third-party relicensing right is implied.
