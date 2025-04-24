from playwright.sync_api import sync_playwright
import pytest
from pages.login_page import LoginPage

@pytest.fixture
def login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        login_page = LoginPage(page)
        yield login_page
        browser.close()

"Перевіра видимості полів і кнопки"
def test_username_field_is_visible(login_page):
    login_page.navigate()
    assert login_page.is_element_visible(login_page.username_input), "Username field is not shown"
    print("Test successful: Username field is shown")
    
def test_password_field_is_visible(login_page):
    login_page.navigate()
    assert login_page.is_element_visible(login_page.password_input), "Password field is not shown"
    print("Test successful: Password field is shown")
    
def test_login_button_is_visible(login_page):
    login_page.navigate()
    assert login_page.is_element_visible(login_page.login_button), "Login button is not shown"
    print("Test successful: Login button is shown")

"Кейси на валідний/невалідний логін з параметризацією"
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

def test_login(login_page, username, password, expected_message):
    login_page.navigate()
    login_page.login(username, password)
      
    if expected_message is None:
        assert login_page.is_login_successful(), "Login failed"
        print("Test successful: User logged in")
    else:
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message not displayed"
        assert expected_message in error_message, f"Unexpected error message: {error_message}"
        print(f"Test successful: Error message displayed — '{error_message}'")

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


        