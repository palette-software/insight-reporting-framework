#!/bin/bash

# Fail if there are errors
set -e

LOCKFILE=/tmp/PI_Reporting_Delta.flock

flock -n ${LOCKFILE} \
  python3 /opt/insight-reporting-framework/reporting.py /etc/palette-insight-server/reporting-framework-delta-config.yml