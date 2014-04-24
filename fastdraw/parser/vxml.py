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

from lxml import etree

from fastdraw.common import exception
from fastdraw.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class VXMLParser(object):

    def __init__(self):
        pass

    def _parse(self, fn):
        try:
            etree.parse(fn)
        except etree.XMLSyntaxError:
            raise exception.InvalidXML(filename=fn.name)

    def parse(self, filename):
        with open(filename) as fn:
            self._parse(fn)
