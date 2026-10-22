#!/bin/sh
# SPDX-License-Identifier: MIT
set -eu
D=$(CDPATH="" cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$D/plan.py" uninstall "$@"
