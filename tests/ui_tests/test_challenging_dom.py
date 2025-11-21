from autox.autox_logger import logger
from page_objects.challenging_dom_objects import ChallengingDOMObjects
from page_objects.home_page_objects import HomePageObjects


class Test_ChallengingDOM:
    def test_challenging_dom_is_loaded(self, setup_driver):
        home_page_objects = HomePageObjects(self.driver)
        home_page_objects.click_challenging_dom()
        logger.info("Clicked Challenging DOM")
        url = self.driver.current_url
        assert "/challenging_dom" in url
        logger.info(f"/challenging_dom is in {url}")

    def test_click_edit_for_any_element(self):
        rand_element = "Adipisci3"
        challenging_dom_objects = ChallengingDOMObjects(self.driver)
        challenging_dom_objects.find_dynamic_table_element(rand_element)
        logger.info(f"Found the element: {rand_element}")
        url = self.driver.current_url
        assert "#edit" in url
        logger.info(f"#edit is in {url}")
