from settings import EMAIL, PASSWORD, NAME


def test_add_new_product_to_cart(home_page):
    name = 'andre'
    surname = 'bud'
    new_page = home_page.open_new_products_page()
    product_page = new_page.add_product_to_cart()
    product_page.buy_product()
    cart_page = product_page.open_cart_page()
    cart_page = cart_page.fill_register_form(name, surname, '9261234567', 'name1@ya.ru', is_subscribed=False)

    assert cart_page.get_user_name() == f'{name.upper()} {surname.upper()}'


def test_add_new_product_and_login(home_page):
    new_page = home_page.open_new_products_page()
    product_page = new_page.add_product_to_cart()
    product_page.buy_product()
    cart_page = product_page.open_cart_page()
    cart_page.login(EMAIL, PASSWORD)

    assert cart_page.get_user_name() == NAME


def test_login(home_page):
    home_page = home_page.main_login(EMAIL, PASSWORD)

    assert home_page.get_user_name() == NAME


def test_registration(home_page):
    pass








