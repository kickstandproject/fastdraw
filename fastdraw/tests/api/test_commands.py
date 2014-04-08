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

from fastdraw.api import commands
from fastdraw.tests import base


class TestCase(base.TestCase):

    def test_answer(self):
        res = commands.answer()
        self.assertEqual("same => n,Answer(0)", res)
        res = commands.answer(delay=1000)
        self.assertEqual("same => n,Answer(1000)", res)

    def test_background(self):
        res = commands.background(['beep'])
        self.assertEqual("same => n,Background(beep)", res)
        res = commands.background(['beep'], skip=True)
        self.assertEqual("same => n,Background(beep,s)", res)
        res = commands.background(['beep'], noanswer=True)
        self.assertEqual("same => n,Background(beep,n)", res)
        res = commands.background(['beep'], match=True)
        self.assertEqual("same => n,Background(beep,m)", res)
        res = commands.background(['beep'], skip=True, match=True)
        self.assertEqual("same => n,Background(beep,s,m)", res)
        res = commands.background(['beep'],
                                  skip=True, match=True, noanswer=True)
        self.assertEqual("same => n,Background(beep,s,n,m)", res)
        res = commands.background(['beep', 'boop'])
        self.assertEqual("same => n,Background(beep&boop)", res)

    def test_goto(self):
        res = commands.goto(context='default')
        self.assertEqual("same => n,Goto(default,s,1)", res)
        res = commands.goto(context='example', exten='555')
        self.assertEqual("same => n,Goto(example,555,1)", res)
        res = commands.goto(context='foo', exten='bar', priority=5)
        self.assertEqual("same => n,Goto(foo,bar,5)", res)

    def test_hangup(self):
        res = commands.hangup()
        self.assertEqual("same => n,Hangup()", res)
        res = commands.hangup(cause='44')
        self.assertEqual("same => n,Hangup(44)", res)

    def test_noop(self):
        res = commands.noop()
        self.assertEqual("same => n,NoOp()", res)
        res = commands.noop('beep')
        self.assertEqual("same => n,NoOp(beep)", res)

    def test_playback(self):
        res = commands.playback(['beep'])
        self.assertEqual("same => n,Playback(beep)", res)
        res = commands.playback(['beep'], noanswer=True)
        self.assertEqual("same => n,Playback(beep,noanswer)", res)
        res = commands.playback(['beep'], skip=True)
        self.assertEqual("same => n,Playback(beep,skip)", res)
        res = commands.playback(['beep'], skip=True, noanswer=True)
        self.assertEqual("same => n,Playback(beep,skip,noanswer)", res)
        res = commands.playback(['beep', 'boop'])
        self.assertEqual("same => n,Playback(beep&boop)", res)
