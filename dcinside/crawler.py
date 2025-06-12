from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from .exception import ServerException, DeletedPostException, StaleElementException

class Crawler:
    def __init__(self, driver_path, timeout=60, retry=True):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")

        self.retry = retry
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_page_load_timeout(timeout)

    def crawl(self, gallery, idx):
        while True:
            try:
                self.driver.get(f"https://gall.dcinside.com/board/view/?id={gallery}&no={idx}")

                try:
                    self.driver.find_element(By.CLASS_NAME, "delet")
                except NoSuchElementException:
                    pass
                else:
                    raise DeletedPostException

                comments = []
                try:
                    n_comments = self.driver.find_element(By.CLASS_NAME, "cmt_paging")
                    n_comments = n_comments.find_elements(By.TAG_NAME, "a")
                    last_comment_page = len(n_comments) + 1
                except NoSuchElementException:
                    last_comment_page = 0

                title = self.driver.find_element(By.CLASS_NAME, "title_subject")
                content = self.driver.find_element(By.CLASS_NAME, "writing_view_box")
                content_divs = content.find_elements(By.TAG_NAME, "div")
                content = content_divs[-1]

                for i in range(last_comment_page, 0, -1):
                    self.driver.execute_script(f"viewComments({i}, 'D')")

                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "usertxt"))
                    )

                    page_comments = self.driver.find_elements(By.CLASS_NAME, "usertxt")
                    for comment in page_comments:
                        try:
                            comments.append(comment.text)
                        except StaleElementReferenceException:
                            pass

                return {
                    "title": title.text,
                    "content": content.text,
                    "comments": comments
                }

            except DeletedPostException:
                raise DeletedPostException

            except (NoSuchElementException, TimeoutException):
                if not self.retry:
                    raise ServerException
                # retry 동작을 위해 while 루프 계속
