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

from fastdraw.telephony import utils
from fastdraw.tests import base


class TestCase(base.TestCase):

    def test_join_audio(self):
        res = utils.join_audio([])
        self.assertEqual('', res)
        res = utils.join_audio(['hi'])
        self.assertEqual('hi', res)
        res = utils.join_audio(['hi', 'bye'])
        self.assertEqual('hi&bye', res)

    def test_join_options(self):
        res = utils.join_options([])
        self.assertEqual('', res)
        res = utils.join_options(['hi'])
        self.assertEqual(',hi', res)
        res = utils.join_options(['hi', 'bye'])
        self.assertEqual(',hi,bye', res)
