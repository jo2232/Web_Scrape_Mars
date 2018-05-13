import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform

def init_browser():
    if platform == "darwin":
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    else:
        executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def build_titles(title):
    final_titles = ""
    for a in title:
        final_titles += " " + a
        print(final_titles)
    return final_titles

def scrape():
    browser = init_browser()
    
    nasa_data = {}
        
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    
        
    # News Article scrape
    list_items = []
    soup = BeautifulSoup(html, "html.parser")
    list_items = soup.find_all("ul", class_="item_list")

    titles = list_items[0].find_all("div", class_="content_title")

    title_list = []
    for div in titles:
        divs = div.text
        title_list.append(divs)

    nasa_data["news_titles"] = title_list

    teaser_soup = list_items[0].find_all("div", class_="article_teaser_body")

    teaser_list = []
    for teaser in teaser_soup:
        teasers = teaser.text
        teaser_list.append(teasers)

    nasa_data["news_teasers"] = teaser_list


# Weather Scrape
browser = init_browser()
    
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')    
    
weather_report = []
soup = BeautifulSoup(html, "html.parser")
tweet_text = soup.find("div", class_="js-tweet-text-container")
nasa_data["weather_report"] = tweet_text.p.text



# title_list = []
# for div in list_items:
#     divs = div.find("div", class_="content_title").text
#     title_list.append(divs)
#     print(title_list)


# In[35]:


browser = init_browser()

mars_pic = {}

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
#input_field = browser.find_by_css('html.js.flexbox.canvas.canvastext.webgl.geolocation.postmessage.no-websqldatabase.indexeddb.hashchange.history.draganddrop.websockets.rgba.hsla.multiplebgs.backgroundsize.borderimage.borderradius.boxshadow.textshadow.opacity.cssanimations.csscolumns.cssgradients.no-cssreflections.csstransforms.csstransforms3d.csstransitions.fontface.generatedcontent.video.audio.localstorage.sessionstorage.webworkers.applicationcache.svg.inlinesvg.smil.svgclippaths.-moz-.no-touch body#images.dark_background.logged_out.mobile_menu div#main_container div#site_body div#page section.filter_bar.module div.grid_layout form.section_search div.search_binder input.search_field')
#input_field[0].fill('surfing')
search_button = browser.find_by_xpath('//*[@id="full_image"]')
search_button.click()
time.sleep(7)
# more_info = browser.find_by_xpath('https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA17838')
# more_info.click()
# time.sleep(7)
html = browser.html
try:
    # create a soup object from the html
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find("div", class_="fancybox-inner")
    img_src = elem.find("img")["src"]
except:
    img_src =""

time.sleep(2)
# add our src to surf data with a key of src
mars_pic["src"] = img_src


# In[44]:


browser = init_browser()
    
mars_facts = {}
    
url = 'https://space-facts.com/mars/'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')    

labels = []
soup = BeautifulSoup(html, "html.parser")
div_locale = soup.find("div", class_="post-content")
label_locale = div_locale.find_all("td", class_="column-1")

for row in label_locale:
    labels.append(row.get_text())

facts = []
fact_locale = div_locale.find_all("td", class_="column-2")

for row in fact_locale:
    facts.append(row.get_text())



# In[47]:


import pandas as pd


# In[80]:


mars_df = pd.DataFrame({"label": labels})


# In[82]:


mars_df["facts"] = facts


# In[83]:


mars_df


# In[84]:


mars_df.to_html(columns={"label", "facts"})


# In[28]:


browser = init_browser()

hemi_pic = []

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

title_list = []
title_d = soup.find_all("div", class_="description")
for heading in title_d:
    hemi_title = heading.find("h3").get_text()
    title_list.append(hemi_title)
search_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div/section/div/div[2]/div[1]/a/img')
search_button.click()
time.sleep(7)

html = browser.html
try:
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find("div", id="wide-image")
    img_src = elem.find("img", class_="wide-image")["src"]
except:
    img_src =""
    
hemi_pic.append(img_src)

time.sleep(2)
back_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div[3]/section/a')
back_button.click()
time.sleep(7)

search_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div/section/div/div[2]/div[2]/a/img')
search_button.click()

time.sleep(7)

html = browser.html
try:
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find("div", id="wide-image")
    img_src = elem.find("img", class_="wide-image")["src"]
except:
    img_src =""

hemi_pic.append(img_src)

time.sleep(7)

back_button = browser.find_by_css('html body#splashy div.wrapper div.container div.content section.block.metadata a.button')
back_button.click()
time.sleep(7)

search_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div/section/div/div[2]/div[3]/a/img')
search_button.click()

html = browser.html
try:
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find("div", id="wide-image")
    img_src = elem.find("img", class_="wide-image")["src"]
except:
    img_src =""
    
hemi_pic.append(img_src)

time.sleep(7)

back_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div[3]/section/a')
back_button.click()

time.sleep(7)

search_button = browser.find_by_xpath('/html/body/div[1]/div[1]/div/section/div/div[2]/div[4]/a/img')
search_button.click()

time.sleep(7)

html = browser.html
try:
    # create a soup object from the html
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find("div", id="wide-image")
    img_src = elem.find("img", class_="wide-image")["src"]
except:
    img_src =""

hemi_pic.append(img_src)

hemisphere_image_urls = []
for i in range(0, len(hemi_pic)):
    item = {"title": title_list[i],
           "image_url": hemi_pic[i]}
    hemisphere_image_urls.append(item)

print(hemisphere_image_urls)
# mars_pic["src"] = img_src

