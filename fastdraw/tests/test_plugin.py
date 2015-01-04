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
from fastdraw import plugin
from fastdraw.publisher import test as test_publisher


TEST_NOTIFICATION = {
    u'event_type': u'queue.enter',
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


class NotificationBaseTestCase(test.BaseTestCase):

    def test_handle_event_type(self):
        self.assertFalse(plugin.NotificationBase._handle_event_type(
            'queue.start', ['queue']))
        self.assertTrue(plugin.NotificationBase._handle_event_type(
            'queue.start', ['queue.*']))

    class FakePlugin(plugin.NotificationBase):

        def process_notification(self, message):
            return message

    class FakePayloadPlugin(FakePlugin):
        event_types = ['queue.*']

    class FakeFooPlugin(FakePlugin):
        event_types = ['foo.*']

    def _do_test_to_samples(self, plugin_class, match):
        p = test_publisher.TestPublisher()
        plug = plugin_class([p])

        plug.to_samples_and_publish(TEST_NOTIFICATION)

        if match:
            self.assertEqual(p.samples, list(TEST_NOTIFICATION))
        else:
            self.assertEqual(0, p.calls)

    def test_to_samples_match(self):
        self._do_test_to_samples(self.FakePayloadPlugin, True)

    def test_to_samples_no_match(self):
        self._do_test_to_samples(self.FakeFooPlugin, False)
