import logging
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright
import pytest
from pages.login_page import LoginPage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_results.log')
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture
def login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        login_page = LoginPage(page)
        yield login_page

        if hasattr(pytest, 'current_test_info') and pytest.current_test_info().failed:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot_on_failure",
                attachment_type=AttachmentType.PNG
            )

        browser.close()

"Перевіра видимості полів і кнопки"
@allure.feature("Login Page Elements")
@allure.story("Element Visibility")
@allure.title("Test username field visibility")
@allure.severity(allure.severity_level.NORMAL)
def test_username_field_is_visible(login_page):
    logger.info("Starting test_username_field_is_visible")
    
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Verify username field is visible"):
        assert login_page.is_element_visible(login_page.username_input), "Username field is not shown"
        logger.info("Test successful: Username field is shown")

@allure.feature("Login Page Elements")
@allure.story("Element Visibility")
@allure.title("Test password field visibility")
@allure.severity(allure.severity_level.NORMAL)
def test_password_field_is_visible(login_page):
    logger.info("Starting test_password_field_is_visible")
    
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Verify password field is visible"):
        assert login_page.is_element_visible(login_page.password_input), "Password field is not shown"
        logger.info("Test successful: Password field is shown")

@allure.feature("Login Page Elements")
@allure.story("Element Visibility")
@allure.title("Test login button visibility")
@allure.severity(allure.severity_level.NORMAL)
def test_login_button_is_visible(login_page):
    logger.info("Starting test_login_button_is_visible")
    
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Verify login button is visible"):
        assert login_page.is_element_visible(login_page.login_button), "Login button is not shown"
        logger.info("Test successful: Login button is shown")

@allure.feature("Login Functionality")
@allure.story("Login Scenarios")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        ("standard_user", "secret_sauce", None),
        ("invalid_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
        ("", "secret_sauce", "Epic sadface: Username is required"),
        ("standard_user", "", "Epic sadface: Password is required"),
        ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out.")
    ]
)
@allure.title("Test login with {username}/{password}")
def test_login(login_page, username, password, expected_message):
    logger.info(f"Starting test_login with username: {username}, password: {password}")
    
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step(f"Perform login with username: {username}, password: {password}"):
        login_page.login(username, password)
    
    if expected_message is None:
        with allure.step("Verify successful login"):
            assert login_page.is_login_successful(), "Login failed"
            logger.info("Test successful: User logged in")
    else:
        with allure.step("Verify error message"):
            error_message = login_page.get_error_message()
            assert error_message is not None, "Error message not displayed"
            assert expected_message in error_message, f"Unexpected error message: {error_message}"
            logger.info(f"Test successful: Error message displayed — '{error_message}'")

"Кейси на валідний/невалідний логін без параметризації. Аналогічно тому, що вище, але розбито на окремі функції. Закоментив, щоб не проганяти ті самі кейси двічі"    
# def test_successful_login(login_page):
#     login_page.navigate()
#     login_page.login("standard_user", "secret_sauce")
    
#     assert login_page.is_login_successful(), "Login failed"
#     print("Test successful: User logged in")
        

# def test_wrong_username_and_password(login_page):
#     login_page.navigate()
#     login_page.login("invalid_user", "wrong_password")
    
#     error_message = login_page.get_error_message()
#     assert error_message is not None, "Error message not displayed"
#     assert "Epic sadface: Username and password do not match any user in this service" in error_message, "Unexpected error message"
#     print("Test successful: Error message displayed for invalid login")
        

# def test_empty_username(login_page):
#     login_page.navigate()
#     login_page.login("","secret_sauce")
    
#     error_message = login_page.get_error_message()
#     assert error_message is not None, "Error message not displayed"
#     assert "Epic sadface: Username is required" in error_message, "Unexpected error message"
#     print("Test successful: Error message displayed for empty username")


# def test_empty_password(login_page):
#     login_page.navigate()
#     login_page.login("standard_user","")
    
#     error_message = login_page.get_error_message()
#     assert error_message is not None, "Error message not displayed"
#     assert "Epic sadface: Password is required" in error_message, "Unexpected error message"
#     print("Test successful: Error message displayed for empty password")


        
