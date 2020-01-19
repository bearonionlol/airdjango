from django.core.management.base import BaseCommand
from airscrape.models import Price
from requests_html import AsyncHTMLSession

def save_price(prices):
    stores = prices['stores_and_prices']
    the_cheapest_price = prices['cheapest_price']
    price = Price()
    price.stores_and_prices = stores
    price.cheapest_price = the_cheapest_price
    price.save()


asession = AsyncHTMLSession()

bestbuy_price = []
a = {}
async def get_bestbuy():
    r = await asession.get('https://www.bestbuy.com/site/apple-airpods-pro-white/5706659.p?skuId=5706659')
    sel = 'div.priceView-hero-price.priceView-customer-price span'
    print("The current price for AirPods Pro at Best Buy: " +r.html.find(sel, first=True).text)
    bestbuy_price.append(r.html.find(sel, first=True).text)
    a["Best Buy"] = r.html.find(sel, first=True).text
    return (bestbuy_price)

frys_price = []
b = {}
async def get_frys():
    r = await asession.get('https://www.frys.com/product/9956186?site=sr:SEARCH:MAIN_RSLT_PG')
    sel = 'span#did_price1valuediv.net-total.net-total-price'
    print("The current price for AirPods Pro at Fry's: " +r.html.find(sel, first=True).text)
    frys_price.append(r.html.find(sel, first=True).text)
    b["Fry's"] = r.html.find(sel, first=True).text
    return (frys_price)

target_price = []
c = {}
async def get_target():
    r = await asession.get('https://www.target.com/p/apple-airpods-pro/-/A-54191101?ref=tgt_adv_XS000000&AFID=google_pla_df&fndsrc=tgtao&CPNG=PLA_Electronics%2BShopping_Local&adgroup=SC_Electronics&LID=700000001170770pgs&network=g&device=c&location=9027766&ds_rl=1246978&ds_rl=1248099&ds_rl=1246978&gclid=CjwKCAiA8ejuBRAaEiwAn-iJ3tZYPXz9_sFzXa_lRKXQAr7zzTpoo3XoE3k7JX8rpajVo4JUbovfTxoChYEQAvD_BwE&gclsrc=aw.ds')
    await r.html.arender()
    sel = 'div.h-text-bold[data-test="product-price"]'
    print("The current price for AirPods Pro at Target: " +r.html.find(sel, first=True,).text)
    target_price.append(r.html.find(sel, first=True).text)
    c["Target"] = r.html.find(sel, first=True).text
    return (target_price)

result = asession.run(get_bestbuy, get_frys, get_target,)

for x in a, b, c:
    print(x)


all_prices = []
for price in bestbuy_price, frys_price, target_price,:
    dollar_stripped = price[0].strip('$')
    all_prices.append(float(dollar_stripped))
# print(all_prices)


def lowest_price():
    lowest_price = []
    low = min(all_prices)
    for x in all_prices:
        if x == low:
            lowest_price.append(str(x))
    return lowest_price


my_list = lowest_price()
d = {**a, **b, **c,}
# print([k for k, v in d.items() if v[1:] in my_list])

all_stores = []
for k, v in d.items():
    if v[1:] in my_list:
        print(k + " " + "has the cheapest set of AirPods Pro at: $" + my_list[0])
        out = {
            'stores_and_prices': k,
            'cheapest_price': k + " " + "has the cheapest set of AirPods Pro at: $" + my_list[0]
        }
        all_stores.append(out)


class Command(BaseCommand):
    def handle(self, **options):
        # result()
        print(all_stores)
        for z in all_stores:
            save_price(z)