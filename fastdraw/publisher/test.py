#
# Copyright 2013 eNovance
#
# Author: Julien Danjou <julien@danjou.info>
#
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

"""Publish a sample in memory, useful for testing
"""


class TestPublisher(object):

    def __init__(self):
        self.samples = []
        self.calls = 0

    def publish_samples(self, samples):
        """Send a message for publishing

        :param samples: Samples after transformation
        """
        self.samples.extend(samples)
        self.calls += 1
