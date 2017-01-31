# Palette Insight Architecture

![Palette Insight Architecture](https://github.com/palette-software/palette-insight/blob/master/insight-system-diagram.png?raw=true)

# Palette Reporting Framework

[LoadTables]: https://github.com/palette-software/insight-gp-import
[Data Model]: https://github.com/palette-software/insight-data-model
## What is Palette Reporting Framework?

It processes the data loaded by [LoadTables] in multiple stages and makes it available for the Palette Insight Reporting Workbooks.
The workflow for the data processing can be found in [Data Model].

In this repository you will also find:

- maintenance script for the processed CSV files of the [LoadTables] service
 ([scripts/cleanup_insight_server_archive.sh](scripts/cleanup_insight_server_archive.sh))
- maintenance script for the log files of the Greenplum Database
 ([scripts/cleanup_db_log.sh](scripts/cleanup_db_log.sh))
- maintenance script for the Palette database schema
 ([scripts/db_maintenance.sh](scripts/db_maintenance.sh))

## How do I set up Palette Reporting Framework?

### Prerequisites

- Palette Reporting Framework is compatible with Python 3.5
- Workflow YAML files from the [Data Model] repository

### Packaging

To build the package you may use the [create_rpm.sh](create_rpm.sh) script:

```bash
export VERSION_NUMBER="$(sed -n 's/Version. \([0-9]*\.[0-9]*\.[0-9]*$\)/\1/p' < reporting-framework-config.yml)"
export PACKAGEVERSION=123
export VERSION=v$VERSION_NUMBER.$PACKAGEVERSION

./create_rpm.sh
```

### Configuration

Make sure your database (`Host`, `Port`, `User`, `Password`, `Database` and `Schema`)
and `WorkflowFilename` settings are correct.

### Installation

The most convenient is to build the RPM package and install it using either yum or rpm.
It does require and install the other necessary components and services.

## How can I test-drive Palette Reporting Framework?

If you have not installed it as an RPM package then install the required python modules by

```bash
pip install -r requirements.txt
```

Then run
```bash
python reporting.py reporting-framework-config.yml
python reporting.py reporting-framework-delta-config.yml
```

In order to allow only one instance to run it is advised to use the
[run_reporting.sh](run_reporting.sh) or [run_reporting_delta.sh](run_reporting_delta.sh) scripts.

The tests can be run with:

```bash
python -m unittest
```

## Is Palette Reporting Framework supported?

Palette Reporting Framework is licensed under the GNU GPL v3 license. For professional support please contact developers@palette-software.com

Any bugs discovered should be filed in the [Palette Reporting Framework Git issue tracker](https://github.com/palette-software/insight-reporting-framework/issues) or contribution is more than welcome.
