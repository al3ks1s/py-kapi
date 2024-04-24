

class Account():

    def __init__(self):

        self.account_id: int

        self.is_registered: int
        self.user_id: int       # user_id is different than account_id, for some reasons

        self.nickname: str
        self.email: str

        self.gender: str
        self.birthyear: int

        self.device_list: []

        self.days_since_create: int

        self.inflow_type: int

        self.return_date: str

        self.icon_id: int

        self.icon_name: str

        self.icon_image_url: str

        self.terms_of_service: {id: int, is_accept: int, url: str}

        self.privacy_policy: {id: int, is_accept: int, url: str}