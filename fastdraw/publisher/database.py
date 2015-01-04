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

"""Publish a sample to the database."""

from fastdraw.db import api


class DatabasePublisher(object):
    def __init__(self):
        self.db_api = api

    def publish_samples(self, samples):
        """Send a message for publishing

        :param samples: Samples after transformation
        """
        for sample in samples:
            self._create_resource(sample.as_dict())

    def _create_resource(self, data):
        self.db_api.create_resource(
            name=data['name'], resource_id=None,
            resource_metadata=data['resource_metadata'],
            project_id=None, user_id=None)
