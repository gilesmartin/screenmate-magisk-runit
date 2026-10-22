# Proposed readiness improvement — not deployed

The extracted gate waits indefinitely but sleeps five seconds between checks; its package query has an eight-second timeout. A future revision should use a monotonic overall deadline, preserve the eight-second query bound, latch a failure/down state on expiry, and require explicit investigation before retry. Test signal handling and runit respawn behavior in isolation first. This proposal is not a claim that the live gate already has these properties.
