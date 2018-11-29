def test_open_empty_cart(home_page):
    new_page = home_page.open_cart_page()

    assert new_page.is_empty() is True


def test_add_new_product_to_cart(home_page):
    new_page = home_page.open_new_products_page()
    product_page = new_page.add_product_to_cart()
    product_page.buy_product()

    cart_page = product_page.open_cart_page()
    cart_page.fill_register_form('name', 'surname', '9261234567', 'name@ya.ru', is_subscribed=False)

    assert cart_page.get_product_in_cart_count() == 1
