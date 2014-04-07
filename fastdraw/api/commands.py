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


def answer(delay=0):
    """Answer the channel.

    :param delay: The number of milliseconds to wait before moving to the next
                  priority.
    :type delay: int
    """
    res = 'same => n,Answer(%d)' % delay

    return res


def goto(context, exten='s', priority=1):
    res = 'same => n,Goto(%s,%s,%d)' % (context, exten, priority)

    return res


def hangup(cause=''):
    """Hangup the calling channel.

    :param cause: Hangup cause code to use for the channel.
    :type cause: str
    """
    res = 'same => n,Hangup(%s)' % cause

    return res


def noop(comment=''):
    """Add a noop

    :param comment: The comment string for this NoOp (default: '')
    :type comment: string
    """
    res = 'same => n,NoOp(%s)' % comment

    return res
