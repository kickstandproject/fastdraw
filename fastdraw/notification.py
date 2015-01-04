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
from stevedore import extension

from fastdraw import messaging
from fastdraw.openstack.common import log as logging
from fastdraw.openstack.common import service as os_service
from fastdraw.publisher import database as db_publisher
from fastdraw.publisher import faye as faye_publisher

LOG = logging.getLogger(__name__)


class NotificationService(os_service.Service):

    NOTIFICATION_NAMESPACE = 'fastdraw.notification'

    @classmethod
    def _get_notifications_manager(cls, publishers):
        return extension.ExtensionManager(
            namespace=cls.NOTIFICATION_NAMESPACE,
            invoke_on_load=True,
            invoke_args=(publishers, ))

    def start(self):
        super(NotificationService, self).start()

        publish = [
            db_publisher.DatabasePublisher(),
            faye_publisher.FayePublisher(),
        ]

        self.notification_manager = self._get_notifications_manager(publish)

        if not list(self.notification_manager):
            LOG.warning(
                'Failed to load any notification handlers for %s',
                self.NOTIFICATION_NAMESPACE)

        endpoints = []
        targets = []
        for ext in self.notification_manager:
            handler = ext.obj
            LOG.debug(
                'Event types from %(name)s: %(type)s' %
                {'name': ext.name,
                 'type': ', '.join(handler.event_types)})
            targets.extend(handler.get_targets(cfg.CONF))
            endpoints.append(handler)

        self.listeners = []
        listener = messaging.get_notification_listener(
            targets, endpoints)
        listener.start()
        self.listeners.append(listener)

        # Add a dummy thread to have wait() working
        self.tg.add_timer(604800, lambda: None)

    def stop(self):
        map(lambda x: x.stop(), self.listeners)
        super(NotificationService, self).stop()
