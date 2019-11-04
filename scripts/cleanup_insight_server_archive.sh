#!/bin/bash
#
# Clean up the .csv.gz files in the archive directory
#

INSIGHT_SERVER_ARCHIVES_DIR="/data/insight-server/uploads/palette/archive"
HOST_DIRS=$(find ${INSIGHT_SERVER_ARCHIVES_DIR} -mindepth 1 -maxdepth 1 -type d)
for HOST_DIR in ${HOST_DIRS}; do
    # In order not to flood logs with deleted csv files the output is suppressed
    "$(dirname "$0")"/cleanup_dir.sh "${HOST_DIR}" 61 false > /dev/null
done

INSIGHT_SERVERLOGS_ARCHIVES_DIR="/data/insight-server/serverlogs-archives/palette/uploads/public"
HOST_DIRS=$(find "${INSIGHT_SERVERLOGS_ARCHIVES_DIR}" -mindepth 1 -maxdepth 1 -type d)
for HOST_DIR in ${HOST_DIRS}; do
    # In order not to flood logs with deleted csv files the output is suppressed
    "$(dirname "$0")"/cleanup_dir.sh "${HOST_DIR}" 15 false > /dev/null
done
