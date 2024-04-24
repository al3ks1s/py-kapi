


class Chapter():

    def __init__(self):
        self.title_id: int

        self.episode_id: int
        self.episode_name: str

        self.index: int
        self.start_time: str
        
        self.is_viewed : int
        self.is_viewed_last_page: int
        
        self.thumbnail_image_url: str
        self.web_thumbnail_image_url: str
        
        self.badge: int
        
        self.rental_finish_time: str
        self.rental_rest_time: str
        
        self.point: int
        self.bonus_point: int
        
        self.use_status: int
        
        self.featured_text: str
        self.first_page_image_url: str

        self.magazine_id: int
        self.magazine_name: str

        self.viewing_direction: int
        self.ticket_rental_enabled: int
        
        self.comic_volume: str
        self.short_introduction_text: str

        self.view_bulk_buy: int
        self.comment_num: int
        self.single_sale_enabled: int

    class Episode():

        def __init__(self, title_id: int):

            self.scramble_seed: int
            self.page_list: [str]
            self.previous_episode: {title_id: int, episode_id: int, age_rating: str}
            self.next_episode: {title_id: int, episode_id: int, age_rating: str}
            self.age_rating: str

