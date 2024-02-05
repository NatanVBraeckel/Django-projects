from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
from .models import Link

# Create your views here.
def scrape(request):

    if request.method == "POST":
        site = request.POST.get('site', '')
        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get("href")
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)
        return HttpResponseRedirect('/')
    else:
        link_address_list = Link.objects.all()

    return render(request, 'scraper/result.html', {'link_address_list': link_address_list})

def clear(request):
    Link.objects.all().delete()
    return HttpResponseRedirect('/')