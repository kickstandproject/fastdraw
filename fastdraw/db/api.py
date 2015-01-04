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

from oslo.config import cfg

from fastdraw.openstack.common.db import api as db_api
from fastdraw.openstack.common import log as logging

CONF = cfg.CONF

_BACKEND_MAPPING = {'sqlalchemy': 'fastdraw.db.sqlalchemy.api'}

IMPL = db_api.DBAPI(backend_mapping=_BACKEND_MAPPING)
LOG = logging.getLogger(__name__)


def create_resource(name, project_id, resource_id, resource_metadata, user_id):
    return IMPL.create_resource(
        name=name, project_id=project_id, resource_id=resource_id,
        resource_metadata=resource_metadata, user_id=user_id)
