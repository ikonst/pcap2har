import urllib.parse

# dpkt.http is buggy, so we use our modified replacement
import dpkt.http
from . import message as http


class Request(http.Message):
    '''
    HTTP request. Parses higher-level info out of dpkt.http.Request
    Members:
    * query: Query string name-value pairs. {string: [string]}
    * host: hostname of server.
    * fullurl: Full URL, with all components.
    * url: Full URL, but without fragments. (that's what HAR wants)
    '''

    def __init__(self, tcpdir, pointer):
        super().__init__(tcpdir, pointer, dpkt.http.Request)
        # get query string. its the URL after the first '?'
        uri = urllib.parse.urlparse(self.msg.uri)
        self.host = self.msg.headers['host'] if 'host' in self.msg.headers else ''
        fullurl = urllib.parse.ParseResult('http', self.host, uri.path, uri.params, uri.query, uri.fragment)
        self.fullurl = fullurl.geturl()
        self.url, frag = urllib.parse.urldefrag(self.fullurl)
        self.query = urllib.parse.parse_qs(uri.query, keep_blank_values=True)
