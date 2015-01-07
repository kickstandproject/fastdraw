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

from ceilometer import sample
from ceilometer.tests import base

from fastdraw.payload import notifications

QUEUE_CALLER_CREATE = {
    u'_context_auth_token': None,
    u'_context_instance_uuid': None,
    u'_context_is_admin': False,
    u'_context_read_only': False,
    u'_context_request_id': u'req-f44ea673-f89e-4874-a261-fbd2d799ca44',
    u'_context_show_deleted': False,
    u'_context_tenant': None,
    u'_context_user': None,
    u'_unique_id': u'fccdf6c6232c497cb29c4ab291443bea',
    u'event_type': u'queue.caller.create',
    u'message_id': u'9860daf0-1360-11e4-9191-0800200c9a66',
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
    u'priority': u'INFO',
    u'publisher_id': u'payload.example.net',
    u'timestamp': u'2014-07-24 16:52:55.743968',
}

QUEUE_MEMBER_UPDATE = {
    u'_context_auth_token': None,
    u'_context_instance_uuid': None,
    u'_context_is_admin': False,
    u'_context_read_only': False,
    u'_context_request_id': u'req-71120ee4-b896-48c5-9b63-88717dccd828',
    u'_context_show_deleted': False,
    u'_context_tenant': None,
    u'_context_user': None,
    u'_unique_id': u'318252e9e9db4d3f875662a4fb098196',
    u'event_type': u'queue.member.update',
    u'message_id': u'57245369-e2f2-444e-8100-721a90bad25b',
    u'payload': {
        u'status': u'1',
        u'uuid': u'1001@example.org',
        u'created_at': u'2014-12-31T18:23:38Z',
        u'number': u'1001@example.org',
        u'status_at': u'2015-01-07T18:58:05Z',
        u'paused': u'False',
        u'queue_id': u'cc096e0b-0c96-4b8b-b812-ef456f361ee3',
        u'paused_at': u'2014-12-31T18:23:38Z'
    },
    u'priority': u'INFO',
    u'publisher_id': u'payload',
    u'timestamp': u'2015-01-07 18:58:05.966610',
}


class TestNotifications(base.TestCase):

    def test_process_notification(self):
        info = list(notifications.QueueCaller().process_notification(
            QUEUE_CALLER_CREATE))[0]
        for name, actual, expected in [
            ('counter_name', info.name, 'queue.caller.create'),
            ('counter_type', info.type, sample.TYPE_GAUGE),
            ('counter_volume', info.volume, 1),
            ('host', info.resource_metadata['host'],
             QUEUE_CALLER_CREATE['publisher_id']),
            ('queue_id', info.resource_metadata['queue']['id'],
             QUEUE_CALLER_CREATE['payload']['queue']['id']),
            ('timestamp', info.timestamp,
             QUEUE_CALLER_CREATE['timestamp']),

        ]:
            self.assertEqual(expected, actual, name)

    def test_queue_caller_create(self):
        counters = list(notifications.QueueCaller().process_notification(
            QUEUE_CALLER_CREATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_queue_member_update(self):
        counters = list(notifications.QueueMember().process_notification(
            QUEUE_MEMBER_UPDATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
