#!/usr/bin/python

import shlex, subprocess, smtplib, string;

HOST = "mail.bubakov.czf"
SUBJECT = "ALERT: Faulty drive ESXi2"
TO = "buh@bubakov.net"
FROM = "buh@bubakov.net"

def mailto(disk1, disk2):

	BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        disk1,
        disk2,
        ), "\r\n")
	server = smtplib.SMTP(HOST)
	server.sendmail(FROM, [TO], BODY)
	server.quit()

command1 = "/usr/src/RemoteArcconf/arcconf GETCONFIG 1"
command2 = "grep '  State'"
args1 = shlex.split(command1)
args2 = shlex.split(command2)

p1 = subprocess.Popen(args1,stdout=subprocess.PIPE)
p2 = subprocess.Popen(args2,stdin=p1.stdout,stdout=subprocess.PIPE)
data = p2.communicate()[0].splitlines()

#print data[0];
#print data[1];

#data = ['1','2'];

#data[0] = "State                              : Online"
#data[1] = "State                              : Offline"


if not "Online" in data[0] or not "Online" in data[1]: mailto(data[0],data[1])