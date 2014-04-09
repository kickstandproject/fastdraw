# vim: tabstop=4 shiftwidth=4 softtabstop=4

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
import mock
import testtools

from fastdraw import builder
from fastdraw.cmd import shell
from fastdraw.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        def clear_conf():
            shell.CONF.reset()
            shell.CONF.unregister_opt(shell.command_opt)

        self.addCleanup(clear_conf)

    def _main_test_helper(self, argv, func_name, **exp_args):
        self.useFixture(fixtures.MonkeyPatch('sys.argv', argv))
        shell.main()
        func_name.assert_called_once_with(**exp_args)

    def test_update(self):
        builder.Builder.update = mock.Mock()
        self._main_test_helper(
            ['fastdraw.cmd.shell', 'update', 'foo.vxml'],
            builder.Builder.update, filename='foo.vxml')
