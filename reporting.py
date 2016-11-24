import logging
import logging.handlers
import yaml
from database import Database
import workflow
import sys
import datetime
from jinja2 import Template
import subprocess

# https://docs.python.org/3.5/library/logging.html#logging.addLevelName
# https://docs.python.org/3.5/library/logging.html#logging-levels
# Arbitrary chosen value for custom log level.
# We need a custom level to have 'FATAL' appear in log files (instead of CRITICAL)
FATAL_ERROR = 49

def execute_workflow(workflow, db):
    for item in workflow:
        logging.info('Start "{}"'.format(item['name']))
        if item.get('transaction', False):
            db.execute_multiple_query(item['queries'])
        else:
            db.execute(item['queries'])
        logging.info('End "{}"'.format(item['name']))


def load_config(filename):
    with open(filename) as config_file:
        config = yaml.load(config_file)
    return config


def setup_logging(filename, console_enabled):
    FORMAT = '%(asctime)-15s - %(levelname)-5s - %(module)-10s - %(message)s'

    log_handlers = []

    file_log_handler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=10485760, backupCount=5)

    log_handlers.append(file_log_handler)

    if console_enabled:
        console = logging.StreamHandler()
        log_handlers.append(console)

    logging.basicConfig(level=logging.DEBUG, format=FORMAT, handlers=log_handlers)

    logging.addLevelName(FATAL_ERROR, 'FATAL')


def get_last_loaded_day(db, schema_name):
    return db.execute_single_query("Get last loaded day", "select {schema_name}.get_max_ts_date('{schema_name}', 'p_cpu_usage_agg_report')".format(schema_name=schema_name))[0][0]


def get_last_loadable_day(db, schema_name, last_day):
    return db.execute_single_query("Get last loadable day",
        "select coalesce((max(ts) - interval'1 day' - interval'2 hours')::date, date'1001-01-01') from {schema_name}.p_threadinfo_delta where ts_rounded_15_secs >= date'{last_day}' + interval'2 days' + interval'2 hours'".format(schema_name=schema_name, last_day=last_day))[0][0]


def get_next_day(db, schema_name, last_day):
    return db.execute_single_query("Get next day",
        "select coalesce(min(ts)::date, date'1001-01-01') from {schema_name}.p_threadinfo_delta where ts_rounded_15_secs >= date'{last_day}' + interval'1 day'".format(schema_name=schema_name, last_day=last_day))[0][0]


def run_sh_command(cmd, output):
    subprocess.run(args=cmd, stdout=output, stderr=output)


def maintenance(config):
    logging.info('Start maintenance.')
    log_load_control(config['LoadControlLogFilename'], "Start maintenance...")
    with open(config['LoadControlLogFilename'], "a") as out:
        run_sh_command(['sudo', '/opt/insight-reporting-framework/cleanup_insight_server_archive.sh'], out)
        run_sh_command(['sudo', '-i', '-u', 'gpadmin', '/opt/insight-reporting-framework/cleanup_db_log.sh'], out)

    with open(config['MaintenanceLogFilename'], 'w') as db_out:
        run_sh_command(['sudo', '-i', '-u', 'gpadmin', '/opt/insight-reporting-framework/db_maintenance.sh'], db_out)

    log_load_control(config['LoadControlLogFilename'], "End maintenance.")
    logging.info('End maintenance.')

def load_days(db, config, workflow_filename):
    schema_name = config['Schema']
    last_loaded_day = get_last_loaded_day(db, schema_name)
    last_loadable_day = get_last_loadable_day(db, schema_name, last_loaded_day)

    if last_loaded_day == datetime.date(1001, 1, 1):
        next_day = get_next_day(db, schema_name, last_loaded_day)
    else:
        next_day = last_loaded_day + datetime.timedelta(days=1)

    top_limit = (last_loadable_day - next_day + datetime.timedelta(days=1)).days
    for i in range(0, top_limit):
        maintenance(config)
        load_date = next_day + datetime.timedelta(days=i)
        workflow_doc = workflow.load_from_file(workflow_filename, config, load_date)
        logging.info("Loading date: {}".format(load_date.isoformat()))
        execute_workflow(workflow_doc, db)


def load(db, config, workflow_filename):
    if config['WorkflowType'] == "Daily":
        log_load_control(config['LoadControlLogFilename'], "Start reporting...")
        load_days(db, config, workflow_filename)
        log_load_control(config['LoadControlLogFilename'], "End reporting.")
    elif config['WorkflowType'] == "Delta":
        workflow_doc = workflow.load_from_file(workflow_filename, config)
        execute_workflow(workflow_doc, db)
    else:
        raise Exception("Invalid WorkflowType in the config.yml")


def log_load_control(filename, msg):
    with open(filename, "a") as out:
        out.write(msg + " " + datetime.datetime.now().isoformat() + "\n")


def main():

    try:
        config_filename = sys.argv[1]
        config = load_config(config_filename)

        setup_logging(config['Logfilename'], config['ConsoleLog'])

        logging.info('Start Insight Reporting.')
        workflow_filename = config['WorkflowFilename']
        db = Database(config)
        logging.debug('Executing "{}" workflow'.format(workflow_filename))
        load(db, config, workflow_filename)

        logging.info('End Insight Reporting.')
    except Exception as exception:
        logging.log(FATAL_ERROR, 'Unhandled exception occurred: {}'.format(exception))


if __name__ == '__main__':
    main()
