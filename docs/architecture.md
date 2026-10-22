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
