#!/usr/bin/env python
from checks import AgentCheck
import time
import rethinkdb as r
import os


class RethinkDBCheck(AgentCheck):
    def check(self, instance):
        self.log.info('Checking RethinkDB connectivity...')
        rethinkdb_host = os.environ.get('RETHINKDB_HOST', 'localhost')
        rethinkdb_auth_key = os.environ['RETHINKDB_AUTH_KEY']
        try:
            with r.connect(
                    host=rethinkdb_host, db='muzhack',
                    auth_key=rethinkdb_auth_key) as conn:
                projects = r.table('projects').run(conn)
        except r.ReqlError as err:
            self.log.warn(
                'Connecting to RethinkDB @ {} failed: {}'
                    .format(rethinkdb_host, err))
            msg_title = 'RethinkDB is not connectable'
            msg_text = 'RethinkDB did not respond on adress {}'.format(
                rethinkdb_host)
            alert_type = 'error'
        else:
            if projects:
                self.log.info('RethinkDB works, successfully queried projects')
                msg_title = 'RethinkDB is functioning'
                msg_text = 'RethinkDB was successfully queried for data'
                alert_type = 'info'
            else:
                self.log.info(
                    'RethinkDB doesn\'t work, couldn\t query projects')
                msg_title = 'RethinkDB returns no data'
                msg_text = 'RethinkDB did not return any projects'
                alert_type = 'error'
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'rethinkdb_check',
            'msg_title': msg_title,
            'msg_text': msg_text,
            'alert_type': alert_type,
        })
