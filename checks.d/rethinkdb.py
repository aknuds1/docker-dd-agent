    #!/usr/bin/env python
from checks import AgentCheck
import time

class RethinkDBCheck(AgentCheck):
    def check(self, instance):
        self.log.info('Checking RethinkDB connectivity')
        msg_title = 'RethinkDB is functioning'
        msg_text = 'RethinkDB was successfully queried for data'
        alert_type = 'info'
        self.event({
            'timestamp': int(time.time()),
            'event_type': 'rethinkdb_check',
            'msg_title': msg_title,
            'msg_text': msg_text,
            'alert_type': alert_type,
        })

if __name__ == '__main__':
    check, instances = RethinkDBCheck.from_yaml('/path/to/conf.d/http.yaml')
    for instance in instances:
        print('Checking RethinkDB...')
        check.check(instance)
        if check.has_events():
            print('Events: {}'.format(check.get_events()))
        print('Metrics: {}'.format(check.get_metrics()))
