'''
bs4に置き換えられないのはjavascriptやらで動的にサイトロードされたり利用規約のポップアップのボタンを押すのに、
seleniumでアクセスする必要があるから。

BeautifulSoupで取得可能の有無
- standfm    O
- YouTube    O
- Spotify    O
- Tver       X (動的に生成されるサイト) → Selenium
- radiotalk  O
- radiko     X (動的に生成されるサイト) → 〃

だいぶ早くなった。体感 1/3 倍くらいの時間になった。
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re

class ChannelScraper:
    def __init__(self, channel_id, wait_time, css_selector, url_start):
        self.channel_id = channel_id
        self.wait_time = wait_time
        self.css_selector = css_selector
        self.url_start = url_start
        self.driver = None

    def quit(self):
        pass

    def click_agree_button(self):
        pass

    def get_latest_episode(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url())
        self.click_agree_button()  
        wait = WebDriverWait(self.driver, self.wait_time)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.css_selector)))
        for element in elements:
            href_value = element.get_attribute('href')
            if href_value and href_value.startswith(self.url_start):
                return href_value

    def base_url(self):
        raise NotImplementedError()

class TverScraper(ChannelScraper):
    def base_url(self):
        return f'https://tver.jp/series/{self.channel_id}'
    
    def click_agree_button(self):
        # "同意する" ボタンのCSSセレクタ
        agree_button_selector = ".terms-modal_buttonWrapper__4PB8Y .terms-modal_done__aJ_4I"
        wait = WebDriverWait(self.driver, self.wait_time)
        agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, agree_button_selector)))
        agree_button.click()

    def quit(self):
        self.driver.quit()

class StandFmScraper(ChannelScraper):   
    def base_url(self):
        return f'https://stand.fm/channels/{self.channel_id}'
         
    def get_latest_episode(self):
            res = requests.get(self.base_url())
            soup = BeautifulSoup(res.text, 'html.parser')
            standfm_links = soup.select('div.css-175oi2r a[href^="/episodes/"]')
            url = f"https://stand.fm{standfm_links[0]['href']}"
            return url

class YouTubeScraper(ChannelScraper):
    def base_url(self):
        return f'https://www.youtube.com/{self.channel_id}/videos'
    
    def get_latest_episode(self):
            res = requests.get(self.base_url())
            soup = BeautifulSoup(res.text, 'html.parser')
            script_contents = str(soup.find_all('script'))
            video_ids = re.findall(r'\"url\":\"(/watch\?v=[^\"]+)\"', script_contents)
            url = f"https://www.youtube.com{video_ids[0]}"
            return url

class SpotifyScraper(ChannelScraper):
    def base_url(self):
        return f'https://open.spotify.com/show/{self.channel_id}'
    
    def get_latest_episode(self):
        res = requests.get(self.base_url())
        soup = BeautifulSoup(res.text, 'html.parser')
        spotify_link = soup.find('meta', {'name': 'music:song'})
        url =spotify_link['content']
        return url

class RadiotalkScraper(ChannelScraper):
    def base_url(self):
        return f'https://radiotalk.jp/program/{self.channel_id}'

    def get_latest_episode(self):
        res = requests.get(self.base_url())
        soup = BeautifulSoup(res.text, 'html.parser')
        radiotalk_link = soup.select_one('div.program-action a.button[href]')
        url = f'https://radiotalk.jp{radiotalk_link["href"]}'
        return url
    
class RadikoScraper(ChannelScraper):
    def base_url(self):
        return f'https://radiko.jp/persons/{self.channel_id}'

    def click_agree_button(self):
        # "同意する" ボタンのCSSセレクタ
        agree_button_selector = ".styles__ModalStyle-sc-1vsew57-0.ivEZfU-button"
        wait = WebDriverWait(self.driver, self.wait_time)
        agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, agree_button_selector)))
        agree_button.click()

    def quit(self):
        self.driver.quit()
