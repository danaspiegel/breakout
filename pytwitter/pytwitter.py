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
__license__ = 'Python'
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
      Takes: A valid twitter method
      Returns: Output from the server in the requested format (e.g. json)
      """
      # Some methods are POST only. Default to sending a GET.
      use_post = False
      post_only_methods = ('statuses_update', 'statuses_delete',
          'account_end_session', 'friendships_destroy', 'friendships_create',
          'direct_messages_destroy', 'direct_messages_new',
          'account_update_delivery_service', 'account_update_profile_colors',
          'account_update_profile_image', 'favorites_create',
          'account_update_profile_background_image', 'account_update_profile',
          'notifications_follow', 'notifications_leave', 'blocks_create',
          'blocks_destroy', 'favorites_destroy', 'oauth_access_token',
          'saved_searches_destroy', 'saved_searches_create')
      if _method in post_only_methods:
        use_post = True
      # Exception case for 'direct_messages' and 'saved_searches'
      # Can't just replace('_', '/') for this one
      if 'direct_messages' in _method:
        # _method should look like one of:
        #  direct_messages.format
        #  direct_messages/method.format
        _method = re.sub(r'^(direct_messages)_(.+)$', r'\1/\2', _method)
      elif 'saved_searches' in _method:
        #  saved_searches.format
        #  saved_searches/method.format
        _method = re.sub(r'^(saved_searches)_(.+)$', r'\1/\2', _method)
      else:
        # Everything else.
        _method = _method.replace('_', '/', 1)
      # Set the format. Fallback to json.
      # format='' implies no format requested (for e.g. oauth methods)
      if params.has_key('format'):
        if params['format'] == '':
          format = ''
        else:
          format = '.%s' % params['format']
        del params['format']
      else:
        format = '.json'
      url = '%s/%s%s' % (_self.url, _method, format)
      for key in params.keys():
        params[key] = str(params[key])
      params = urllib.urlencode(params)
      resp = _self._send_data(url, params, use_post)
      return resp
    return method

  def _send_data(self, url, data, use_post=False):
    """ Authenticates with the server
    Sends the request and returns a response in the requested format (e.g json)
    Raises TwitterError exception on urllib2.UrlError
    """
    try:
      pwdmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
      pwdmanager.add_password(
          None, self.url, self.username, self.password)
      opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(pwdmanager))
      if use_post:
        req = urllib2.Request(url, data)
      else:
        url = '%s?%s' % (url, data)
        req = urllib2.Request(url)
      resp = opener.open(req).read()
      try:
        return resp
      except:
        return None
    except urllib2.URLError, error:
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
