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

import copy


class Sample(object):

    def __init__(
            self, project_id, name, resource_metadata, timestamp, user_id,
            volume):
        self.name = name
        self.project_id = project_id
        self.resource_metadata = resource_metadata
        self.timestamp = timestamp
        self.user_id = user_id
        self.volume = volume

    def as_dict(self):
        return copy.copy(self.__dict__)

    @classmethod
    def from_notification(cls, name, message, project_id, user_id, volume):
        metadata = copy.copy(message['payload'])
        metadata['event_type'] = message['event_type']
        metadata['host'] = message['publisher_id']
        return cls(
            name=name,
            project_id=project_id,
            resource_metadata=metadata,
            timestamp=message['metadata']['timestamp'],
            user_id=user_id,
            volume=volume)
