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

import oslo.messaging
import oslo.messaging.conffixture

from fastdraw import messaging
from fastdraw import notification
from fastdraw.openstack.common.fixture import config
from fastdraw.publisher import test as test_publisher
from fastdraw.tests import base as tests_base

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


class NotificationServiceTestCase(tests_base.BaseTestCase):

    def setUp(self):
        super(NotificationServiceTestCase, self).setUp()
        self.CONF = self.useFixture(config.Config()).conf
        self.useFixture(oslo.messaging.conffixture.ConfFixture(self.CONF))

        self.CONF.set_override('notification_driver', 'messaging')
        self.CONF.set_override('control_exchange', 'payload')
        messaging.setup('fake://')
        self.addCleanup(messaging.cleanup)

        self.publisher = test_publisher.TestPublisher()
        self.srv = notification.NotificationService(self.publisher)

    def test_start(self):
        self.srv.start()
        notifier = messaging.get_notifier('foobar')
        notifier.info(
            None, TEST_NOTIFICATION['event_type'],
            TEST_NOTIFICATION['payload'])
        self.srv.stop()
