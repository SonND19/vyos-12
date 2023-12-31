#!/usr/bin/env python3
#
# Copyright (C) 2018 VyOS maintainers and contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# File: vyos-show-version
# Purpose:
#    Displays image version and system information.
#    Used by the "run show version" command.


import os
import argparse

from sys import exit
from vyos.config import Config
from vyos.utils.process import call

PDNS_CMD='/usr/bin/rec_control --socket-dir=/run/powerdns'

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", action="store_true", help="Reset all cache")
parser.add_argument("domain", type=str, nargs="?", help="Domain to reset cache entries for")

if __name__ == '__main__':
    args = parser.parse_args()

    # Do nothing if service is not configured
    c = Config()
    if not c.exists_effective(['service', 'dns', 'forwarding']):
        print("DNS forwarding is not configured")
        exit(0)

    if args.all:
        call(f"{PDNS_CMD} wipe-cache \'.$\'")
        exit(0)

    elif args.domain:
        call(f"{PDNS_CMD} wipe-cache \'{0}$\'".format(args.domain))

    else:
        parser.print_help()
        exit(1)
