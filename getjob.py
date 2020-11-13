#!/usr/bin/env python

"""GetJob, This code is to send mails with different context depending of company info.
:2020 by Ronald Rivera
"""
import csv
from datetime import datetime
from email import message
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re
import json
import ssl
import smtplib
import sys
from time import sleep

class GetJob():
  #load values
  def __init__(self, profile, sms_path, bulk_path, doc_path, *args, **kwargs):
    self.profile = json.load(open(profile))
    self.sms_path = sms_path
    self.bulk_path = bulk_path
    self.doc_path = doc_path
    
  def send(self):
    #print self.profile['name']
    mails_data = self._parse_csv(self.bulk_path)
    for data in mails_data:
      print self._config_mail(data)
      
  def _config_mail(self, data):
    #header format mail
    to = "%s <%s>" % (data[0], data[2])
    sender = "%s <%s>" % (self.profile['name'], self.profile['mail'])
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = self._lang(data[5], data[1])
    message["Bcc"] = to  # Recommended for mass emails
    #Body
    message.attach(MIMEText("hi", "plain"))    
    #PDF file in binary mode
    with open(self.doc_path, "rb") as attach:
      #define mime type
      doc = MIMEBase("application", "octet-stream")
      doc.set_payload(attach.read())
    # Encode to ASCII characters  
    encoders.encode_base64(doc)
    # Add header
    doc.add_header(
      "Content-Disposition",
      "attachment; filename= %s" % self.doc_path,
    )
    #Attach and convert message in string
    message.attach(doc)
    return message.as_string()
  
  def count_recipients(self, bulk_path = None):
    return len(self._parse_csv(bulk_path))
  
  def _lang(self, l, pos):
    if l == "en":
      return "Application for %s" % pos
    else:
      return "Applicacion al trabajo %s" % pos
     
  def _parse_csv(self, bulk_path = None):
    """
    Parse the entires each row csv and return to array
    """  
    if not bulk_path:
      bulk_path = self.bulk_path
    try:
      bulk_file = open(bulk_path, 'rwb')
    except IOError:
      raise IOError("Error csv path")
    bulk_reader = csv.reader(bulk_file, delimiter=',')
    bulk_headlings = next(bulk_reader)
    bulk_list = []
    for i, rowi in enumerate(bulk_reader):
      for j, rowj in enumerate(bulk_headlings):
        bulk_headlings[j] = rowi[j]
      bulk_list.append(bulk_headlings)
    return bulk_list
  
def main(sys_args):
  profile = sys_args[0]
  sms_path = sys_args[1]
  bulk_path = sys_args[2]
  doc_path = sys_args[3]
  if os.path.splitext(profile)[1] != '.json':
    print("The profile argument doesn't seem to contain a valid json file.")
    sys.exit()
    
  if os.path.splitext(bulk_path)[1] != '.csv':
    print("The profile argument doesn't seem to contain a valid json file.")
    sys.exit()  

  try:
    profile, sms_path, bulk_path, doc_path
  except ValueError:
    print("Not enough argumants supplied. GetJob requests 1 option and 3 arguments: ./getjob.py profile sms_path  bulk_path doc_path")
    sys.exit()
  mail = GetJob(profile, sms_path, bulk_path, doc_path)
  mail.send()
  
if __name__ == '__main__':
  main(sys.argv[1:])