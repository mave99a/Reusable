# -*- coding: utf-8 -*-
import re
from django.utils.html import escape
from google.appengine.api import urlfetch
from django.http import HttpResponse, HttpResponseRedirect

from PageRank import PageRank 
from xml.etree.ElementTree import XML

def ScrapeSearchResult(url, regex, groupname):
    try: 
        result = urlfetch.fetch(url)
        p =re.compile(regex)
        f = p.search(result.content)
        if (f != None): 
            res = f.group(groupname)
        else: 
            res = "0"
    except:
        res = "?"
         
    return res  
#
#  Google.com's indexed pages and links
#  
def gpages(request, site):
    res = ScrapeSearchResult('http://www.google.com/search?q=site:' + site, '<b>(?P<number>[\d,]*)</b> from <b>', 'number')   
    return HttpResponse(res)

def glinks(request, site):
    res = ScrapeSearchResult('http://www.google.com/search?q=link:' + site, '<b>(?P<number>[\d,]*)</b> linking to', 'number')   
    return HttpResponse(res)

#  Microsoft Live.com search, "Advanced search keywords"
#    site: Returns webpages that belong to the specified site. 
#    inanchor: These keywords return webpages that contain the specified term in the metadata
def livepages(request, site):
    res = ScrapeSearchResult('http://search.live.com/results.aspx?q=site:' + site, 'of (?P<number>[\d,]*) result', 'number')   
    return HttpResponse(res)

def livelinks(request, site):
    res = ScrapeSearchResult('http://search.live.com/results.aspx?q=inanchor:' + site, 'of (?P<number>[\d,]*) result', 'number')   
    return HttpResponse(res)

# baidu
def baidupages(request, site):
    res = ScrapeSearchResult('http://www.baidu.com/s?wd=site:' + site, '<td align="right" nowrap>\D*(?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)

def baidulinks(request, site):
    res = ScrapeSearchResult('http://www.baidu.com/s?wd=inurl:' + site, '<td align="right" nowrap>\D*(?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)

# yahoo
def ypages(request, site):
    res = ScrapeSearchResult('http://siteexplorer.search.yahoo.com/search?p=http://' + site, 'Pages \((?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)

def ylinks(request, site):
    res = ScrapeSearchResult('http://siteexplorer.search.yahoo.com/search?p=http://' + site, 'Inlinks \((?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)

def delicious(request, site):
    res = ScrapeSearchResult('http://del.icio.us/url/check?url=http://' + site, 'class="savers(\d*)">(?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)
    
def reddit(request, site):
    res = ScrapeSearchResult('http://www.reddit.com/search?q=' + site, 'class="summary">about (?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)

#===============================================================================
# def digg(request, site):
#    res = ScrapeSearchResult('http://digg.com/search?submit=Search&section=news&type=url&area=all&sort=new&s=' + site, 'class="summary">about (?P<number>[\d,]*)', 'number')   
#    return HttpResponse(res)
#===============================================================================


def w3chtml(request, site):
    res = ScrapeSearchResult('http://validator.w3.org/check?uri=http://' + site, '<h2 id="results"(?P<number>.*)</h2>', 'number')   
    return HttpResponse(res)

def w3ccss(request, site):
    res = ScrapeSearchResult('http://jigsaw.w3.org/css-validator/validator?uri=' + site, '<h3>(?P<number>.*)</h3>', 'number')   
    return HttpResponse(res)


def stumbleupon(request, site):
    res = ScrapeSearchResult('http://www.stumbleupon.com/url/' + site, 'class="textOk">(?P<number>[\d,]*)', 'number')   
    return HttpResponse(res)


# page ranks
def gpr(request, site):
    res = str(PageRank(site))
    return HttpResponse(res)

#whois 
def whois(request, site):
    result = urlfetch.fetch('http://www.trynt.com/whois-api/v1/?f=0&h=' + site)
    whoisres = XML(result.content)
    name = whoisres.find('Whois/regrinfo/owner/name').text
    return HttpResponse(name) 
