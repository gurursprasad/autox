from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePageObjects:
    def __init__(self, driver):
        self.driver = driver

    challenging_dom = "//a[contains(text(), 'Challenging DOM')]"
    frames = "//a[contains(text(), 'Frames')]"

    def click_challenging_dom(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, HomePageObjects.challenging_dom))).click()
        return

    def click_frames(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, HomePageObjects.frames))).click()
        return
