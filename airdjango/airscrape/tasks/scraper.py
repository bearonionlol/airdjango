"""airscrape/tasks/scraper.py
"""
from airscrape.models import Price, Store
from requests_html import HTMLSession


def import_price(product, store, selector, needs_render=False):
    """

    Parameters
    ----------
    product : Product Model
    store : str
        enum('target', 'bestbuy', 'frys')
    selector : str
    needs_render : bool

    Returns
    -------
    None

    """
    session = HTMLSession()
    r = session.get(product.target_url)
    if needs_render:
        r.html.render()
    pstring = r.html.find(selector, first=True).text
    price = float(pstring[1:])
    storemodel = Store.objects.get(name=store)
    query = Price.objects.filter(product=product, store=storemodel)
    if query.exists():
        pricemodel = query.first()
    else:
        pricemodel = Price(product=product, store=storemodel)
    pricemodel.price = price
    pricemodel.save()


def import_target(product):
    """Import Target product pricing into DB.

    Parameters
    ----------
    product : Product model

    Returns
    -------
    None

    """
    selector = 'div.h-text-bold[data-test="product-price"]'
    import_price(product, 'target', selector, needs_render=True)


def import_frys(product):
    """Import Frys product pricing into DB.

    Parameters
    ----------
    product : Product model

    Returns
    -------
    None

    """
    selector = 'span#did_price1valuediv.net-total.net-total-price'
    import_price(product, 'frys', selector)


def import_bestbuy(product):
    """Import BestBuy product pricing into DB.

    Parameters
    ----------
    product : Product model

    Returns
    -------
    None

    """
    selector = 'div.priceView-hero-price.priceView-customer-price span'
    import_price(product, 'bestbuy', selector)

