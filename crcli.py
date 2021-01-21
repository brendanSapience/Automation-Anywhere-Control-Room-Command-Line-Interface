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
import DevicesLogics
import UsersLogics
import RolesLogics
import ObjectsLogics
import WLMLogics
import ActivitiesLogics
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

#####
# AUTH Parser
# Authentication commands
# auth <login,logout,list>
#####

def login(args):
    if not args.LOGIN:
        parser.error('no login passed')
    if not args.PWD:
        parser.error('no password passed')
    if not args.URL:
        parser.error('no url passed')
    if not args.SESSIONNAME:
        args.SESSIONNAME = DataUtils.RandomSessionNameGenerator()
    AuthLogics.login(args.CRVERSION,args.URL,args.LOGIN,args.PWD,args.SESSIONNAME)

def logout(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    AuthLogics.logout(args.SESSIONNAME)


def listsessions(args):
    AuthLogics.listSessions()

auth_parser = subparsers.add_parser('auth')
auth_subparsers = auth_parser.add_subparsers()

# auth login
login_parser = auth_subparsers.add_parser('login')
login_parser.add_argument('-u','--user',type=str,default="", help='CR Login', dest="LOGIN")
login_parser.add_argument('-s','--session',type=str,default="", help='Session Name',dest="SESSIONNAME")
login_parser.add_argument('-p', '--pwd',type=str,default="", help='CR Password', dest="PWD")
login_parser.add_argument('-r', '--url',type=str,default="", help='CR URL',dest="URL")
login_parser.add_argument('-v', '--version',type=str,default=DEFAULT_CR_VERSION, help='CR Version',dest="CRVERSION")
#login_parser.add_argument('-s', '--session',type=str,default="", help='Session Name',dest="SESSIONNAME")
login_parser.set_defaults(func=login)

# auth logout
login_parser = auth_subparsers.add_parser('logout')
#login_parser.add_argument('-s', '--session',type=str,default="", help='Session Name',dest="SESSIONNAME")
login_parser.set_defaults(func=logout)

# auth list
sesslist_parser = auth_subparsers.add_parser('list')
sesslist_parser.set_defaults(func=listsessions)


#####
# Device Parser
# device <list>
#####

def device_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    DevicesLogics.device_list(args.OUTPUTFORMAT,args.SESSIONNAME)

# Device commands
device_parser = subparsers.add_parser('device')
device_subparsers = device_parser.add_subparsers()

# device list
device_list_parser = device_subparsers.add_parser('list')
device_list_parser.set_defaults(func=device_list)


#####
# Role Parser
# role <list>
#####

def role_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    RolesLogics.role_list(args.OUTPUTFORMAT,args.SESSIONNAME)

# Role commands
role_parser = subparsers.add_parser('role')
role_subparsers = role_parser.add_subparsers()

# role list
role_list_parser = role_subparsers.add_parser('list')
role_list_parser.set_defaults(func=role_list)

#####
# Activity Parser
# activity <list>
#####

# activity commands
activity_parser = subparsers.add_parser('activity')
activity_subparsers = activity_parser.add_subparsers()

# activity list
def activity_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')

    ActivitiesLogics.activity_list(args.OUTPUTFORMAT,args.SESSIONNAME)

activity_list_parser = activity_subparsers.add_parser('list')
activity_list_parser.set_defaults(func=activity_list)


#####
# User Parser
# user <list>
#####

# User commands
user_parser = subparsers.add_parser('user')
user_subparsers = user_parser.add_subparsers()

# user list
def user_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    UsersLogics.user_list(args.OUTPUTFORMAT,args.SESSIONNAME)

user_list_parser = user_subparsers.add_parser('list')
user_list_parser.set_defaults(func=user_list)

# user create
def user_create(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.USERNAME:
        parser.error('You need to pass parameter -u (--username)')
    if not args.PASSWORD:
        parser.error('You need to pass parameter -p (--password)')
    if not args.EMAIL:
        parser.error('You need to pass parameter -e (--email)')

    UsersLogics.create(args.OUTPUTFORMAT,args.SESSIONNAME,args.USERNAME,args.PASSWORD,args.EMAIL,args.ROLES,args.DESC,args.FIRSTNAME,args.LASTNAME)

user_create_parser = user_subparsers.add_parser('create')
user_create_parser.set_defaults(func=user_create)
user_create_parser.add_argument("-u","--username", type=str, help = "Username (ex: \"linus\") or list of Usernames (ex: \"linus,carly,yli\")", dest = "USERNAME")
user_create_parser.add_argument("-p","--password", type=str, help = "Password", dest = "PASSWORD")
user_create_parser.add_argument("-d","--description", type=str, help = "Description", dest = "DESC")
user_create_parser.add_argument("-f","--firstname", type=str, help = "First Name", dest = "FIRSTNAME")
user_create_parser.add_argument("-l","--lastname", type=str, help = "Last Name", dest = "LASTNAME")
user_create_parser.add_argument("-e","--email", type=str,default = "aa@aa.com", help = "User Email", dest = "EMAIL")
user_create_parser.add_argument("-r","--roles", type=str,default = "", help = "list of role IDs to assign (ex: \"1,3,4\")", dest = "ROLES")

# user delete
def user_delete(args):
    if not args.USERNAME:
        parser.error('You need to pass parameter -u (--username)')

    UsersLogics.delete(args.OUTPUTFORMAT,args.SESSIONNAME,args.USERNAME)

user_delete_parser = user_subparsers.add_parser('delete')
user_delete_parser.set_defaults(func=user_delete)
user_delete_parser.add_argument("-u","--username", type=str, help = "<create & setlogin & delete>: Username (ex: \"linus\") or list of Usernames (ex: \"linus,carly,yli\")", dest = "USERNAME")

# user setlogin
def user_setlogin(args):
    if not args.USERNAME:
        parser.error('You need to pass parameter -u (--username)')
    if not args.LOGINUSER:
        parser.error('You need to pass parameter -n (--loginusername)')
    if not args.LOGINPWD:
        parser.error('You need to pass parameter -w (--loginpassword)')

    UsersLogics.setlogin(args.OUTPUTFORMAT,args.SESSIONNAME,args.USERNAME,args.LOGINUSER,args.LOGINPWD)

user_setlogin_parser = user_subparsers.add_parser('setlogin')
user_setlogin_parser.set_defaults(func=user_setlogin)
user_setlogin_parser.add_argument("-u","--username", type=str, help = "<create & setlogin & delete>: Username (ex: \"linus\") or list of Usernames (ex: \"linus,carly,yli\")", dest = "USERNAME")
user_setlogin_parser.add_argument("-n","--loginusername", type=str,default = "", help = "<setlogin>: OS Login to register under username", dest = "LOGINUSER")
user_setlogin_parser.add_argument("-w","--loginpassword", type=str,default = "", help = "<setlogin>: OS Password to register under username", dest = "LOGINPWD")


#####
# Bot Parser
# bot <list,show,update>
#####

# bot commands
bot_parser = subparsers.add_parser('bot')
bot_subparsers = bot_parser.add_subparsers()

# bot list
def bot_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    ObjectsLogics.bot_list(args.OUTPUTFORMAT,args.SESSIONNAME,args.ObjNameFilter)

bot_list_parser = bot_subparsers.add_parser('list')
bot_list_parser.set_defaults(func=bot_list)
bot_list_parser.add_argument("-l","--name",default = "", help = "Name filter", dest = "ObjNameFilter")


# bot show
def bot_show(args):
    if not args.ObjID:
        parser.error('You need to pass parameter -i (--id) (Object ID to show the definition of)')

    JsonStringOfObjectDef = ObjectsLogics.bot_show(args.OUTPUTFORMAT,args.SESSIONNAME,args.ObjID)
    print(JsonStringOfObjectDef)


bot_show_parser = bot_subparsers.add_parser('show')
bot_show_parser.set_defaults(func=bot_show)
bot_show_parser.add_argument("-i","--id",default = "", help = "Object ID (show & update)", dest = "ObjID")

# bot update
def bot_update(args):
    if not args.ObjID:
        parser.error('You need to pass parameter -i (--id) (Object ID to show the definition of)')
    if not args.UpdatedObjectDef:
        parser.error('You need to pass parameter -d (--def) (JSON definition file for the objects)')

    ObjectsLogics.bot_update(args.OUTPUTFORMAT,args.SESSIONNAME,args.ObjID,args.UpdatedObjectDef)

bot_update_parser = bot_subparsers.add_parser('update')
bot_update_parser.set_defaults(func=bot_update)
bot_update_parser.add_argument("-i","--id",default = "", help = "Object ID (show & update)", dest = "ObjID")
bot_update_parser.add_argument("-d","--def",default = "", help = "Updated Object Definition (as JSON file)", dest = "UpdatedObjectDef")

#####
# WLM Parser
# wlm <list,show>
#####

# WLM commands
wlm_parser = subparsers.add_parser('wlm')
wlm_subparsers = wlm_parser.add_subparsers()

# queue list
def wlm_queue_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    WLMLogics.wlm_queue_list(args.OUTPUTFORMAT,args.SESSIONNAME)

queue_list_parser = wlm_subparsers.add_parser('list')
queue_list_parser.set_defaults(func=wlm_queue_list)
#bot_list_parser.add_argument("-l","--name",default = "", help = "Name filter", dest = "ObjNameFilter")

# queue show
def wlm_queue_show(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.QueueID:
        parser.error('no queue ID passed')
    WLMLogics.wlm_queue_show(args.OUTPUTFORMAT,args.SESSIONNAME,args.QueueID,args.INFOTYPE)

queue_show_parser = wlm_subparsers.add_parser('show')
queue_show_parser.set_defaults(func=wlm_queue_show)
queue_show_parser.add_argument("-i","--id",default = "", help = "Queue ID", dest = "QueueID")
queue_show_parser.add_argument("-t","--type",default = "OWNERS", help = "<MEMBERS,OWNERS,PARTICIPANTS", dest = "INFOTYPE")

# Workitems Command
workitem_parser = subparsers.add_parser('workitem')
workitem_subparsers = workitem_parser.add_subparsers()


# workitem list
def wlm_queue_workitem_list(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.QueueID:
        parser.error('no queue ID passed')
    WLMLogics.wlm_queue_workitem_list(args.OUTPUTFORMAT,args.SESSIONNAME,args.QueueID)

workitem_list_parser = workitem_subparsers.add_parser('list')
workitem_list_parser.set_defaults(func=wlm_queue_workitem_list)
workitem_list_parser.add_argument("-i","--id",default = "", help = "Queue ID", dest = "QueueID")

# workitem add
def wlm_add_workitems(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.QueueID:
        parser.error('no queue ID passed')
    if not args.JSONWorkItems:
        parser.error('You need to pass parameter -w (JSON String of workitems to add)')

    WLMLogics.wlm_add_workitems(args.OUTPUTFORMAT,args.SESSIONNAME,args.QueueID,args.JSONWorkItems)

wi_upload_parser = workitem_subparsers.add_parser('add')
wi_upload_parser.set_defaults(func=wlm_add_workitems)
wi_upload_parser.add_argument("-i","--id",default = "", help = "Queue ID", dest = "QueueID")
wi_upload_parser.add_argument("-w","--workitems",default = "", help = "JSON String of Workitems to add. For example: {'workItems':[{'json': {'firstname': 'Yli','lastname': 'Z','dob': '1111111','membershipnumber': ''}}]}", dest = "JSONWorkItems")

# workitem show
def workitem_show(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.QueueID:
        parser.error('no queue ID passed')
    if not args.WorkitemID:
        parser.error('no workitem ID passed')
    WLMLogics.workitem_show(args.OUTPUTFORMAT,args.SESSIONNAME,args.QueueID,args.WorkitemID)

workitem_show_parser = workitem_subparsers.add_parser('show')
workitem_show_parser.set_defaults(func=workitem_show)
workitem_show_parser.add_argument("-i","--id",default = "", help = "Queue ID", dest = "QueueID")
workitem_show_parser.add_argument("-w","--wiid",default = "", help = "Workitem ID", dest = "WorkitemID")

#workitem_delete
def workitem_delete(args):
    if not args.SESSIONNAME:
        parser.error('no session name passed')
    if not args.QueueID:
        parser.error('no queue ID passed')
    if not args.WorkitemID:
        parser.error('no workitem ID passed')
    WLMLogics.workitem_delete(args.OUTPUTFORMAT,args.SESSIONNAME,args.QueueID,args.WorkitemID)

workitem_delete_parser = workitem_subparsers.add_parser('delete')
workitem_delete_parser.set_defaults(func=workitem_delete)
workitem_delete_parser.add_argument("-i","--id",default = "", help = "Queue ID", dest = "QueueID")
workitem_delete_parser.add_argument("-w","--wiid",default = "", help = "Workitem IDs (comma separated IDs)", dest = "WorkitemID")

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
