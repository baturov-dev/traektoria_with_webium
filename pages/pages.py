from time import sleep

from selenium.webdriver.common.by import By
from webium import BasePage, Find, Finds
from webium.controls.checkbox import Checkbox
from webium.controls.link import Link

from settings import MAIN_URL


class SitePage(BasePage):
    new_page_link = Find(Link, by=By.XPATH, value='//a[@href="/new/"]')
    cart_link = Find(Link, by=By.XPATH, value='//a[@class="trigger" and @href="/cart/"]')

    def open_cart_page(self):
        self.cart_link.click()

        return CartPage(self._driver)

    def open_new_products_page(self):
        self.new_page_link.click()

        return NewPage(self._driver)


class HomePage(SitePage):
    def __init__(self, driver):
        super().__init__(driver=driver, url=MAIN_URL)

    def get_title(self):
        return self._driver.title


class NewPage(SitePage):
    new_products = Finds(
        by=By.XPATH,
        value='//a[@class="p_link" and not(descendant::div[@class="p_tags labels"]/span[text()="SOON"])]'
    )

    def add_product_to_cart(self):
        product = self._get_new_product()
        product.click()

        return ProductPage(self._driver)

    def _get_new_product(self, index=0):
        if index >= len(self.new_products):
            raise Exception('Index out of range for new_products')

        return self.new_products[index]


class CartPage(BasePage):
    home_page_button = Find(by=By.XPATH, value='//a[@class="btn "]')
    empty_cart = Find(by=By.XPATH, value='//*[@class="empty_cart "]')
    products_in_cart = Finds(by=By.XPATH, value='//li[ancestor::ul[@class="cart_product_list simple "]]')

    name_input = Find(by=By.XPATH, value='//input[@name="USER_NAME"]')
    surname_input = Find(by=By.XPATH, value='//input[@name="USER_LAST_NAME"]')
    phone_input = Find(by=By.XPATH, value='//input[@name="USER[PERSONAL_PHONE]"]')
    email_input = Find(by=By.XPATH, value='//input[@name="USER_EMAIL"]')
    subscribe_checkbox = Find(Checkbox, by=By.XPATH, value='//input[@name="USER[SUBSCRIBE]"]')
    register_button = Find(by=By.XPATH, value='//input[@class="compact show_if_fast_selected"]')
    terms_confirm_yes_button = Find(by=By.XPATH, value='//input[@name="terms_confirm_yes"]')

    def open_home_page(self):
        if not self.is_empty():
            raise Exception('The cart is not empty!')
        self.home_page_button.click()

        return HomePage(self._driver)

    def is_empty(self):
        return self.empty_cart is not None

    def get_product_in_cart_count(self):
        return len(self.products_in_cart)

    def fill_register_form(self, name, surname, phone, email, is_subscribed=False):
        self.name_input.send_keys(name)
        self.surname_input.send_keys(surname)
        self.phone_input.send_keys(phone)
        self.email_input.send_keys(email)
        self.subscribe_checkbox.set_checked(is_subscribed)

        self.register_button.submit()
        self.terms_confirm_yes_button.click()


class ProductPage(SitePage):
    buy_button = Find(by=By.XPATH, value='//*[@type="submit" and @class="btn buy kdxAddToCart"]')

    def buy_product(self):
        self.buy_button.click()
        # have to wait for element to become visible
        sleep(3)
