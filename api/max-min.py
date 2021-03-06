#max/min for the day with nodes
import psycopg2
import time

#run every hour

DB_PASSWORD = "password"
DB_USER = "yggindex"
DB_NAME = "yggindex"
DB_HOST = "localhost"

def age_calc(ustamp):
	if (time.time() - ustamp) <= 14400 :
		return True
	else:
		return False

def get_nodes_for_count():
	dbconn = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
	cur = dbconn.cursor()
	nodes = {}
	cur.execute("select * from yggindex")

	for i in cur.fetchall():
		if age_calc(int(i[2])):
			nodes[i[0]] = [i[1],int(i[2])]

	cur.close()
	dbconn.close()

	return str(len(nodes))

def add_to_db():
	dbconn = psycopg2.connect(host=DB_HOST,database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
	cur = dbconn.cursor()

	cur.execute('''INSERT INTO timeseries(max, unixtstamp) VALUES(''' + "'" + get_nodes_for_count() + "'," + str(int(time.time())) + ''')''')

	dbconn.commit()
	cur.close()
	dbconn.close()

add_to_db()
