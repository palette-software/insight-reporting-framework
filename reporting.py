import logging
import psycopg2
import yaml


def main():
    logging.basicConfig(filename='./insight-reporting.log', level=logging.DEBUG)
    logging.info('Start Insight Reporting.')

    with open("./Config.yml") as config_file:
        config = yaml.load(config_file)

    with open("./workflow.yml") as workflow_file:
        workflow = yaml.load(workflow_file)

    schema_name = config["Schema"]

    conn = psycopg2.connect("dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**config))
    cur = conn.cursor()
    cur.execute("set search_path = " + schema_name)

    for i in workflow:
        cur.execute("select " + i.replace("#schema_name#", "'" + schema_name + "'"))
        for record in cur:
            print(record[0])

    conn.commit()
    cur.close()
    conn.close()

    logging.info('End Insight Reporting.')


if __name__ == '__main__':
    main()
