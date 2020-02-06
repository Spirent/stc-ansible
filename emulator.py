#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-16 22:32:09
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-02-06 12:36:40

from tests.playbook import PlaybookEmulator
from module_utils.logger import Logger
import argparse

parser = argparse.ArgumentParser(
	description='STC Ansible playbook emulator',
)

parser.add_argument('playbook', type=str, help='Ansible playbook to emulate')
parser.add_argument('-labserver', '-s', required=True, metavar='lab-server', help="lab server IP address or DNS")
parser.add_argument('-chassis',  '-c',  help="list of chassis IP address, comma separated", default="")
parser.add_argument('-v',  '--verbose', action='store_true', help="verbose output")
parser.add_argument('-vvv',  '--extraverbose', action='store_true', help="extra verbose output")

args = parser.parse_args()
if args.verbose:
	Logger.setVerbose()
if args.extraverbose:
	Logger.setExtraVerbose()

ports = []
chassis = []
if len(args.chassis)>0:
	chassis = args.chassis.split(",")
	ports = ["//"+ip+"/1/1" for ip in chassis]


emulator = PlaybookEmulator(args.labserver, chassis, ports)
emulator.play(args.playbook)
