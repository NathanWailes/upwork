#! /usr/bin/env python

import hashlib
import urllib
import pickle
import time


try:
    import json
except ImportError:
    import simplejson as json


class Mixpanel(object):
    VERSION = '2.0'

    def __init__(self, api_key, api_secret, endpoint):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint

    def request(self, params, output_filepath):
        params['api_key'] = self.api_key
        params['expire'] = int(time.time()) + 600  # Grant this request 10 minutes.

        if 'sig' in params: del params['sig']
        params['sig'] = self.hash_args(params)

        request_url = self.endpoint + '/?' + self.unicode_urlencode(params)

        print request_url

        urllib.urlretrieve(request_url, output_filepath)

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def hash_args(self, args, secret=None):
        """
            Hashes arguments by joining key=value pairs, appending a secret, and
            then taking the MD5 hex digest.
        """
        for a in args:
            if isinstance(args[a], list): args[a] = json.dumps(args[a])

        args_joined = ''
        for a in sorted(args.keys()):
            if isinstance(a, unicode):
                args_joined += a.encode('utf-8')
            else:
                args_joined += str(a)

            args_joined += '='

            if isinstance(args[a], unicode):
                args_joined += args[a].encode('utf-8')
            else:
                args_joined += str(args[a])

        hash = hashlib.md5(args_joined)
        print args_joined

        if secret:
            hash.update(secret)
        elif self.api_secret:
            hash.update(self.api_secret)
        return hash.hexdigest()
