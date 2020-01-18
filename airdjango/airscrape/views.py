from airscrape.models import Price
from django.template.response import TemplateResponse


def index(request):
    query = Price.objects.all()
    context = {'prices': query}
    return TemplateResponse(request, 'general/index.html', context)

