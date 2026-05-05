import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
BASE_URL = "http://100.53.112.114:8001"
ADMIN_EMAIL = "admin@hakibank.com"
ADMIN_PASSWORD = "admin123"
TEST_EMAIL = "testuser_selenium@gmail.com"
TEST_PASSWORD = "Test@12345"
TEST_NAME = "Selenium User"


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """Set up headless Chrome WebDriver for each test."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Driver fixture that logs in as admin before the test."""
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']").send_keys(ADMIN_EMAIL)
    driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(4)
    return driver


# ─────────────────────────────────────────────
# Test Cases
# ─────────────────────────────────────────────

class TestPageLoading:
    """TC01–TC03: Basic page loading tests"""

    def test_TC01_landing_page_loads(self, driver):
        """TC01: Landing page should load with correct title."""
        driver.get(BASE_URL)
        assert driver.title != "", "Page title should not be empty"
        assert "404" not in driver.title.lower(), "Page should not return 404"

    def test_TC02_login_page_loads(self, driver):
        """TC02: Login page should load and contain email/password inputs."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        email_input = driver.find_elements(By.CSS_SELECTOR, "input[type='email'], input[name='email']")
        password_input = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        assert len(email_input) > 0, "Email input should be present on login page"
        assert len(password_input) > 0, "Password input should be present on login page"

    def test_TC03_signup_page_loads(self, driver):
        """TC03: Signup page should load and contain registration form."""
        driver.get(f"{BASE_URL}/signup")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        inputs = driver.find_elements(By.TAG_NAME, "input")
        assert len(inputs) >= 3, "Signup page should have at least 3 input fields"


class TestAuthentication:
    """TC04–TC08: Authentication tests"""

    def test_TC04_successful_admin_login(self, driver):
        """TC04: Admin should be able to login with valid credentials."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']").send_keys(ADMIN_EMAIL)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)
        assert "/login" not in driver.current_url, "Admin should be redirected away from login after success"

    def test_TC05_login_with_wrong_password(self, driver):
        """TC05: Login with wrong password should stay on login page."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']").send_keys(ADMIN_EMAIL)
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        assert "/login" in driver.current_url or driver.find_elements(
            By.CSS_SELECTOR, "input[type='password']"
        ), "User should remain on login page after wrong password"

    def test_TC06_login_with_invalid_email(self, driver):
        """TC06: Login with non-existent email should fail."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']").send_keys("nonexistent@fake.com")
        driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys("anypassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        assert "/login" in driver.current_url or driver.find_elements(
            By.CSS_SELECTOR, "input[type='password']"
        ), "User should remain on login page with invalid email"

    def test_TC07_successful_signup(self, driver):
        """TC07: New user should be able to register successfully."""
        import random
        unique_email = f"testuser_{random.randint(1000,9999)}@gmail.com"
        driver.get(f"{BASE_URL}/signup")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        inputs = driver.find_elements(By.TAG_NAME, "input")
        # Fill name, email, password fields
        for inp in inputs:
            input_type = inp.get_attribute("type") or ""
            input_name = inp.get_attribute("name") or ""
            if "name" in input_name.lower() or "full" in input_name.lower():
                inp.send_keys(TEST_NAME)
            elif input_type == "email" or "email" in input_name.lower():
                inp.send_keys(unique_email)
            elif input_type == "password":
                inp.send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        assert "/signup" not in driver.current_url or "success" in driver.page_source.lower(), \
            "User should be redirected or see success message after signup"

    def test_TC08_logout_functionality(self, logged_in_driver):
        """TC08: Logged-in user should be able to logout."""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        # Look for logout button/link
        logout_elements = driver.find_elements(By.XPATH,
            "//*[contains(text(),'Logout') or contains(text(),'logout') or contains(text(),'Sign Out')]"
        )
        assert len(logout_elements) > 0, "Logout button should be visible after login"
        logout_elements[0].click()
        time.sleep(2)
        assert "/login" in driver.current_url or BASE_URL == driver.current_url, \
            "User should be redirected to login or home after logout"


