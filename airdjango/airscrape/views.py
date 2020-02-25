# from django.shortcuts import render
#
# # Create your views here.

# from airscrape.models import Price, Product, Store
# from django.template.response import TemplateResponse
#
#
# def index(request):
#     query = Price.objects.all()
#     context = {'prices': query}
#     return TemplateResponse(request, 'general/index.html', context)


from airscrape.models import Price, Product
from django.template.response import TemplateResponse
from airscrape.tasks import scraper


from airscrape.models import Price, Product
from django.template.response import TemplateResponse
from airscrape.tasks import scraper

def index(request):
    if request.method == 'POST':
        if 'update' in request.POST:
            if request.POST['update'] == 'Update':
                scraper.import_all_product_prices()
    query = Product.objects.all()
    context = {'products': query}
    return TemplateResponse(request, 'general/index.html', context)
