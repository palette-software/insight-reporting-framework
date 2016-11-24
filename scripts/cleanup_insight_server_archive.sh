#!/bin/bash
#
# Clean up the .csv.gz files in the archive directory
#

INSIGHT_SERVER_DATA_DIR="/data/insight-server/uploads"

CLUSTER_DIRS=$(find ${INSIGHT_SERVER_DATA_DIR} -mindepth 1 -maxdepth 1 -type d)

for CLUSTER_DIR in ${CLUSTER_DIRS}; do
    ARCHIVE_DIRS=$(find "${CLUSTER_DIR}/archive" -mindepth 1 -maxdepth 1 -type d)
    for ARCHIVE_DIR in ${ARCHIVE_DIRS}; do
        # In order not to flood logs with deleted csv files the output is suppressed
        "$(dirname "$0")"/cleanup_dir.sh "${ARCHIVE_DIR}" 61 false > /dev/null
    done
done
