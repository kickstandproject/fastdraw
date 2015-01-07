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

"""Publish a sample using the Faye pub/sub messaging system."""

from ceilometer.openstack.common import log
from ceilometer import publisher
from oslo.config import cfg
import requests
import simplejson

OPTS = [
    cfg.StrOpt(
        'url', default='http://127.0.0.1:4000/faye',
        help='URL for faye service.'),
]
GROUP = cfg.OptGroup(
    name='faye', title='Options for the Faye service api.')

CONF = cfg.CONF
CONF.register_group(GROUP)
CONF.register_opts(OPTS, GROUP)
LOG = log.getLogger(__name__)


class FayePublisher(publisher.PublisherBase):

    def __init__(self, parsed_url):
        super(FayePublisher, self).__init__(parsed_url)

        self.headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

    def publish_samples(self, context, samples):
        """Send a metering message for publishing

        :param context: Execution context from the service or RPC call
        :param samples: Samples from pipeline after transformation
        """
        for sample in samples:
            self._faye(sample.as_dict())

    def _faye(self, data):
        event = data['name'].replace(".", "_")
        channel = "/%s" % event
        data = {
            'channel': channel,
            'data': {
                'event_type': data['name'],
                'payload': data['resource_metadata'],
            }
        }
        requests.post(
            CONF.faye.url, data=simplejson.dumps(data), headers=self.headers,
            verify=False)
