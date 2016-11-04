import logging
import logging.handlers
import yaml
from database import Database
import workflow
import sys
import datetime
from jinja2 import Template

# https://docs.python.org/3.5/library/logging.html#logging.addLevelName
# https://docs.python.org/3.5/library/logging.html#logging-levels
# Arbitrary chosen value for custom log level.
# We need a custom level to have 'FATAL' appear in log files (instead of CRITICAL)
FATAL_ERROR = 49


class PaletteReportingNotAfter2AM(Exception):
    pass


def execute_workflow(workflow, db):
    for item in workflow:
        logging.info('Start "{}"'.format(item['name']))
        if item.get('transaction', False):
            db.execute_in_transaction(item['queries'])
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


def get_last_loaded_day(db):
    return db.execute_single_query("select palette.get_max_ts_date('palette', 'p_cpu_usage_report')")[0][0]


def get_last_loadable_day(db, last_day):
    return db.execute_single_query(
        "select coalesce(max(ts)::date, date'1001-01-01') from palette.p_threadinfo_delta where ts_rounded_15_secs >= date'{}' + interval'1 day'".format(last_day))[0][0]


def get_first_loadable_day(db, last_day):
    return db.execute_single_query(
        "select coalesce(min(ts)::date, date'1001-01-01') from palette.p_threadinfo_delta where ts_rounded_15_secs >= date'{}' + interval'1 day'".format(last_day))[0][0]


def check_passed_2_am():
    if datetime.datetime.today().hour < 2:
        raise PaletteReportingNotAfter2AM("Error: Reporting cannot be executed before 2 AM.")


def load_days(db, config, workflow_filename):
    check_passed_2_am()
    last_loaded_day = get_last_loaded_day(db)
    last_loadable_day = get_last_loadable_day(db, last_loaded_day)

    if last_loaded_day == datetime.date(1001, 1, 1):
        last_loaded_day = get_first_loadable_day(db, last_loaded_day)

    for i in range(1, (last_loadable_day - last_loaded_day).days):
        load_date = last_loaded_day + datetime.timedelta(days=i)
        workflow_doc = workflow.load_from_file(workflow_filename, config, load_date)
        logging.info("Loading date: {}".format(load_date.isoformat()))
        execute_workflow(workflow_doc, db)


def main():
    try:
        config_filename = sys.argv[1]
        config = load_config(config_filename)

        setup_logging(config['Logfilename'], config['ConsoleLog'])

        logging.info('Start Insight Reporting.')
        workflow_filename = config['WorkflowFilename']
        db = Database(config)
        logging.debug('Executing "{}" workflow'.format(workflow_filename))
        load_days(db, config, workflow_filename)

        logging.info('End Insight Reporting.')
    except Exception as exception:
        logging.log(FATAL_ERROR, 'Unhandled exception occurred: {}'.format(exception))


if __name__ == '__main__':
    main()
