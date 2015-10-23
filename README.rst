Description
===========
Uses `RethinkDB <http://www.rethinkdb.com>`_ as a persistence layer for events published
to the Particle cloud. Also provides an optional log server for posting custom events
to without going through the Particle cloud.

Requirements
============

* `rethinkdb`
* `sseclient` (for evt_monitor.py)
* `tornado` (for log_monitor.py)

Usage
=====

	$ rethinkdb &

	$ python3 setup_db.py

	Creating database particle
		...
	Creating table logs
		...
	Creating table events
		...
	Creating secondary index on coreid
		...
	Creating secondary index on event
		...
	Database is ready!

	$ python3 evt_monitor.py &
	Starting event loader!
	events {'published_at': '2015-10-23T23:28:17.508Z', 'coreid': 'xxx', 'ttl': '60', 'event': 'spark/status', 'data': 'online'}
	...

	$ python3 log_monitor.py &

	$ curl -H "Content-Type: application/json" -X POST -d '{"foo":"bar"}' localhost:8081/log
	logs {'foo': 'bar'}

Queries
=======

Open `localhost:8080` in your browser and use the "Data Explorer" tab to run queries interactively.

Get unique device IDs:

	r.db('particle').table('events').pluck('coreid').distinct()

Count events by type of event:

	r.db('particle').table('events').group('event').count()


You can also follow the `quickstart guide <https://www.rethinkdb.com/docs/quickstart/>`_ for a
better tutorial of rethinkdb and its query language.