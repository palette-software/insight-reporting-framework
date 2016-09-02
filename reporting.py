import logging
import psycopg2
import yaml

logging.basicConfig(filename='./insight-reporting.log', level=logging.DEBUG)
logging.info('Start Insight Reporting.')

with open("./Config.yml") as fd:
    d = yaml.load(fd.read())

with open("./workflow.yml") as fd:
    wf = yaml.load(fd.read())


schema_name = d["Schema"]

conn = psycopg2.connect("dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**d))
cur = conn.cursor()
cur.execute("set search_path = " + schema_name)

for i in wf:
    cur.execute("select " + i.replace("#schema_name#", "'" + schema_name + "'"))
    for record in cur:
        print(record[0])

conn.commit()
cur.close()
conn.close()

logging.info('End Insight Reporting.')
