#!/usr/bin/env python
#coding=utf-8
#script name check_web.py
import socket
import re
import sys
import os
import json
import requests

def check_webserver(address, port, resource):
    #建立http请求串
    if not resource.startswith('/'):
        resource = '/' + resource
    request_string = "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (resource, address)
    #创建一个tcpsocket
    s = socket.socket()
    try:
        s.connect((address, port))
        s.send(request_string)
        #获取前100字节
        rsp = s.recv(100)
    except socket.error,e:
        return False
    finally:
        s.close()
    lines = rsp.splitlines()
    try:
        version, status, message = re.split(r'\s+', lines[0], 2)
    except ValueError:
        return False
    return status
if __name__ == '__main__':
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("-a", "--address", dest="address", default='localhost',
    #                   help="ADDRESS for webserver", metavar="ADDRESS")
    # parser.add_option("-p", "--port", dest="port", type="int", default=80,
    #                   help="PORT for webserver",metavar="PORT")
    # parser.add_option("-r", "--resource", dest="resource",default="index.html",
    #                   help="RESOURCE to check", metavar="RESOURCE")
    # (options, args) = parser.parse_args()
    # print "options: %s, args: %s" % (options, args)
    if not os.path.exists('./weblist.txt'):
        print "The checked weblist file not exist,Please check!"
        sys.exit(1)
    fe = open('./weblist.txt')
    weblines = fe.readlines()
    fe.close()
    data = {}
    data['content'] = {}
    for web in weblines:
        web = web.strip('\n')
        web = web.split(' ')
        if web[0].startswith("#"):
            continue
        webinfo={}
        # check_webserver(options.address, options.port=80, options.resource='/')
        status = check_webserver(web[0], port = 80, resource = web[1])
        if not status:
            webinfo['url'] = web[0]
            webinfo['status'] = status
            data['content'] = webinfo
        elif  int(status)>400:
            webinfo['url'] = web[0]
            webinfo['status'] = status
            data['content'] = webinfo
    if data['content']:
        import urllib2
        import urllib
        url="http://monitor.putao.com/index.php"
        postdata = urllib.urlencode(data)
        request = urllib2.Request(url, postdata)
        response = urllib2.urlopen(request)
        sys.exit(not response)




