# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2013 PolyBeacon, Inc.
#
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

"""SQLAlchemy storage backend."""

import sys

from fastdraw.common import exception
from fastdraw.db.sqlalchemy import models
from fastdraw.openstack.common.db import exception as db_exc
from fastdraw.openstack.common.db.sqlalchemy import session as db_session
from fastdraw.openstack.common import log as logging

LOG = logging.getLogger(__name__)

get_session = db_session.get_session

_DEFAULT_QUOTA_NAME = 'default'


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


def create_resource(
        name, project_id, resource_id, resource_metadata, user_id):
    """Create a new resource."""
    values = {
        'name': name,
        'project_id': project_id,
        'resource_id': resource_id,
        'resource_metadata': resource_metadata,
        'user_id': user_id,
    }

    try:
        res = _create_model(model=models.Resource(), values=values)
    except db_exc.DBDuplicateEntry:
        raise exception.ResourceAlreadyExists(name=values['name'])

    return res


def _create_model(model, values):
    """Create a new model."""
    model.update(values)
    model.save()

    return model
