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

"""
CLI interface for Fastdraw builder.
"""

import logging

from oslo.config import cfg

from fastdraw import builder
from fastdraw.common import config
from fastdraw.openstack.common import log

CONF = cfg.CONF
LOG = log.getLogger(__name__)


def do_update():
    build = builder.Builder()
    build.update(filename=CONF.command.filename)


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('update')
    parser.add_argument('filename')
    parser.set_defaults(func=do_update)


command_opt = cfg.SubCommandOpt(
    'command', title='Commands', help='Available commands',
    handler=add_command_parsers)


def main():
    CONF.register_cli_opt(command_opt)
    config.parse_args()
    log.setup('fastdraw')
    CONF.log_opt_values(LOG, logging.INFO)

    CONF.command.func()
