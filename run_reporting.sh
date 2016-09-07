#!/bin/bash

# Fail if there are errors
set -e

LOCKFILE=/tmp/PI_Reporting.flock

flock -n ${LOCKFILE} \
  python3 /opt/insight-reporting-framework /etc/palette-insight-server/reporting-framework-config.yml