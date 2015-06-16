#!/usr/bin/python

import shlex, subprocess, smtplib, string;

HOST = "mail.bubakov.czf"
SUBJECT = "ALERT: Faulty drive ESXi"
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

command1 = "/opt/hp/hpssacli/bin/hpssacli controller slot=0 physicaldrive all show"
command2 = "grep physicaldrive"
args1 = shlex.split(command1)
args2 = shlex.split(command2)

p1 = subprocess.Popen(args1,stdout=subprocess.PIPE)
p2 = subprocess.Popen(args2,stdin=p1.stdout,stdout=subprocess.PIPE)
data = p2.communicate()[0].splitlines()

#print data[0];
#print data[1];

#data = ['1','2'];

#data[0] = "physicaldrive 1I:0:1 (port 1I:box 0:bay 1, SATA, 1 TB, OK)"
#data[1] = "physicaldrive 1I:0:1 (port 1I:box 0:bay 2, SATA, 1 TB, OK)"


if not "OK" in data[0] or not "OK" in data[1]: mailto(data[0],data[1])