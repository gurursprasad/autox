from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from autox.utilities.common_utils import assert_with_log
from autox.autox_logger import logger


class FramesObjects:
    def __init__(self, driver):
        self.driver = driver

    nested_frames = "//a[contains(text(), 'Nested Frames')]"
    i_frames = "//a[contains(text(), 'iFrame')]"

    def click_nested_frames(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, self.nested_frames))).click()

    def click_i_frames(self):
        wait = WebDriverWait(self.driver, 10)
        # Switch to default content first to ensure we're on the main page
        self.driver.switch_to.default_content()
        wait.until(EC.element_to_be_clickable((By.XPATH, self.i_frames))).click()

    def switch_to_frame(self, frame_reference):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it(frame_reference))

    def validate_frameset(self):
        # Locate the frameset element
        frameset = self.driver.find_element(By.TAG_NAME, "frameset")

       # Validate frameset attributes
        assert_with_log("1", frameset.get_attribute("frameborder"), "Frameborder should be 1")
        assert_with_log("frameset-middle", frameset.get_attribute("name"), "Name should be frameset-middle")
        assert_with_log("33%,33%,33%", frameset.get_attribute("cols"), "Cols should be 33%,33%,33%")

        # Find all frame elements within the frameset
        frames = frameset.find_elements(By.TAG_NAME, "frame")
        assert len(frames) == 3, "There should be 3 frames"

        # Expected frame details
        expected_frames = [
            {"src": "/frame_left", "scrolling": "no", "name": "frame-left"},
            {"src": "/frame_middle", "scrolling": "no", "name": "frame-middle"},
            {"src": "/frame_right", "scrolling": "no", "name": "frame-right"},
        ]

        # Validate each frame
        for i, frame in enumerate(frames):
            expected = expected_frames[i]
            assert_with_log(expected["src"], frame.get_attribute("src"), f"Frame {i} src should be {expected['src']}")
            assert_with_log(expected["scrolling"], frame.get_attribute("scrolling"), f"Frame {i} scrolling should be {expected['scrolling']}")
            assert_with_log(expected["name"], frame.get_attribute("name"), f"Frame {i} name should be {expected['name']}")
            
        logger.info("Frameset validation successful")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def validate_iframe(self):
        # Wait for the iframe to be available
        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.ID, "mce_0_ifr")))

        # Validate iframe attributes
        assert iframe.get_attribute("id") == "mce_0_ifr", "Iframe ID should be mce_0_ifr"
        assert iframe.get_attribute("title") == "Rich Text Area", "Iframe title should be 'Rich Text Area'"
        assert iframe.get_attribute("frameborder") == "0", "Iframe frameborder should be 0"
        assert iframe.get_attribute("allowtransparency") == "true", "Iframe allowtransparency should be true"

        # Switch to the iframe
        self.driver.switch_to.frame(iframe)

        # Validate content inside the iframe
        try:
            # Check if the editor body is present
            editor_body = self.driver.find_element(By.ID, "tinymce")
            assert editor_body is not None, "Editor body should be present"

            # Check initial content
            content = editor_body.get_attribute("innerHTML")
            assert "Your content goes here." in content, "Initial content should be present"

            logger.info("Iframe content validation successful")
        except Exception as e:
            logger.info(f"Error validating iframe content: {e}")
        finally:
            # Switch back to default content
            self.driver.switch_to.default_content()

        # Validate the container div
        container = self.driver.find_element(By.CLASS_NAME, "tox-editor-container")
        assert container is not None, "Editor container should be present"

        # Validate TinyMCE toolbar is disabled (as per the HTML)
        toolbar = self.driver.find_element(By.CLASS_NAME, "tox-toolbar-overlord")
        assert "tox-tbtn--disabled" in toolbar.get_attribute("class"), "Toolbar should be disabled"

        logger.info("Iframe validation successful")
