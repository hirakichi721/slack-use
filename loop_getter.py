#!/usr/bin/python3

#
# loop_getter.py
# 2021.7.8
# by Hirakichi
#   For my convenient future, I want to create any comfortable codes.
#

#
# Requirement: Python3
# 
# Pre-requirement
# 0. pip3 install requests --user
# 1. Create apps
#   Refer to: https://kishaku-kangen.blogspot.com/2020/07/slackapilegacy-token-slackchannels.html
# 2. Execute this program via "python3"
#

import requests
import json
import time
import subprocess
import os
import sys
import datetime

## -----------------------------------------------------------------------
# Set PARAMETERS before executing 
## -----------------------------------------------------------------------
# Bot Token
bottoken = "{{ Your Bot Token }}"
# Channel ID you can get from the channel url link
channelID = "{{ Your Channel ID }}"
# Maximum number of messages to get at a time.(If the message updated more then GET_MESSAGE_NUM, you miss some messages.)
GET_MESSAGE_NUM=10 
# Sleep Time among next slack message getting.
SLEEP_TIME=10  # (sec)
# Syslog Tag
SYSLOG_TAG = "{{ Tag for syslog }}"
# Output File Directory
OutputFileDir = "/home/slacker/slackget/logs/"
## -----------------------------------------------------------------------

# API Reference for conversations.history
#  https://api.slack.com/methods/conversations.history
# API URL
url = "https://slack.com/api/conversations.history"

header={
    "Authorization": "Bearer {}".format(bottoken)
}

payload  = {
    "channel" : channelID,
    "limit": GET_MESSAGE_NUM,
    }

if not os.path.isdir(OutputFileDir):
  os.makedirs(OutputFileDir)
if not os.path.isdir(OutputFileDir):
  print("[ERROR] Cannot create temporary directory " + OutputFileDir)
  sys.exit(0)

OutputFile = OutputFileDir+"slack-tmp.log"

def send_to_syslog(queue):
  messages = ""
  for i in range(0,len(queue)):
    messages=messages+queue[i]+"\n"
  # Remove a file sent
  if os.path.isfile(OutputFile):
    if os.path.getsize(OutputFile)==0:
      os.remove(OutputFile)
    else:
      os.rename(OutputFile, OutputFile+datetime.datetime.now().strftime('.%Y%m%d-%H%M%S'))
  # Write to a file newly send
  with open(OutputFile,"a") as fw:
    fw.write(messages)
  # loggerOutputTest
  subprocess.call("logger -f " + OutputFile + " -t "+SYSLOG_TAG,shell=True)

latest_ts=0
msgqueue=[] # 0=>oldest
while True:
  msgqueue=[]
  res = requests.get(url, headers=header, params=payload)
  js=res.json()
  for i in reversed(range(0,len(js["messages"]))):
    if latest_ts==0 or latest_ts<float(js["messages"][i]["ts"]):
      text=js["messages"][i]["text"]
      msgqueue.append(text)
  latest_ts = float(js["messages"][0]["ts"])
  send_to_syslog(msgqueue)
  time.sleep(SLEEP_TIME)
