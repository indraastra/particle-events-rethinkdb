import rethinkdb as r

from config import *

if __name__ == "__main__":
	r.connect(host=DB_HOST, port=DB_PORT).repl()
	db_list = r.db_list().run()
	if DB_NAME not in db_list:
		print("Creating database", DB_NAME)
		print("\t", r.db_create(DB_NAME).run())
		print()

	table_list = r.db(DB_NAME).table_list().run()
	for table in [LOG_TABLE_NAME, EVT_TABLE_NAME]:
		if table in table_list: continue
		print("Creating table", table)
		print("\t", r.db(DB_NAME).table_create(table).run())
		print()

	index_list = r.db(DB_NAME).table(EVT_TABLE_NAME).index_list().run()
	for key in [EVENT_NAME_FIELD, DEVICE_ID_FIELD]:
		if key in index_list: continue
		print("Creating secondary index on", key)
		print("\t", r.db(DB_NAME).table(table).index_create(key).run())
		print()

	print("Database is ready!")