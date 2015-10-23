import json

import rethinkdb as r
import sseclient

from config import *

def sse_loader():
    """
    Generates event records for insertion into the database.
    """
    print("Starting event loader!")
    sse_source = sseclient.SSEClient("https://api.particle.io/v1/devices/events?access_token=" + ACCESS_TOKEN)
    connection = r.connect(host=DB_HOST, port=28015)

    for e in sse_source:
        if e.data:
            event = e.event
            data = json.loads(e.data)
            data["event"] = event
            print(EVT_TABLE_NAME, data)
            r.db(DB_NAME).table(EVT_TABLE_NAME).insert(data).run(connection)


if __name__ == "__main__":
    sse_loader()
