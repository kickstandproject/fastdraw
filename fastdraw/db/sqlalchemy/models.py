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

import json

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator

from fastdraw.openstack.common.db.sqlalchemy import models


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)


class FastdrawBase(models.TimestampMixin, models.ModelBase):

    metadata = None


Base = declarative_base(cls=FastdrawBase)


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    project_id = Column(String(255))
    resource_id = Column(String(255), nullable=False)
    resource_metadata = Column(JSONEncodedDict())
    user_id = Column(String(255))
