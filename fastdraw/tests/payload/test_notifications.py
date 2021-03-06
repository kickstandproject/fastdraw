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
    u'_context_request_id': u'req-1216ba12-ff72-4bc4-98b3-720491574ac0',
    u'_context_show_deleted': False,
    u'_context_tenant': None,
    u'_context_user': None,
    u'_unique_id': u'5033527250ba457db491cfba2baef32e',
    u'event_type': u'queue.caller.create',
    u'message_id': u'bad980f6-99c3-45ae-bca7-0c9c44a0a8e1',
    u'payload': {
        u'created_at': u'2015-01-08T02:15:19Z',
        u'name': u'Paul Belanger',
        u'number': u'6135551234',
        u'position': 0,
        u'queue_id': u'cc096e0b-0c96-4b8b-b812-ef456f361ee3',
        u'status': u'1',
        u'status_at': u'2015-01-08T02:15:19Z',
        u'uuid': u'1420683318.7220'
    },
    u'priority': u'INFO',
    u'publisher_id': u'payload.example.net',
    u'timestamp': u'2015-01-08 02:15:19.045539',
}

QUEUE_CALLER_DELETE = {
    u'_context_auth_token': None,
    u'_context_instance_uuid': None,
    u'_context_is_admin': False,
    u'_context_read_only': False,
    u'_context_request_id': u'req-20e9bf87-4903-4273-ab69-2d90ae6d926d',
    u'_context_show_deleted': False,
    u'_context_tenant': None,
    u'_context_user': None,
    u'_unique_id': u'ac704579dbd24beaba01313a3fe609e4',
    u'event_type': u'queue.caller.delete',
    u'message_id': u'fc0d942d-1d1a-4b85-b6d9-567a1d3ed7be',
    u'payload': {
        u'created_at': u'2015-01-08T02:15:19Z',
        u'name': u'Paul Belanger',
        u'number': u'6135551234',
        u'position': 0,
        u'queue_id': u'cc096e0b-0c96-4b8b-b812-ef456f361ee3',
        u'status': u'1',
        u'status_at': u'2015-01-08T02:15:19Z',
        u'uuid': u'1420683318.7220'
    },
    u'priority': u'INFO',
    u'publisher_id': u'payload.example.net',
    u'timestamp': u'2015-01-08 02:15:22.498354',
}

QUEUE_CALLER_UPDATE = {
    u'_context_auth_token': None,
    u'_context_instance_uuid': None,
    u'_context_is_admin': False,
    u'_context_read_only': False,
    u'_context_request_id': u'req-2cd081a1-56a3-435f-9f88-d82a11a866a9',
    u'_context_show_deleted': False,
    u'_context_tenant': None,
    u'_context_user': None,
    u'_unique_id': u'596f7677762c4553a5a6cda629d508b7',
    u'event_type': u'queue.caller.update',
    u'message_id': u'8e5c5d4d-d41f-41e6-bbba-e98f85010185',
    u'payload': {
        u'created_at': u'2015-01-13T23:10:51Z',
        u'name': u'Paul Belanger',
        u'number': u'6135551234',
        u'position': 0,
        u'queue_id': u'cc096e0b-0c96-4b8b-b812-ef456f361ee3',
        u'status': u'1',
        u'status_at': u'2015-01-13T23:10:51Z',
        u'uuid': u'1420683318.7220'
    },
    u'priority': u'INFO',
    u'publisher_id': u'payload.example.net',
    u'timestamp': u'2015-01-13 23:10:51.490459',
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
            ('counter_name', info.name, 'queue.caller'),
            ('counter_type', info.type, sample.TYPE_GAUGE),
            ('counter_volume', info.volume, 1),
            ('host', info.resource_metadata['host'],
             QUEUE_CALLER_CREATE['publisher_id']),
            ('queue_id', info.resource_metadata['queue_id'],
             QUEUE_CALLER_CREATE['payload']['queue_id']),
            ('timestamp', info.timestamp,
             QUEUE_CALLER_CREATE['timestamp']),

        ]:
            self.assertEqual(expected, actual, name)

    def test_QueueCallerCRUD_create(self):
        counters = list(notifications.QueueCallerCRUD().process_notification(
            QUEUE_CALLER_CREATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_QueueCallerCRUD_delete(self):
        counters = list(notifications.QueueCallerCRUD().process_notification(
            QUEUE_CALLER_DELETE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_QueueCallerCRUD_update(self):
        counters = list(notifications.QueueCallerCRUD().process_notification(
            QUEUE_CALLER_UPDATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_queue_caller(self):
        counters = list(notifications.QueueCaller().process_notification(
            QUEUE_CALLER_CREATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_queue_member_crud(self):
        counters = list(notifications.QueueMemberCRUD().process_notification(
            QUEUE_MEMBER_UPDATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)

    def test_queue_member(self):
        counters = list(notifications.QueueMember().process_notification(
            QUEUE_MEMBER_UPDATE))
        self.assertEqual(1, len(counters))
        c = counters[0]
        self.assertEqual(1, c.volume)
