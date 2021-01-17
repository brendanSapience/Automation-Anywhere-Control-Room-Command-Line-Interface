##############################################################
#
# Author: Bren Sapience
# Date: Jan 2021
# Scope:
#
#
##############################################################
#!/usr/bin/env python3

import argparse
import sys
import logging
sys.path.insert(1, './logics')
sys.path.insert(1, './libs')
import AuthLogics
import IQBotLILogics
import IQBotGroupsLogics
import IQBotCommons
import DataUtils

VERSION="0.0.1"
DEFAULT_CR_VERSION = "A2019.18"
SupportedCRVersions = ["A2019.18"]

logging.basicConfig(level=logging.ERROR)

#####
# General Parser
#####

parser = argparse.ArgumentParser()
parser.add_argument('-v','--version', action='version', version=VERSION)
parser.add_argument('-s','--session',type=str,default="", help='Session Name',dest="SESSIONNAME")
parser.add_argument('-f','--format',type=str,default="JSON", help='Output Format <JSON,CSV,DF>',dest="OUTPUTFORMAT")
subparsers = parser.add_subparsers()


li_parser = subparsers.add_parser('li')
li_subparsers = li_parser.add_subparsers()

#####
# Learning Instance Parser
# li <list, list_files, list_groups, show>
#####

# LI list

def li_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    IQBotCommons.list_learning_instances(args.OUTPUTFORMAT,args.SESSIONNAME)

li_list_parser = li_subparsers.add_parser('list')
li_list_parser.set_defaults(func=li_list)


# LI show

def li_show(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.LIID:
        parser.error('no LI ID passed')
    IQBotLILogics.get_learning_instance_detail(args.OUTPUTFORMAT,args.SESSIONNAME,args.LIID)

li_show_parser = li_subparsers.add_parser('show')
li_show_parser.set_defaults(func=li_show)
li_show_parser.add_argument("-i","--id",type=str,default="", help = "<all> Learning Instance ID", dest = "LIID")

# LI list_files

def li_list_files(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.LIID:
        parser.error('no LI ID passed')
    if not args.FILESTATUS:
        args.FILESTATUS = ""
    IQBotLILogics.list_learning_instance_files(args.OUTPUTFORMAT,args.SESSIONNAME,args.LIID,args.FILESTATUS)

li_listfiles_parser = li_subparsers.add_parser('list_files')
li_listfiles_parser.set_defaults(func=li_list_files)
li_listfiles_parser.add_argument("-t","--status",type=str,default="", help = "<list_files> ['','VALIDATION','UNCLASSIFIED','INVALID','SUCCESS','UNTRAINED']", dest = "FILESTATUS")
li_listfiles_parser.add_argument("-i","--id",type=str,default="", help = "<all> Learning Instance ID", dest = "LIID")

# LI list_groups

def li_list_groups(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.LIID:
        parser.error('no LI ID passed')

    IQBotLILogics.list_learning_instance_groups(args.OUTPUTFORMAT,args.SESSIONNAME,args.LIID)

li_listgroups_parser = li_subparsers.add_parser('list_groups')
li_listgroups_parser.set_defaults(func=li_list_groups)
li_listgroups_parser.add_argument("-i","--id",type=str,default="", help = "<all> Learning Instance ID", dest = "LIID")

#####
# Group Parser
# group <list, activate, deactivate>
#####

group_parser = subparsers.add_parser('group')
group_subparsers = group_parser.add_subparsers()

# Group list

def group_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    IQBotGroupsLogics.list_groups(args.OUTPUTFORMAT,args.SESSIONNAME)

grp_list_parser = group_subparsers.add_parser('list')
grp_list_parser.set_defaults(func=group_list)


# Group activate / deactivate

def change_grp_status(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.LIID:
        parser.error('no LI ID passed')
    if not args.GROUPNUM:
        parser.error('no Group number passed')

    IQBotGroupsLogics.change_group_status(args.OUTPUTFORMAT,args.SESSIONNAME,args.LIID,args.GROUPNUM,args.NEWGRPSTATUS)

grp_update_parser = group_subparsers.add_parser('update')
grp_update_parser.set_defaults(func=change_grp_status)
grp_update_parser.add_argument("-i","--id",type=str,default="", help = "Learning Instance ID", dest = "LIID")
grp_update_parser.add_argument("-g","--grp", type=str,default = "", help = "\"ALL\" or one Group Number or a list of Groups separated by commas, ex: \"ALL\" or \"4\" or \"2,3\")", dest = "GROUPNUM")
grp_update_parser.add_argument("-s","--status", type=str,default = "OFF", help = "\"ON\" or \"OFF\")", dest = "NEWGRPSTATUS")


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
