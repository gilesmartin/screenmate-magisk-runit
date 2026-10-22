# Hooking the standard Screenmate/Android boot process

## Observed current chain

```text
Standard Android LOCKED_BOOT_COMPLETED / BOOT_COMPLETED broadcast
  -> existing installed, direct-boot-aware boot receiver
  -> device-protected foreground service
  -> authenticated ADB connection to loopback, port 5555
  -> verifies root and checks whether the existing AP watchdog is alive
  -> if absent, launches it with setsid and redirected standard streams
  -> narrow added block at top of /data/local/virtualap/watchdog.sh
  -> BusyBox setsid -> start-supervisor.sh
  -> BusyBox flock holds one runsvdir instance for its full lifetime
  -> runit services/magisk/run
  -> Magisk Android-readiness gate
  -> Magisk service
```

The receiver's registered boot actions and its installed bytecode were inspected read-only. Off-device analysis showed device-protected storage, a foreground service, an authenticated loopback ADB client, detached watchdog launch, and a follow-up liveness check after disconnect. No app-private key or app data was read. The private helper's application identity and APK are deliberately not distributed.

This is a standard Android broadcast entry into a previously installed local bootstrap, **not proof that an OEM init.rc directly executes the watchdog**. Searching the firmware init directories did not find a direct watchdog launch. A separate OEM property-action utility was observed but is not claimed as this launch path. The owner reports several successful reboots since installation on Saturday; no new reboot was required.

## Exact added hook

The original narrow block is in [the inactive reference](../reference/boot-hook.sh.in). Excluding the publication guard, it checks `run/disable-boot`, checks `start-supervisor.sh` is executable, then invokes BusyBox `setsid` with stdin from `/dev/null` and output redirected to `logs/boot.log`, in the background. It returns control promptly to the existing watchdog. The rest of that unrelated watchdog is not included.

`disable-boot` affects future launch attempts; it does not stop a live supervisor or remove root grants. `services/magisk/down` controls runit's automatic service start; neither marker is a complete uninstall.

## Reproducing without the private adapter

A compatible owner must provide a separately reviewed trusted root boot trigger. An owner-built direct-boot-aware receiver can use Android's normal boot broadcasts and an explicitly provisioned authenticated loopback ADB client, or an existing trustworthy firmware boot hook can launch the supervisor. Provisioning keys, installing such a helper, modifying init, or changing TCP ADB is outside this plan-only release. Never embed a shared key or rely on MagiskSU to bootstrap the Magisk daemon it is supposed to start.

The Magisk/runit layer is independent of the AP. Moving its launch into a dedicated root-owned entry avoids depending on an AP manager's lifecycle, but requires separate installation approval and boot testing. Merely changing `watchdog.sh` permissions is insufficient while its parent directory remains writable by others. No live directory was hardened, replaced or restarted during publication.

The existing bootstrap monitors the AP watchdog, not every runsvdir exit. Do not infer that it restarts a failed supervisor while the watchdog remains alive.
