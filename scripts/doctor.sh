#!/system/bin/sh
# SPDX-License-Identifier: MIT
# Read-only current-namespace status. No policies, package lists, logs or IDs dumped.
flag() { if "$@" >/dev/null 2>&1; then printf yes; else printf no; fi; }
printf 'root_shell=%s\n' "$(flag test "$(id -u)" = 0)"
printf 'selinux_enforcing=%s\n' "$(flag test "$(getenforce 2>/dev/null)" = Enforcing)"
printf 'android_ready=%s\n' "$(flag test "$(getprop sys.boot_completed 2>/dev/null)" = 1)"
printf 'zygote_ready=%s\n' "$(flag test "$(getprop init.svc.zygote 2>/dev/null)" = running)"
printf 'magisk_daemon_present=%s\n' "$(flag pidof magiskd)"
printf 'supervisor_present=%s\n' "$(flag pidof runsvdir)"
printf 'su_symlink_expected=%s\n' "$(flag test "$(readlink /product/bin/su 2>/dev/null)" = /debug_ramdisk/magisk)"
a=$(stat -Lc '%d:%i' /product/bin/su 2>/dev/null) || a=
b=$(stat -Lc '%d:%i' /debug_ramdisk/magisk 2>/dev/null) || b=
if [ -n "$a" ] && [ -n "$b" ] && [ "$a" = "$b" ]; then printf 'same_inode_current_namespace=yes\n'; else printf 'same_inode_current_namespace=no\n'; fi
printf 'failure_lock_present=%s\n' "$(flag test -e /data/local/screenmate-services/run/magisk-failure.lock)"
printf 'boot_disabled=%s\n' "$(flag test -e /data/local/screenmate-services/run/disable-boot)"
printf 'note=observational_only_not_app_root_or_boot_acceptance\n'
