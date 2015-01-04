#
# Copyright 2013 Intel
#
# Author: Shuangtai Tian <shuangtai.tian@intel.com>
#
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

from oslo.config import cfg
import oslo.messaging

from fastdraw import plugin
from fastdraw import sample

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
    def get_targets(conf):
        """Return a sequence of oslo.messaging.Target

        This sequence is defining the exchange and topics to be connected for
        this plugin.
        """
        return [
            oslo.messaging.Target(
                topic=topic, exchange=conf.payload.control_exchange)
            for topic in conf.notification_topics]


class QueueCaller(PayloadNotificationBase):
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
            user_id=None,
            volume=1)


class QueueMember(PayloadNotificationBase):
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
            user_id=None,
            volume=1)
