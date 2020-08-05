import requests
import json
import argparse

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
        if method == 'DELETE':
            return json.loads(req.text)['message']
        else:
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

    def get_subnet(self, subnet):
        req = self.__api_send_request(endpoint=f'/subnets/cidr/{subnet}')
        return req[0]['id']

    def del_address(self, address, subnetId):
        req = self.__api_send_request(endpoint=f'/addresses/{address}/{subnetId}/', method='DELETE')
        return req


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adiciona ou remove reserva de IP no Ipam", epilog="by FF")
    parser.version = '1.0'
    parser.add_argument("--user", type=str, required=True)
    parser.add_argument("--password", type=str, required=True)
    parser.add_argument("--subnetid", type=str, required=True)
    parser.add_argument("--action", choices=['add', 'del'], required=True)
    parser.add_argument("--ipaddress", type=str, metavar='192.168.144.120')
    parser.add_argument("--hostname", type=str)
    parser.add_argument("--description", type=str)
    parser.add_argument("-v", action='version')
    args = parser.parse_args()
    ipam = Ipam('https://ipam.local.domain', 'robot', args.user, args.password)
    ipam.login()
    if args.action == 'add':
        if args.description and args.hostname:
            resultIP = ipam.add_address_first_free(args.subnetid, args.hostname, args.description)
            print(resultIP)
        else:
            print("Error: the following arguments are required: --hostname, --description")
    else:
        if args.ipaddress:
            resultIP = ipam.del_address(args.ipaddress, args.subnetid)
            print(resultIP)
        else:
            print("Error: the following arguments are required: --ipaddress")
