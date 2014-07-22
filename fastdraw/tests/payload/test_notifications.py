#
# Copyright (C) 2013-2014 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastdraw.openstack.common import test
from fastdraw.payload import notifications

QUEUE_CALLER_CREATE = {
    u'event_type': u'queue.caller.create',
    u'payload': {
        u'called': {
            u'number': u'6135551234',
        },
        u'caller': {
            u'id': u'rPhIaKtm3EKpIi.uPQIAoSypw0O079Q6',
            u'name': u'Paul Belanger',
            u'number': u'213',
        },
        u'position': u'5',
        u'queue': {
            u'id': u'8de686f6-dbaa-4414-b45a-53e8a125d882',
            u'name': u'support',
            u'number': u'101',
        },
    },
    u'metadata': {
        u'message_id': u'9860daf0-1360-11e4-9191-0800200c9a66',
        u'timestamp': u'2014-07-24 16:52:55.743968',
    },
    u'publisher_id': u'payload.example.net',
}

QUEUE_CALLER_DELETE = {
    u'event_type': u'queue.caller.delete',
    u'payload': {
        u'called': {
            u'number': u'6135551234',
        },
        u'caller': {
            u'id': u'rPhIaKtm3EKpIi.uPQIAoSypw0O079Q6',
            u'name': u'Paul Belanger',
            u'number': u'213',
        },
        u'position': u'1',
        u'queue': {
            u'id': u'8de686f6-dbaa-4414-b45a-53e8a125d882',
            u'name': u'support',
            u'number': u'101',
        },
        u'reason': u'0',
    },
    u'metadata': {
        u'message_id': u'9860daf0-1360-11e4-9191-0800200c9a66',
        u'timestamp': u'2014-07-24 16:52:55.743968',
    },
    u'publisher_id': u'payload.example.net',
}


class TestNotifications(test.BaseTestCase):

    def test_process_notification(self):
        info = list(notifications.QueueCaller(None).process_notification(
            QUEUE_CALLER_CREATE))[0]
        for name, actual, expected in [
            ('counter_name', info.name, 'queue.caller.create'),
            ('counter_volume', info.volume, 1),
            ('host', info.resource_metadata['host'],
             QUEUE_CALLER_CREATE['publisher_id']),
            ('queue_id', info.resource_metadata['queue']['id'],
             QUEUE_CALLER_CREATE['payload']['queue']['id']),
            ('timestamp', info.timestamp,
             QUEUE_CALLER_CREATE['metadata']['timestamp']),

        ]:
            self.assertEqual(expected, actual, name)

    def test_queue_caller_create(self):
        counters = list(notifications.QueueCaller(None).process_notification(
            QUEUE_CALLER_CREATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_queue_caller_delete(self):
        counters = list(notifications.QueueCaller(None).process_notification(
            QUEUE_CALLER_DELETE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
