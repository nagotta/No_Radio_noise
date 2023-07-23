from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChannelScraper:
    def __init__(self, channel_id, wait_time, css_selector, url_start):
        self.channel_id = channel_id
        self.wait_time = wait_time
        self.css_selector = css_selector
        self.url_start = url_start
        self.driver = webdriver.Chrome()

    def quit(self):
        self.driver.quit()

    def click_agree_button(self):
        pass

    def get_latest_episode(self):
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

class StandFmScraper(ChannelScraper):
    def base_url(self):
        return f'https://stand.fm/channels/{self.channel_id}'

class YouTubeScraper(ChannelScraper):
    def base_url(self):
        return f'https://www.youtube.com/{self.channel_id}/videos'

class SpotifyScraper(ChannelScraper):
    def base_url(self):
        return f'https://open.spotify.com/show/{self.channel_id}'
    
class RadiotalkScraper(ChannelScraper):
    def base_url(self):
        return f'https://radiotalk.jp/program/{self.channel_id}'
    
class RadikoScraper(ChannelScraper):
    def base_url(self):
        return f'https://radiko.jp/persons/{self.channel_id}'

    def click_agree_button(self):
        # "同意する" ボタンのCSSセレクタ
        agree_button_selector = ".styles__ModalStyle-sc-1vsew57-0.ivEZfU-button"
        wait = WebDriverWait(self.driver, self.wait_time)
        agree_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, agree_button_selector)))
        agree_button.click()
