from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChallengingDOMObjects:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    dynamic_table_elements = "//tbody//tr//td"
    dynamic_table_element = "//td[contains(text(), {})]"

    def find_dynamic_table_element(self, item):
        wait = WebDriverWait(self.driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, ChallengingDOMObjects.dynamic_table_elements))
        )
        # actions = ActionChains(self.driver)

        for element in elements:
            if element.text == item:
                row = element.find_element(By.XPATH, "parent::tr")
                row.find_element(By.XPATH, "//td//a[contains(text(), 'edit')]").click()

        return
