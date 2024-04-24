

class Manga():

    def __init__(self):

        self.title_id: int
        self.title_name: str

        self.banner_image_url: str
        self.thumbnail_image_url: str
        self.thumbnail_rect_image_url: str
        self.feature_image_url: str

        self.campaign_text: str
        self.notice_text: str
        
        self.next_updated_text: str
        
        self.comic_text: str

        self.author_text: str
        self.introduction_text: str
        self.short_introduction_text: str
        
        self.free_episode_update_cycle_text: str
        self.new_episode_update_cycle_text: str

        self.episode_order: int
        self.favorite_display: int
        self.support_display: int
        self.first_episode_id: int

        self.magazine_category: int
        self.publish_category: int

        self.last_read_episode_id: int
        self.next_read_episode_id: int

        self.favorite_status: int
        self.support_status: int

        self.title_ticket_enabled: int
    
        self.first_comic_id: int
        self.last_read_comic_id: int
        self.next_read_comic_id: int

        self.genre_id_list: [int]

        self.favorite_score: int
        self.support_score: int

        self.episode_free_updated: str
        self.free_episode_count: int

        self.latest_paid_episode_id: [int]
        self.latest_free_episode_id: int

        self.total_episode_count: int

        self.free_comic_count: int
        self.latest_comic_published_date: str
        self.latest_comic_id: [int]
        self.total_comic_count: int

        self.community_id: str

        self.episode_id_list: [int]

        self.title_share_ret: {title_name: str, twitter_post_text: str, url: str}

        self.author_list: [str]






