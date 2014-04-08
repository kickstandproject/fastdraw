# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

import fixtures
from oslo.config import cfg
import stubout
import testtools

from fastdraw.openstack.common import log as logging
from fastdraw.tests import conf_fixture

CONF = cfg.CONF
logging.setup('fastdraw')


class MoxStubout(fixtures.Fixture):
    """Deal with code around mox and stubout as a fixture."""

    def setUp(self):
        super(MoxStubout, self).setUp()

        self.stubs = stubout.StubOutForTesting()


class TestCase(testtools.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each method to initialize test environment."""
        super(TestCase, self).setUp()

        self.log_fixture = self.useFixture(fixtures.FakeLogger())
        self.useFixture(conf_fixture.ConfFixture(CONF))
        mox_fixture = self.useFixture(MoxStubout())
        self.stubs = mox_fixture.stubs
