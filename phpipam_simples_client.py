import requests
import json


requests.packages.urllib3.disable_warnings()


class Ipam:
    def __init__(self, url, appid, username, password, token=None, ssl_verify=False):
        self.url = url
        self.appid = appid
        self.username = username
        self.password = password
        self.baseurl = f"{self.url}/api/{self.appid}"
        self.token = token
        self.headers = {'token': self.token}
        self.ssl_verify = ssl_verify
        self.login()

    def __api_send_request(self, endpoint, method='GET', params=None):
        req = requests.request(
            method=method,
            url=self.baseurl + endpoint,
            params=params,
            verify=self.ssl_verify, 
            headers=self.headers
        )
        return json.loads(req.text)['data']

    def login(self):
        req = requests.post(self.baseurl + '/user/', verify=self.ssl_verify, auth=(self.username, self.password))
        self.token = json.loads(req.text)['data']['token']
        self.headers['token'] = self.token
        return json.loads(req.text)['data']['expires']
        
    def get_address_first_free(self, subnetId):
        params = {'subnetId': subnetId}
        req = self.__api_send_request(endpoint='/addresses/first_free/', params=params)
        return req
    
    def add_address_first_free(self, subnetId, hostname, ticket):
        params = {'subnetId': subnetId, 'hostname': hostname, 'description': ticket}
        req = self.__api_send_request(endpoint='/addresses/first_free/', params=params, method='POST')
        return req


# Info subnet
#res = requests.get(baseurl + '/subnets/', params={'id': '456'}, verify=False, headers={'token': token})
#print(json.dumps(json.loads(res.text), indent=4))
#
## Info IP 
#res = requests.get(baseurl + '/addresses/tags/', params={'id': '623'}, verify=False, headers={'token': token})
#print(json.dumps(json.loads(res.text), indent=4))
#
## Info subnet 
#res = requests.get(baseurl + '/subnets/cidr/10.50.0.0/22', verify=False, headers={'token': token})
#print(json.dumps(json.loads(res.text), indent=4))
