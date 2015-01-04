# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
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

import abc
import fnmatch

import six


class PluginBase(object):
    """Base class for all plugins."""


@six.add_metaclass(abc.ABCMeta)
class NotificationBase(PluginBase):
    """Base class for plugins that support the notification API."""

    def __init__(self, publishers):
        super(NotificationBase, self).__init__()
        self.publishers = publishers

    @staticmethod
    def _handle_event_type(event_type, match):
        """Check wheather event_type should be handled.

        It is according to match.
        """
        return any(map(lambda e: fnmatch.fnmatch(event_type, e), match))

    @abc.abstractproperty
    def event_types(self):
        """Return a sequence of strings.

        Strings are defining the event types to be given to this plugin.
        """

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        """RPC endpoint for notification messages

        When another service sends a notification over the message
        bus, this method receives it.

        :param ctxt: oslo.messaging context
        :param publisher_id: publisher of the notification
        :param event_type: type of notification
        :param payload: notification payload
        :param metadata: metadata about the notification

        """
        message = {
            'event_type': event_type,
            'metadata': metadata,
            'payload': payload,
            'publisher_id': publisher_id,
        }
        self.to_samples_and_publish(message)

    @abc.abstractmethod
    def process_notification(self, message):
        """Return a sequence of Counter instances for the given message.

        :param message: Message to process.
        """

    def to_samples_and_publish(self, message):
        if not self._handle_event_type(
                message['event_type'], self.event_types):
            return
        for publisher in self.publishers:
            publisher.publish_samples(
                list(self.process_notification(message)))