class TestDashboard:
    """TC09–TC11: Dashboard and navigation tests"""

    def test_TC09_admin_dashboard_loads(self, logged_in_driver):
        """TC09: Admin dashboard should load after login."""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        time.sleep(2)
        page_source = driver.page_source.lower()
        assert any(word in page_source for word in ["dashboard", "balance", "account", "welcome"]), \
            "Dashboard page should contain dashboard-related content"

    def test_TC10_dashboard_has_navigation(self, logged_in_driver):
        """TC10: Dashboard should have navigation menu."""
        driver = logged_in_driver
        time.sleep(2)
        nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .sidebar, .navbar, [class*='nav'], [class*='sidebar']")
        assert len(nav_elements) > 0, "Dashboard should have a navigation element"

    def test_TC11_admin_can_access_manage_users(self, logged_in_driver):
        """TC11: Admin should be able to navigate to manage users page."""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        time.sleep(2)
        user_links = driver.find_elements(By.XPATH,
            "//*[contains(text(),'User') or contains(text(),'user') or contains(@href,'user')]"
        )
        assert len(user_links) > 0, "Admin should see user management links"


class TestNavigation:
    """TC12–TC15: Navigation and page access tests"""

    def test_TC12_unauthenticated_redirect(self, driver):
        """TC12: Unauthenticated access to dashboard should redirect to login."""
        driver.get(f"{BASE_URL}/dashboard")
        time.sleep(2)
        assert "/login" in driver.current_url or "login" in driver.page_source.lower(), \
            "Unauthenticated user should be redirected to login"

    def test_TC13_login_page_has_signup_link(self, driver):
        """TC13: Login page should have a link to signup page."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        signup_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'signup') or contains(text(),'Sign up') or contains(text(),'Register')]"
        )
        assert len(signup_links) > 0, "Login page should have a link to signup"

    def test_TC14_signup_page_has_login_link(self, driver):
        """TC14: Signup page should have a link back to login page."""
        driver.get(f"{BASE_URL}/signup")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        login_links = driver.find_elements(By.XPATH,
            "//a[contains(@href,'login') or contains(text(),'Login') or contains(text(),'Sign in')]"
        )
        assert len(login_links) > 0, "Signup page should have a link to login"

    def test_TC15_page_title_contains_bank(self, driver):
        """TC15: Every page title or content should reference HakiBank."""
        driver.get(BASE_URL)
        time.sleep(2)
        content = (driver.title + driver.page_source).lower()
        assert "haki" in content or "bank" in content, \
            "Page should reference HakiBank in title or content"

    def test_TC16_login_form_submit_button_exists(self, driver):
        """TC16: Login form should have a submit button."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        submit_btn = driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        assert len(submit_btn) > 0, "Login form should have a submit button"

    def test_TC17_admin_transactions_page_accessible(self, logged_in_driver):
        """TC17: Admin should be able to access transaction monitoring page."""
        driver = logged_in_driver
        driver.get(f"{BASE_URL}/admin/transactions")
        time.sleep(2)
        assert "404" not in driver.page_source, "Transaction monitoring page should be accessible"

    def test_TC18_multiple_page_navigation(self, logged_in_driver):
        """TC18: User should be able to navigate between multiple pages without errors."""
        driver = logged_in_driver
        pages = ["/dashboard", "/profile"]
        for page in pages:
            driver.get(f"{BASE_URL}{page}")
            time.sleep(1)
            assert "error" not in driver.page_source.lower() or "404" not in driver.title, \
                f"Page {page} should load without errors"

    def test_TC19_app_responds_to_invalid_route(self, driver):
        """TC19: App should handle invalid routes gracefully (SPA fallback)."""
        driver.get(f"{BASE_URL}/this-route-does-not-exist-xyz")
        time.sleep(2)
        # SPA apps redirect to home or show a 404 component, not a blank page
        assert len(driver.page_source) > 100, "App should return some content for invalid routes"

    def test_TC20_login_page_password_field_masked(self, driver):
        """TC20: Password field on login page should be of type password (masked)."""
        driver.get(f"{BASE_URL}/login")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        assert password_field.get_attribute("type") == "password", \
            "Password field should be masked (type=password)"
        
