#!/usr/bin/env python
# -*- coding: utf-8 -*-
## - HTTpoke
## - kaizoku@phear.cc
## Tests the given webserver for enabled HTTP methods

import sys
import optparse
import httplib

class Probe(object):
    def __init__(self, server, port=None, ssl=None):
        self.server = server
        self.port = port or (443 if ssl else 80)
        self.ssl = ssl

    def getconn(self):
        if self.ssl:
            c = httplib.HTTPSConnection(self.server, self.port, timeout=10)
        else:
            c = httplib.HTTPConnection(self.server, self.port, timeout=10)
        return c

    def request(self, method, path, body=None, headers=None):
        c = self.getconn()
        headers = headers or {}
        c.request(method, path, body, headers=headers)
        return c.getresponse()

    def test(self):
        results = {}
        try:
            results["TRACE"] = "Success" if self.trace() else "Failed"
            results["PUT"] = "Success" if self.put() else "Failed"
            results["DELETE"] = "Success" if self.delete() else "Failed"
        except Exception, e:
            print "Connection failed: %s" % (e,)
        else:
            print "Domain: %s" % (self.server,)
            for test, result in results.iteritems():
                print "%s:\t%s" % (test, result)

    def trace(self):
        r = self.request("TRACE", "/", headers={"Abcd":"efghij"})
        body = r.read()
        if "Abcd" in body or r.status == httplib.OK:
            return True
        else:
            return False

    def put(self):
        r = self.request("PUT", "/blah", "KEHKEHEKEHKEH")
        if r.status in (httplib.OK, httplib.CREATED, httplib.NO_CONTENT):
            return True
        else:
            return False

    def delete(self):
        r = self.request("DELETE", "/blah")
        if r.status in (httplib.OK, httplib.ACCEPTED, httplib.NO_CONTENT):
            return True
        else:
            return False


if __name__ == "__main__":
    parser = optparse.OptionParser(version="%prog 0.1",
        usage="%prog [-p <port>] [-s|--ssl] <webserver>")
    parser.add_option("-p", "--port", help="server port", action="store",
        type="int", dest="port", default=80)
    parser.add_option("-s", "--ssl", help="enable SSL", action="store_true",
        dest="ssl", default=False)
    options, args = parser.parse_args()

    if not args:
        parser.error("Must include at least one web server to test")

    for server in args:
        if server.find(":") != -1:
            server, port = server.split(":")
        else:
            port = options.port
        p = Probe(server, port, options.ssl)
        p.test()
