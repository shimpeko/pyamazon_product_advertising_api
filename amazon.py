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
                 , version
                 , access_key
                 , associate_tag
                 , service
                 , operation
                 , **default_req_params):
        self.__secret_key = secret_key
        self.__h = httplib2.Http(cache_dir) 
        self.__amazon_url = url;
        self.__default_req_params = {'Version': version
                                   , 'AWSAccessKeyId': access_key
                                   , 'AssociateTag': associate_tag
                                   , 'Service': service
                                   , 'Operation': operation}
        self.__default_req_params.update(default_req_params)

    def request(self, **req_params):
        return self.__h.request(self.get_request_url(**req_params))

    def get_request_url(self, **req_params):
        req_params = self.__build_req_params(**req_params)
        return self.__build_url(req_params)

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

    def __build_req_params(self, **req_params):
        return dict(self.__default_req_params, **req_params)

