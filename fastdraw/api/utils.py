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


def join_audio(files):
    """Concatinate a list of files to be included in dialplan output

    :param files: the list of files to concatinate
    :type files: string list
    """
    if len(files) == 0:
        return ''
    res = '&'.join(files)

    return res


def join_options(options):
    """Concatinate a list of options to be included in dialplan output

    :param options: the list of options to concatinate
    :type options: string list
    """
    if len(options) == 0:
        return ''
    res = ',' + ','.join(options)

    return res
