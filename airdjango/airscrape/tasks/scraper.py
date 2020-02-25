"""airscrape/tasks/scraper.py
"""
from airscrape.models import Price, Store, Product
from requests_html import HTMLSession
from multiprocessing.pool import ThreadPool
import subprocess
from airscrape.ext_tasks import get_rendered_html


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
        cmd = f'python airscrape/ext_tasks.py "{url}" "{selector}"'
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

