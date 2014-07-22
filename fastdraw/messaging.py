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

import eventlet

from oslo.config import cfg
import oslo.messaging

NOTIFIER = None
TRANSPORT = None


def cleanup():
    """Cleanup the oslo.messaging layer."""
    global NOTIFIER, TRANSPORT
    assert NOTIFIER is not None
    assert TRANSPORT is not None
    TRANSPORT.cleanup()
    TRANSPORT = NOTIFIER = None


def get_notification_listener(targets, endpoints):
    """Return a configured oslo.messaging notification listener."""
    global TRANSPORT

    return oslo.messaging.get_notification_listener(
        TRANSPORT, targets, endpoints, executor='eventlet')


def get_notifier(publisher_id):
    """Return a configured oslo.messaging notifier."""
    global NOTIFIER
    return NOTIFIER.prepare(publisher_id=publisher_id)


def setup(url=None):
    global NOTIFIER, TRANSPORT

    if url and url.startswith('fake://'):
        eventlet.monkey_patch(time=True)

    if not TRANSPORT:
        oslo.messaging.set_transport_defaults('fastdraw')
        TRANSPORT = oslo.messaging.get_transport(cfg.CONF)

    if not NOTIFIER:
        NOTIFIER = oslo.messaging.Notifier(TRANSPORT)
