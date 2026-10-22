# Security model and known gaps

This extends **already-rooted ADB**, not a universal root exploit. Authenticated TCP ADB on port 5555 is a privileged management surface. Use trusted transport, narrowly provisioned private authorization and no public port exposure. A loopback client still needs its own protected authorized key; localhost is not a reason to disable authentication. No key provisioning or ADB setting is changed by these tools.

## High-priority live findings

- The original AP parent directory was mode 0777. A non-writable script inside a writable directory can be replaced. Root execution from that chain is a serious code-execution boundary. Use a separately reviewed root-owned entry and secure the entire parent chain in an approved change; this assignment did not chmod or replace the original.
- The readiness gate sleeps between checks and bounds each package query, but has no overall deadline. It can wait indefinitely. [A bounded redesign](../examples/bounded-gate-design.md) is proposed, not deployed.
- The wrapper's cleanup unmount, daemon-stop and live-policy restore operations can block. `set +e` records failures but does not make cleanup atomic or automatically create a failure lock. Partial startup can leave ambiguous ownership: the runtime-exists predicate is not a complete ownership certificate. Recovery may attempt policy load while runtime cleanup was incomplete. Do not silently turn these references into a generic installer.
- Recovery is inert unless explicitly armed. No independently running recovery guardian was established. flock prevents simultaneous supervisors, not supervisor-crash recovery; a boot caller that only monitors the AP watchdog need not notice runsvdir death.
- Five-second health checks cover only daemon presence, owned overlay and enforcing mode, not an actual unprivileged app root transaction. Live runtime label was `system_file` despite startup requesting `magisk_file`; reason unknown. Do not automatically change it.
- Shared mount propagation expands the scope beyond one shell. Verify application namespaces and the same device/inode symlink identity on a sacrificial device; a visible SU path or version string alone is not root-app proof.

## Publication boundaries

Only custom script references and new safe tooling/docs are distributed. Device policy pins become local placeholders. No raw kernel policy, Magisk database, ADB keys, Manager/stub APK, binaries, app authorization, private helper identity, precise network endpoint, full AP watchdog, private logs or personal configuration belongs in Git/history/releases. No telemetry or vehicle application is a service dependency.

All reference scripts fail before original code unless explicitly acknowledged for review. The installation tools have no apply mode and cannot execute their plans. These guards are packaging safeguards, not a hardened production runtime.
