# -*- coding: utf-8 -*-

import base64
import json
import rsa
import time

from .compat import urlencode


class TrimedJSONEncoder(json.JSONEncoder):
    item_separator = ','
    key_separator = ':'


class Signer(object):

    policy_context = {}

    def __init__(self, key_pair_id, key_path, key_format='PEM',
                 hash_method='SHA-1', **kwargs):
        self.key_pair_id = key_pair_id
        with open(key_path, 'rb') as f:
            key_data = f.read()
        self.key = rsa.PrivateKey.load_pkcs1(key_data, key_format)
        self.hash_method = hash_method

    def sign(self, url, **kwargs):
        url, kwargs = self.prepare(url, kwargs)
        policy = self.gen_policy(url, **kwargs)
        polstr = json.dumps(policy, cls=TrimedJSONEncoder)
        polbytes = polstr.encode('utf-8')
        # print(pbytes)
        signature = rsa.sign(polbytes, self.key, self.hash_method)
        # print(signature)
        sigstr = self.b64_encode(signature)
        # print(sigstr)
        params = self.gen_params(url, sigstr, **kwargs)
        parastr = urlencode(params, safe='~')
        # print(parastr)
        signed = '?'.join([url, parastr])
        # print(signed)
        return signed

    def prepare(self, url, kw):
        return url, kw

    def gen_policy(self, url, **kwargs):
        policy = {'Statement': [{'Resource': url}]}
        return policy

    def b64_encode(self, s):
        return base64.b64encode(s) \
            .decode('ascii') \
            .replace('+', '-') \
            .replace('=', '_') \
            .replace('/', '~')

    def gen_params(self, url, signature, **kwargs):
        return {
            'Key-Pair-Id': self.key_pair_id,
            'Signature': signature,
        }


class ExpiringSigner(Signer):

    def __init__(self, key_pair_id, key_path, key_format='PEM',
                 hash_method='SHA-1', expire_seconds=600, **kwargs):
        super(ExpiringSigner, self).__init__(key_pair_id, key_path, key_format,
                                             hash_method, **kwargs)
        self.expire_seconds = expire_seconds

    def prepare(self, url, kwargs):
        url, kwargs = super(ExpiringSigner, self).prepare(url, kwargs)
        kwargs['expired_at'] = int(time.time() + self.expire_seconds)
        return url, kwargs

    def gen_policy(self, url, **kwargs):
        policy = super(ExpiringSigner, self).gen_policy(url, **kwargs)
        for st in policy['Statement']:
            st.setdefault('Condition', {})['DateLessThan'] = {
                'AWS:EpochTime': kwargs.get('expired_at', 0),
            }
        return policy

    def gen_params(self, url, signature, **kwargs):
        params = super(ExpiringSigner, self).gen_params(url, signature, **kwargs)
        params['Expires'] = kwargs.get('expired_at', 0)
        return params