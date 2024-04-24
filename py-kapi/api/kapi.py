import sys
import requests
import json

from Crypto.Hash import SHA256,SHA512

__version__ = "0.0.1"

# This fuction generates the x-kmanga-hash header which is 
# a weird digest of the params and birthday cookies, 
# contact me if you want more informations 
# (the code should be self-explanatory enough...)
def generate_xhash(params, birthday):
    
    birthday_dict = json.loads(birthday)

    hashes = []

    for param in sorted(params):
        
        param_sha256 = SHA256.new()
        param_sha512 = SHA512.new()  

        param_sha256.update(bytes(param,"UTF-8"))
        param_sha512.update(bytes(params[param],"UTF-8"))
        
        hashes.append(param_sha256.hexdigest() + "_" + param_sha512.hexdigest())

    param_hashes = ",".join(hashes)

    param_sha256 = SHA256.new()
    param_sha256.update(bytes(param_hashes,"UTF-8"))

    birthday_sha256 = SHA256.new()
    expires_sha512 = SHA512.new()  

    birthday_sha256.update(bytes(birthday_dict["value"],"UTF-8"))
    expires_sha512.update(bytes(birthday_dict["expires"],"UTF-8"))

    birthday_hash = birthday_sha256.hexdigest() + "_" + expires_sha512.hexdigest()

    xhash_sha512 = SHA512.new()

    xhash_sha512.update(bytes(param_sha256.hexdigest()+birthday_hash,"UTF-8"))

    return  xhash_sha512.hexdigest()


class HTTPClient():

    def __init__(self, username, password, apiHost="api.kmanga.kodansha.com"):
        
        self.version = "6.0.0"
        self.platform = "3"

        self.username = username
        self.password = password

        self.apiHost = apiHost

        self.authenticated = False

        self.headers = {
            "Accept": "*/*",
            "User-Agent": f"py-kapi (https://github.com/al3ks1s/py-kapi {__version__}) Python/{sys.version_info[0]}.{sys.version_info[1]} requests/{requests.__version__}",
            "Accept-Language": "en",
            "Connection": "keep-alive",
            "Host": self.apiHost,
            "DNT": "1",
            "Referer": "https://kmanga.kodansha.com/",
            "Origin": "https://kmanga.kodansha.com/",
        
        }

        # Birthday cookie should be valid until 2100, hope you read this in 2100
        self.cookies = {"birthday": '{"value": "2000-01", "expires": "4102444800"}'}

        self.user_id = "0"

    def __enter__(self):
        self.login()

    def __exit__(self):
        self.logout()

    def login(self):

        url = "https://" + self.apiHost + "/web/user/login"

        payload = {
            "version": self.version,
            "platform": self.platform,
            "email": self.username,
            "password": self.password
        }

        headers = self.headers

        response = requests.post(url, data=payload, headers=headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            
            self.update_cookies(response.cookies.get_dict())
            self.authenticated = True

            account_status = self.get_account_status()

            self.user_id = account_status["account"]["user_id"]

    def logout(self):
        
        url = "https://" + self.apiHost + "/web/user/logout"

        payload = {
            "version": self.version,
            "platform": self.platform,
            "target_user_id": str(self.user_id)
            }

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        response = requests.post(url, data=payload, headers=self.headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            return response.json()

    def get_manga(self, title_id):
        
        url = "https://" + self.apiHost + "/title/list"

        payload = {
            "version": self.version,
            "platform": self.platform,
            "title_id_list": title_id
            }

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        response = requests.get(url, params=payload, headers=self.headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            return response.json()

    def get_chapter(self, episode_id):

        # This endpoint accepts a comma separated list of episodes to fetch, for simplicity's sake, we'll only give a single one

        url = "https://" + self.apiHost + "/episode/list"

        payload = {
            "version": self.version,
            "platform": self.platform,
            "episode_id_list": episode_id
            }

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        response = requests.post(url, data=payload, headers=self.headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            return response.json()

    def get_episode(self, episode_id):
        
        url = "https://" + self.apiHost + "/web/episode/viewver"

        payload = {
            "version": self.version,
            "platform": self.platform,
            "episode_id": episode_id
            }

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        response = requests.get(url, params=payload, headers=self.headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            return response.json()

    def get_account_status(self):
        
        url = "https://" + self.apiHost + "/account"

        payload = {
            "version": self.version,
            "platform": self.platform
            }

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        response = requests.get(url, params=payload, headers=self.headers, cookies=self.cookies)

        if response.status_code == 200 and response.json()["status"] == "success":
            return response.json()


    def update_cookies(self, cookies):
        for cookie in cookies:
            self.cookies[cookie] = cookies[cookie]