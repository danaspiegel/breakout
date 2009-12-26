#!/usr/bin/python

""" Twitter api class.
See http://apiwiki.twitter.com/REST+API+Documentation for api docs

In short, converts 'method_action' to 'http://twitter.com/method/action.json'
using the magic of __getattr__. Believe it!

Basic usage:
import pytwitter
twitter = pytwitter.pytwitter(username='username', password='password')
# Update status
twitter.statuses_update(status="<3 TWITTER!!1!")
# Follow biz
twitter.friendships_create(id="biz")

... and so on.

Unless an exception is raised, full output is returned in the requested format
Default: json.
"""

import re
import urllib
import urllib2

__author__ = 'nsheridan@gmail.com (Niall Sheridan)'
__license__ = 'Apache License 2.0'
__copyright__ = 'Copyright 2008, Niall Sheridan'

class TwitterError(Exception):
  """ TwitterError exception
  Raised when the server returns something unexpected
  """
  def __init__(self, code, error):
    self.code = code
    self.error = error

  def __str__(self):
    return 'Error %s: %s' % (self.code, self.error)


class pytwitter:
  """ Twitter client:
  username:: twitter username
  password:: twitter account password
  url (optional):: alternate api url (ex. http://identi.ca/api)

  Methods are converted to corresponding api urls so that:
    pytwitter.statuses_update(status='abcdef', format='json')
  becomes:
    http://twitter.com/statuses/update.json?status=abcdef
  """
  def __init__(self, username=None, password=None, url='http://twitter.com'):
    self.url = url
    self.username = username
    self.password = password

  def __getattr__(self, method):
    def method(_self=self, _method=method, **params):
      """ Dynamic api method constructor
      Args: A valid twitter method
      Returns: Output from the server in the requested format (e.g. json)
      """
      # Normal case: the method 'category_method()' is converted to
      # category/method.format e.g. 'statuses_update' => 'statuses/update.json'
      # Exception cases: methods that have a '_' in the category and
      # cannot be directly translated and have to be handled differently.
      exception_methods = ('direct_messages', 'saved_searches', 'report_spam')
      regex = r'(%s)_(.+)$'
      for exc in exception_methods:
        if exc in _method:
          regex %= exc
          _method = re.sub(regex, r'\1/\2', _method)
          break
      else:
        # Everything else.
        _method = _method.replace('_', '/', 1)

      # Set the format. Fallback to json.
      # format='' implies no format requested (for e.g. oauth methods)
      if params.has_key('format'):
        if params['format'] == '':
          req_format = ''
        else:
          req_format = ''.join(['.', params['format']])
        params.pop('format')
      else:
        req_format = '.json'
      req_method = ''.join([_method, req_format])
      url = '/'.join([_self.url.strip('/'), req_method])
      for key in params.keys():
        params[key] = str(params[key])
      params = urllib.urlencode(params)
      resp = _self._send_data(url, params)
      return resp
    return method

  def _send_data(self, url, data):
    """ Authenticates with the server
    Sends the request and returns a response in the requested format (e.g json)
    Raises TwitterError exception on urllib2.UrlError
    """
    pwdmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pwdmanager.add_password(
        None, self.url, self.username, self.password)
    opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(pwdmanager))
    # Try a POST first
    req = urllib2.Request(url, data)
    try:
      resp = opener.open(req).read()
      return resp
    except urllib2.URLError, error:
      if error.code == 400:
        # This probably means that the wrong request type was used.
        # Twitter should be returning a HTTP 405 in that case, but it doesn't.
        # Potentially throw away real errors and reissue the request using GET.
        url = ''.join([url, '?', data])
        req = urllib2.Request(url)
        try:
          resp = opener.open(req).read()
          return resp
        except urllib2.URLError, error:
          raise TwitterError(error.code, error.read())
      else:
        raise TwitterError(error.code, error.read())


def main():
  """ Test client """
  twitter = pytwitter()
  print twitter.help_test()
  search_client = pytwitter(url='http://search.twitter.com')
  print search_client.search(q='twitter', format='rss')
  # This one fails with a 401 but should at least get the url correct
  print twitter.oauth_request_token(format='')

if __name__ == '__main__':
  main()
