from urllib.parse import quote, urlparse
import httplib2
import time
import hashlib, hmac
import base64

class Amazon:
    
    def __init__(self
                 , cache_dir
                 , secret_key
                 , url
                 , Version
                 , AWSAccessKeyId
                 , AssociateTag
                 , Service
                 , Operation
                 , **default_req_params):
        self.__h = httplib2.Http(cache_dir) 
        self.__secret_key = secret_key
        self.__amazon_url = url;
        self.__default_req_params = {'Version': Version
                                   , 'AWSAccessKeyId': AWSAccessKeyId
                                   , 'AssociateTag': AssociateTag
                                   , 'Service': Service
                                   , 'Operation': Operation}
        self.__default_req_params.update(default_req_params)

    def request(self, **req_params):
        return self.__h.request(self.get_request_url(**req_params))

    def get_request_url(self, **req_params):
        return self.__build_url(dict(self.__default_req_params, **req_params))

    def __build_url(self, req_params):
        req_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        req_param_str = '&'.join((k + "=" + quote(req_params[k].encode('utf-8'),safe='~'))
                                  for k in sorted(req_params.keys()))
        uo = urlparse(self.__amazon_url)
        signature = quote(base64.b64encode(hmac.new(self.__secret_key.encode('ascii')
                                           , ("GET\n" + uo.netloc + "\n" + uo.path
                                           + "\n" + req_param_str).encode('ascii')
                                           , hashlib.sha256).digest()))
        url = self.__amazon_url + "?" + req_param_str + "&Signature=" + signature 
        return url

