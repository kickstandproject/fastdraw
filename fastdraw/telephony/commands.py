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


from fastdraw.telephony import utils


def answer(delay=0):
    """Answer the channel.

    :param delay: The number of milliseconds to wait before moving to the next
                  priority.
    :type delay: int
    """
    res = 'Answer(%d)' % delay

    return res


def background(prompts, skip=False, noanswer=False, match=False):
    """Play sound while waiting for extension

    :param prompts: The files to be played
    :param prompts: list of strings
    :param skip: Skips playback if channel is not 'UP' (default: False)
    :type skip: boolean
    :param noanswer: Don't answer channel before playing files (default: False)
    :type noanswer: boolean
    :param match: Break if a digit matches a 1 digit extension (default: False)
    :type match: boolean
    """
    options = []
    if skip:
        options.append('s')
    if noanswer:
        options.append('n')
    if match:
        options.append('m')
    res = 'Background(%s%s)' % (
        utils.join_audio(prompts), utils.join_options(options))

    return res


def goto(context, exten='s', priority=1):
    """Goto another point in the dialplan

    :param context: The context or label to jump to
    :type context: string
    :param exten: The extension within that context to goto (default: s)
    :type exten: string
    :param priority: The line within the extension (default: 1)
    :type priority: int
    """
    res = 'Goto(%s,%s,%d)' % (context, exten, priority)

    return res


def hangup(cause=''):
    """Hangup the calling channel.

    :param cause: Hangup cause code to use for the channel.
    :type cause: str
    """
    res = 'Hangup(%s)' % cause

    return res


def noop(comment=''):
    """Add a noop

    :param comment: The comment string for this NoOp (default: '')
    :type comment: string
    """
    res = 'NoOp(%s)' % comment

    return res


def playback(prompts, skip=False, noanswer=False):
    """Playback the specified prompts.

    :param prompts: The files to playback
    :type prompts: string
    :param skip: Do not play if not answered (default: False)
    :type skip: boolean
    :param noanswer: Playback without answering (default: False)
    :type noanswer: boolean
    """
    options = []
    if skip:
        options.append('skip')
    if noanswer:
        options.append('noanswer')
    res = 'Playback(%s%s)' % (
        utils.join_audio(prompts), utils.join_options(options))

    return res
