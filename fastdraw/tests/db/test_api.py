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

from fastdraw.tests.db import base


class TestCase(base.TestCase):

    def test_create_resource(self):
        row = {
            'name': 'foo.bar',
            'project_id': 'd876d9e4-c389-4c43-8390-862ffb94debc',
            'resource_id': '5d5ab144-db1d-4f5b-8e6f-effc4cb1be86',
            'resource_metadata': {
                'foo': 'bar',
            },
            'user_id': 'd06df789-203c-4511-8575-77e12090eeb1',
        }
        res = self.db_api.create_resource(
            name=row['name'], project_id=row['project_id'],
            resource_id=row['resource_id'],
            resource_metadata=row['resource_metadata'], user_id=row['user_id'])

        for k, v in row.iteritems():
            self.assertEqual(res[k], v)
