import sys
import requests
import json

from Crypto.Hash import SHA256,SHA512



__version__ = "0.1.0"

# This fuction generates the x-kmanga-hash header which is 
# a weird digest of the params and birthday cookies, 
# contact me if you want more informations 
# (the code should be self-explanatory enough though...)
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


class KAPIClient():

    def __init__(self, username=None, password=None, apiHost="api.kmanga.kodansha.com"):
        
        self.version = "6.0.0"
        self.platform = "3"

        self.username = username
        self.password = password

        self.apiHost = apiHost

        self.authenticated = False

        self.headers = {
            "Accept": "*/*",
            "User-Agent": f"py-kapi {__version__}) Python/{sys.version_info[0]}.{sys.version_info[1]} requests/{requests.__version__}",
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

    def update_cookies(self, cookies):
        for cookie in cookies:
            self.cookies[cookie] = cookies[cookie]

    def request(self, method, endpoint, user_payload):

        url = "https://" + self.apiHost + endpoint

        payload = {
            "version": self.version,
            "platform": self.platform
        }

        for key in user_payload:
            payload[key] = user_payload[key]

        headers = self.headers
        headers["x-kmanga-hash"] = generate_xhash(payload, self.cookies["birthday"])

        if method   == "GET":
            response = requests.get(url, params=payload, headers=self.headers, cookies=self.cookies)
        elif method == "POST":
            response = requests.post(url, data=payload, headers=self.headers, cookies=self.cookies)

        
        if response.status_code == 200 and response.json()["status"] == "success":

            self.update_cookies(response.cookies.get_dict())
            return response.json()
            
        else:

            print("Error : " + str(response.status_code))
            print(response.text)

        
    def login(self):

        payload = {
            "email": self.username,
            "password": self.password
        }

        response = self.request("POST", "/web/user/login", payload)
            
        self.authenticated = True

        account_status = self.get_account()

        self.user_id = account_status["user_id"]

    def logout(self):
        
        payload = {
            "target_user_id": str(self.user_id)
        }

        status = self.request("POST", "/web/user/logout", payload)

        self.authenticated = False
        self.user_id = "0"

        del self.cookies["uwt"]

    def get_title(self, title_id: int):
        
        return self.get_titles([title_id])[0]

        """
        payload = {
            "title_id_list": str(title_id)
        }

        return self.request("GET", "/title/list", payload)["title_list"][0]
        """

    def get_titles(self, title_id_list: [int]):
        
        payload = {
            "title_id_list": ",".join(str(id) for id in title_id_list)
        }

        return self.request("GET", "/title/list", payload)["title_list"]

    # Specific error handling to add to following two funcs : invalid chapter ids will not raise errors from api (Code 200 and success in the json but no episode_list item)
    def get_chapter(self, episode_id: int):

        return self.get_chapters([episode_id])[0]

        """
        payload = {
            "episode_id_list": str(episode_id)
        }

        return self.request("POST", "/episode/list", payload)["episode_list"][0]
        """

    def get_chapters(self, episode_id_list: [int]):

        payload = {
            "episode_id_list": ",".join(str(id) for id in episode_id_list)
        }

        return self.request("POST", "/episode/list", payload)["episode_list"]

    def get_episode(self, episode_id):
        
        payload = {
            "episode_id": str(episode_id)
        }

        return self.request("GET", "/web/episode", payload)["episode"]

    def get_pages(self, episode_id):
        
        payload = {
            "episode_id": str(episode_id)
        }

        response = self.request("GET", "/web/episode/viewer", payload)

        return {"title_id":             response["title_id"], 
                "episode_id":           response["episode_id"],
                "bonus_point":          response["bonus_point"],
                "page_start_position":  response["page_start_position"],
                "direction":            response["direction"],
                "page_slider":          response["page_slider"],
                "scramble_seed":        response["scramble_seed"],
                "page_list":            response["page_list"]
            }
        
    
    def get_account(self):
        
        payload = {}

        return self.request("GET", "/account", payload)["account"]

    # Returns points *and* ticket data
    def get_account_points(self):

        payload = {}

        response = self.request("GET", "/account/point", payload)

        return { "point": response["point"], "ticket": response["ticket"]}

    def get_user(self):
        
        payload = {
            "user_id": str(self.user_id)
        }

        response = self.request("GET", "/user", payload)

        del response["status"]
        del response["response_code"]
        del response["error_message"]

        return response 

    def get_genre_list(self):

        payload = {}

        return self.request("GET", "/genre/search/list", payload)["genre_list"]

    def get_genre_list_by_id(self, genre_id_list: [int]):

        payload = {
            "genre_id_list": ",".join(str(id) for id in genre_id_list)
        }

        return self.request("GET", "/genre/list", payload)["genre_list"]
        
    # Ranking id is one of the genres taken from the responses above
    def get_rankings_all(self, ranking_id, offset = 0, limit = 0):

        payload = {
            "ranking_id": str(ranking_id)
        }

        if offset:
            payload["offset"] = str(offset)
        
        if limit:
            payload["limit"] = str(limit)

        response = self.request("GET", "/ranking/all", payload)

        return { "tab_list": response["tab_list"], "ranking_title_list": response["ranking_title_list"]}


    def get_web_ranking(self):

        payload = {}

        return self.request("GET", "/web/ranking/genre", payload)["genre_ranking_list"]

    def get_web_banner(self):

        payload = {}

        response = self.request("GET", "/web/top", payload)

        return { "banner_list": response["banner_list"], "today_title_list": response["today_title_list"] }

    def get_purchased(self, offset = 0, limit = 0):

        payload = {}

        if offset:
            payload["offset"] = str(offset)
        
        if limit:
            payload["limit"] = str(limit)

        return self.request("GET", "/web/title/purchased", payload)["title_list"]

    def get_title_ticket_list(self, title_id):

        return self.get_title_ticket_list([title_id])[0]

    def get_title_ticket_list(self, title_id_list):

        payload = {
            "title_id_list": ",".join(str(title_id) for title_id in title_id_list)
        }
        
        return self.request("GET", "/title/ticket/list", payload)["title_ticket_list"]

    def get_title_supplement(self, title_id: int):

        payload = {
            "title_id": str(title_id)
        }
        

        response =  self.request("GET", "/title/supplement", payload)

        del response["status"]
        del response["response_code"]
        del response["error_message"]

        return response

    def get_point_subscription(self):
        
        payload = {}

        response =  self.request("GET", "/shop/point/subscription", payload)

        return { "point_subscription_asset_list": response["point_subscription_asset_list"], 
                    "subscribed_category_list": response["subscribed_category_list"] 
                    }

    def get_loginbonus(self):

        payload = {}

        return self.request("GET", "/loginbonus", payload)["loginbonus_list"]

    def buy_episode(self, episode_id: int):

        payload = {
            "episode_id": str(episode_id)
        }

        payload["check_point"] = self.get_chapter(episode_id)["point"]

        response = self.request("POST", "/episode/paid", payload)

        return { "account_point": response["account_point"], 
                    "paid_point": response["paid_point"] }

    def rent_episode(self, episode_id):

        payload = {
            "episode_id": str(episode_id),
            "ticket_type": "1",
            "ticket_version": "1"
        }

        return self.request("POST", "/episode/rental/ticket", payload)

    def finish_reading_episode(self, episode_id):

        payload = {
            "episode_id": str(episode_id)
        }

        response = self.request("GET", "/episode/viewer/finish", payload)

        del response["status"]
        del response["response_code"]
        del response["error_message"]

        return response

    def get_last_page(self, episode_id):

        payload = {
            "episode_id": str(episode_id)
        }

        # Never seen any other response than []
        return self.request("GET", "/episode/viewer/lastpage", payload)["descriptor_id_list"]

    def app_boot(self):

        payload = {}

        response = self.request("GET", "/app/boot", payload)

        del response["status"]
        del response["response_code"]
        del response["error_message"]
        
        return response


"""
Endpoint yet to implement, most of them would be useless in your projects:
https://api.kmanga.kodansha.com/advertisement/view

There are probably other endpoints i haven't discovered yet, if you found one missing, open an issue or a PR for it to be included
"""