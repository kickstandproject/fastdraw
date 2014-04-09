# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2014 PolyBeacon, Inc.
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

from fastdraw.openstack.common import log as logging
from fastdraw.parser import vxml

LOG = logging.getLogger(__name__)


class Builder(object):

    def __init__(self):
        self.parser = vxml.VXMLParser()

    def load_files(self, filename):
        files_to_parse = [filename]
        for in_file in files_to_parse:
            LOG.debug('Parsing VXML file {0}'.format(in_file))
            self.parser.parse(in_file)

    def update(self, filename):
        self.load_files(filename)
