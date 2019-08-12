#!/usr/bin/python

import argparse
import os
from settings import *
from scheduler_finder import SchedulerFinder
from file_helper import ConfigFileHelper, TextFileHelper

def set_values(args):
    if not args.broadcast_ip:
        args.broadcast_ip = HOST_BROADCAST_IP
    if not args.finder_port:
        args.finder_port = SCHED_FINDER_PORT
    if not args.finder_net_interface:
        args.finder_net_interface = VM_NETWORK_INTERFACE
    if not args.finder_timeout:
        args.finder_timeout = SCHED_FINDER_WAIT_TIMEOUT_IN_SECS
    if not args.sched_udp_port:
        args.sched_udp_port = SCHEDULER_UDP_PORT
    if not args.sched_version:
        args.sched_version = SCHEDULER_VERSION
    if not args.sched_net_name:
        args.sched_net_name = SCHEDULER_NETWORK_NAME
    if not args.icecc_host_conf_key:
        args.icecc_host_conf_key = ICECC_SCHEDULER_HOST_CONFIG_KEY
    if not args.icecc_conf:
        args.icecc_conf = ICECC_CONFIG_FILE
    if not args.docker_args_file:
        args.docker_args_file = DOCKER_ARGS_FILE
    if not args.docker_ref_line:
        args.docker_ref_line = DOCKER_ARGS_REF_LINE
    if not args.docker_new_line:
        args.docker_new_line = DOCKER_ARGS_NEW_LINE
    if not args.iceccd_start_command:
        args.iceccd_start_command = ICECCD_START_COMMAND

def set_args(parser):
    parser.add_argument("-b", "--broadcast_ip", help="Broadcast IP address", type=str)
    parser.add_argument("-fp", "--finder_port", help="Scheduler finder listening port", type=int)
    parser.add_argument("-fi", "--finder_net_interface", help="Scheduler finder network interface", type=str)
    parser.add_argument("-ft", "--finder_timeout", help="Scheduler finder wait timeout in seconds", type=int)
    parser.add_argument("-sp", "--sched_udp_port", help="Icecream scheduler UDP port", type=int)
    parser.add_argument("-sv", "--sched_version", help="Icecream scheduler version", type=int)
    parser.add_argument("-sn", "--sched_net_name", help="Icecream scheduler network name", type=str)
    parser.add_argument("-ic", "--icecc_conf", help="Icecream config file", type=str)
    parser.add_argument("-ik", "--icecc_host_conf_key", help="Icecream host config key", type=str)
    parser.add_argument("-df", "--docker_args_file", help="File with args for Docker", type=str)
    parser.add_argument("-dr", "--docker_ref_line", help="New line will be inserted after this line in the Docker args file", type=str)
    parser.add_argument("-dn", "--docker_new_line", help="New line to be added to docker args file", type=str)
    parser.add_argument("-id", "--iceccd_start_command", help="Command to start the icecream daemon", type=str)

def main():
    args_parser = argparse.ArgumentParser()
    set_args(args_parser)
    args = args_parser.parse_args()
    set_values(args)
    sched_finder = SchedulerFinder(broadcast_ip=args.broadcast_ip
                                   , port=args.finder_port
                                   , network_interface=args.finder_net_interface
                                   , wait_timeout_in_secs=args.finder_timeout
                                   , scheduler_udp_port=args.sched_udp_port
                                   , scheduler_version=args.sched_version
                                   , scheduler_net_name=args.sched_net_name)
    icecc_conf_file = ConfigFileHelper(args.icecc_conf)
    docker_args_file = TextFileHelper(args.docker_args_file)
    docker_args_file.add_new_line_after(args.docker_ref_line, args.docker_new_line)
    scheduler_ip_address = sched_finder.get_scheduler_ip_address() 
    if scheduler_ip_address:
        if icecc_conf_file.add_key_value_pair(args.icecc_host_conf_key, scheduler_ip_address):
           os.system(args.iceccd_start_command)


if __name__ == "__main__":
    main()