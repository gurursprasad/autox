from autox.autox_logger import logger
from page_objects.frames_objects import FramesObjects
from page_objects.home_page_objects import HomePageObjects


class Test_Frames:
    def test_frames_is_loaded(self, setup_driver):
        home_page_objects = HomePageObjects(self.driver)
        home_page_objects.click_frames()
        logger.info("Clicked Frames")
        assert "/frames-wrong" in self.driver.current_url

    def test_nested_frames_is_loaded(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_nested_frames()
        logger.info("Clicked Nested Frames")
        assert "/nested_frames" in self.driver.current_url

    def test_i_frames_is_loaded(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        self.driver.back()
        assert "/frames" in self.driver.current_url
        logger.info(f"/frames present in url: {self.driver.current_url}")
        frames_objects.click_i_frames()
        logger.info("Clicked iFrames")
        assert "/iframe" in self.driver.current_url
        logger.info(f"/iframes present in url: {self.driver.current_url}")
        self.driver.back()

    def test_nested_frames(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_nested_frames()
        logger.info("Clicked Nested Frames")
        assert "/nested_frames" in self.driver.current_url
        logger.info(f"/nested_frames present in url: {self.driver.current_url}")
        frames_objects.switch_to_frame("frame-top")
        logger.info("Switched to Frame")
        frames_objects.validate_frameset()
        logger.info("Validated Frameset")
        # frames_objects.switch_to_default_content()
        self.driver.back()

    def test_i_frames(self, setup_driver):
        frames_objects = FramesObjects(self.driver)
        frames_objects.click_i_frames()
        logger.info("Clicked iFrames")
        assert "/iframe" in self.driver.current_url
        logger.info(f"/frames present in url: {self.driver.current_url}")
        frames_objects.switch_to_frame("mce_0_ifr")
        editor = self.driver.find_element("id", "tinymce")
        # Use JavaScript to set content in TinyMCE editor
        test_message = "This is a test message"
        self.driver.execute_script(f"arguments[0].innerHTML = '{test_message}'", editor)
        # Verify content was set
        content = self.driver.execute_script("return arguments[0].innerHTML", editor)
        assert test_message in content
        frames_objects.switch_to_default_content()
        logger.info("Switched to default content")
