# """airscrape/tasks/scraper.py
# """
# from airscrape.models import Price, Store
# from requests_html import HTMLSession
# import re
#
#
# def import_price(product, store, selector, needs_render=False):
#     """
#     Parameters
#     ----------
#     product : Product Model
#     store : str
#         enum('target', 'bestbuy', 'frys')
#     selector : str
#     needs_render : bool
#     Returns
#     -------
#     None
#     """
#     session = HTMLSession()
#     url = getattr(product, f'{store}_url')
#     r = session.get(url)
#     if needs_render:
#         r.html.render()
#     pstring = r.html.find(selector, first=True).text
#     price = float(pstring[1:])
#     storemodel = Store.objects.get(name=store)
#     query = Price.objects.filter(product=product, store=storemodel)
#     if query.exists():
#         pricemodel = query.first()
#     else:
#         pricemodel = Price(product=product, store=storemodel)
#     pricemodel.price = price
#     pricemodel.save()
#
#
# def import_target(product):
#     """Import Target product pricing into DB.
#     Parameters
#     ----------
#     product : Product model
#     Returns
#     -------
#     None
#     """
#     selector = 'div.h-text-bold[data-test="product-price"]'
#     import_price(product, 'target', selector, needs_render=True)
#
#
# def import_frys(product):
#     """Import Frys product pricing into DB.
#     Parameters
#     ----------
#     product : Product model
#     Returns
#     -------
#     None
#     """
#     selector = 'span#did_price1valuediv.net-total.net-total-price'
#     import_price(product, 'frys', selector)
#
#
# def import_bestbuy(product):
#     """Import BestBuy product pricing into DB.
#     Parameters
#     ----------
#     product : Product model
#     Returns
#     -------
#     None
#     """
#     selector = 'div.priceView-hero-price.priceView-customer-price span'
#     import_price(product, 'bestbuy', selector)
#
#
# def import_walmart(product):
#     """Import BestBuy product pricing into DB.
#     Parameters
#     ----------
#     product : Product model
#     Returns
#     -------
#     None
#     """
#     selector = 'span.price.display-inline-block.arrange-fit.price.price--stylized'
#     import_price(product, 'walmart', selector)


# """airscrape/tasks/scraper.py
# """
# from airscrape.models import Price, Store, Product
# from requests_html import HTMLSession
#
#
# STORE_ARGS = {
#     'target': [
#         'div.h-text-bold[data-test="product-price"]',
#         True
#     ],
#     'bestbuy': [
#         'div.priceView-hero-price.priceView-customer-price span',
#         False
#     ],
#     'frys': [
#         'span#did_price1valuediv.net-total.net-total-price',
#         False
#     ]
# }
#
#
# def import_price_from_all(product):
#     for store, args in STORE_ARGS.items():
#         import_price(product, store)
#
#
# def import_all_product_prices():
#     for p in Product.objects.all():
#         import_price_from_all(p)
#
#
# def import_price(product, store):
#     """
#     Parameters
#     ----------
#     product : Product Model
#     store : str
#         enum('target', 'bestbuy', 'frys')
#     Returns
#     -------
#     None
#     """
#     session = HTMLSession()
#     url = getattr(product, f'{store}_url')
#     r = session.get(url)
#     args = STORE_ARGS[store]
#     selector = args[0]
#     needs_render = args[1]
#     if needs_render:
#         r.html.render()
#     pstring = r.html.find(selector, first=True).text
#     price = float(pstring[1:])
#     storemodel = Store.objects.get(name=store)
#     query = Price.objects.filter(product=product, store=storemodel)
#     if query.exists():
#         pricemodel = query.first()
#     else:
#         pricemodel = Price(product=product, store=storemodel)
#     pricemodel.price = price
#     pricemodel.save()

# """airscrape/tasks/scraper.py
# """
# from airscrape.models import Price, Store, Product
# from requests_html import HTMLSession
# from multiprocessing import Process, Pipe
# from multiprocessing.pool import ThreadPool
# from airscrape.external_tasks import get_rendered_html
#
#
# STORE_ARGS = {
#     'target': [
#         'div.h-text-bold[data-test="product-price"]',
#         True
#     ],
#     'bestbuy': [
#         'div.priceView-hero-price.priceView-customer-price span',
#         False
#     ],
#     'frys': [
#         'span#did_price1valuediv.net-total.net-total-price',
#         False
#     ]
# }
#
#
# def import_price_from_all(product, parallel=True):
#     if parallel:
#         with ThreadPool(4) as pool:
#             pool.starmap(import_price, [(product, store) for store in STORE_ARGS.keys()])
#     else:
#         for store, args in STORE_ARGS.items():
#             import_price(product, store)
#
#
# def import_all_product_prices(parallel=True):
#     if parallel:
#         with ThreadPool(4) as pool:
#             pool.map(import_price_from_all, [p for p in Product.objects.all()])
#     else:
#         for p in Product.objects.all():
#             import_price_from_all(p, parallel=False)
#
#
# def import_price(product, store):
#     """
#     Parameters
#     ----------
#     product : Product Model
#     store : str
#         enum('target', 'bestbuy', 'frys')
#     Returns
#     -------
#     None
#     """
#     session = HTMLSession()
#     url = getattr(product, f'{store}_url')
#     args = STORE_ARGS[store]
#     selector = args[0]
#     needs_render = args[1]
#     if needs_render:
#         child, parent = Pipe()
#         p = Process(target=get_rendered_html, args=(url, selector, child))
#         p.start()
#         pstring = parent.recv()
#         p.join()
#     else:
#         r = session.get(url)
#         pstring = r.html.find(selector, first=True).text
#     price = float(pstring[1:])
#     storemodel = Store.objects.get(name=store)
#     query = Price.objects.filter(product=product, store=storemodel)
#     if query.exists():
#         pricemodel = query.first()
#     else:
#         pricemodel = Price(product=product, store=storemodel)
#     pricemodel.price = price
#     pricemodel.save()


"""airscrape/tasks/scraper.py
"""
from airscrape.models import Price, Store, Product
from requests_html import HTMLSession
from multiprocessing.pool import ThreadPool
import subprocess
from airscrape.external_tasks import get_rendered_html


STORE_ARGS = {
    'target': [
        'div.h-text-bold[data-test="product-price"]',
        True
    ],
    'bestbuy': [
        'div.priceView-hero-price.priceView-customer-price span',
        False
    ],
    'frys': [
        'span#did_price1valuediv.net-total.net-total-price',
        False
    ]
}


def import_price_from_all(product, parallel=True):
    if parallel:
        with ThreadPool(4) as pool:
            pool.starmap(import_price, [(product, store) for store in STORE_ARGS.keys()])
    else:
        for store, args in STORE_ARGS.items():
            import_price(product, store)


def import_all_product_prices(parallel=True):
    if parallel:
        with ThreadPool(4) as pool:
            pool.map(import_price_from_all, [p for p in Product.objects.all()])
    else:
        for p in Product.objects.all():
            import_price_from_all(p, parallel=False)


def import_price(product, store):
    """
    Parameters
    ----------
    product : Product Model
    store : str
        enum('target', 'bestbuy', 'frys')
    Returns
    -------
    None
    """
    session = HTMLSession()
    url = getattr(product, f'{store}_url')
    args = STORE_ARGS[store]
    selector = args[0]
    needs_render = args[1]
    if needs_render:
        cmd = f'python airscrape/external_tasks.py "{url}" "{selector}"'
        out = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        pstring = str(out.stdout).replace('"', '').replace("'", '')[1:]
    else:
        r = session.get(url)
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