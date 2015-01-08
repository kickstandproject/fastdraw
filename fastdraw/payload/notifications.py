# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ceilometer.openstack.common import log
from ceilometer import plugin
from ceilometer import sample
from oslo.config import cfg

LOG = log.getLogger(__name__)

OPTS = [
    cfg.StrOpt(
        'control_exchange', default='payload',
        help='Exchange name for Payload notifications.'),
]

GROUP = cfg.OptGroup(
    name='payload', title='Options for the payload service api.')

CONF = cfg.CONF
CONF.register_group(GROUP)
CONF.register_opts(OPTS, GROUP)


class PayloadNotificationBase(plugin.NotificationBase):

    @staticmethod
    def get_exchange_topics(conf):
        """Return a sequence of ExchangeTopics defining the exchange and
        topics to be connected for this plugin.
        """
        return [
            plugin.ExchangeTopics(
                exchange=conf.payload.control_exchange,
                topics=set(topic + ".info"
                           for topic in conf.notification_topics)),
        ]


class QueueCallerCRUD(PayloadNotificationBase):
    """Listen for payload queue caller notifications."""

    event_types = [
        'queue.caller.create',
        'queue.caller.delete',
    ]

    def process_notification(self, message):
        yield sample.Sample.from_notification(
            name=message['event_type'],
            message=message,
            project_id=None,
            resource_id=message['payload']['uuid'],
            type=sample.TYPE_DELTA,
            user_id=None,
            unit='caller',
            volume=1)


class QueueCaller(QueueCallerCRUD):
    """Listen for payload queue caller notifications."""

    def process_notification(self, message):
        yield sample.Sample.from_notification(
            name='queue.caller',
            message=message,
            project_id=None,
            resource_id=message['payload']['uuid'],
            type=sample.TYPE_GAUGE,
            user_id=None,
            unit='caller',
            volume=1)


class QueueMemberCRUD(PayloadNotificationBase):
    """Listen for payload queue member notifications."""

    event_types = [
        'queue.member.add',
        'queue.member.create',
        'queue.member.delete',
        'queue.member.remove',
        'queue.member.update',
    ]

    def process_notification(self, message):
        yield sample.Sample.from_notification(
            name=message['event_type'],
            message=message,
            project_id=None,
            resource_id=message['payload']['uuid'],
            type=sample.TYPE_DELTA,
            user_id=None,
            unit='member',
            volume=1)


class QueueMember(QueueMemberCRUD):
    """Listen for payload queue member notifications."""

    def process_notification(self, message):
        yield sample.Sample.from_notification(
            name='queue.member',
            message=message,
            project_id=None,
            resource_id=message['payload']['uuid'],
            type=sample.TYPE_GAUGE,
            user_id=None,
            unit='member',
            volume=1)
