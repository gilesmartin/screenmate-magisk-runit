# ScreenMate startup services

I built this because I wanted my ScreenMate hotspot and a few other background tasks to start automatically when the unit powers up.

This repo shares the MagiskSU and runit setup behind that arrangement: how it hooks into startup, starts the root service, and keeps it supervised. It does not include a hotspot manager or give an unrooted ScreenMate root access.

## What would I use it for?

It is a starting point for ScreenMate owners who want to run their own background services at boot rather than start them manually each time. MagiskSU lets Android apps request root access; runit starts and watches long-running services.

I have used the setup on my own ScreenMate through several successful reboots. Other firmware has not been verified.

## What do I need?

An already-rooted ScreenMate One, root ADB access, and enough Android/Linux experience to review and adapt shell scripts. The tested unit runs Android 14 on ARM64.

This is an experimental reference, not a one-click installer. The `install.sh` and `uninstall.sh` tools only print plans; they do not change the device. The reference scripts are disabled by default. Read the security and recovery notes before changing anything that runs as root at boot.

## Where to start

- [Setup requirements and installation plan](docs/install.md)
- [How the startup hook works](docs/boot-integration.md)
- [Configuration](docs/configuration.md)
- [Security warnings](docs/security.md) and [recovery](docs/recovery.md)
- [Technical details and developer notes](docs/architecture.md)
- [Tests and reboot evidence](docs/testing.md)

## License

The custom scripts and documentation use the [MIT license](LICENSE). Magisk, BusyBox and runit have their own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md).
