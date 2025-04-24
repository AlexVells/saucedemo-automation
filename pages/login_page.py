from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.saucedemo.com/"
        self.username_input = 'input[data-test="username"]'
        self.password_input = 'input[data-test="password"]'
        self.login_button = 'input[data-test="login-button"]'
        self.inventory_list = '.inventory_list'
        self.error_message = 'h3[data-test="error"]'

    def navigate(self):
        self.page.goto(self.url)

    def is_element_visible(self, selector: str):
        return self.page.is_visible(selector)

    def enter_username(self, username: str):
        self.page.fill(self.username_input, username)

    def enter_password(self, password: str):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_login_successful(self):
        return self.page.wait_for_selector(self.inventory_list, timeout=5000) is not None

    def get_error_message(self):
        return self.page.text_content(self.error_message) if self.page.is_visible(self.error_message) else None