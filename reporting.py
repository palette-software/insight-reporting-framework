import psycopg2
import yaml

print ("Hello World!")

fd = open("./Config.yml")
f = fd.read()
d = yaml.load(f)

conn = psycopg2.connect("dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**d))

cur = conn.cursor()
cur.execute("select * from palette.db_version_meta order by 1 desc limit 10;")
for record in cur:
    print (record)
    ret = record[0]

conn.commit();
cur.close();
conn.close();

print (ret)
