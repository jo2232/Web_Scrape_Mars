import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform
import pandas as pd

def init_browser():
    if platform == "darwin":
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    else:
        executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    nasa_data = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup_news = BeautifulSoup(html, 'html.parser')    

# News Article scrape    
    titles = soup_news.find_all("div", class_="content_title")

    title_list = []
    for div in titles:
        divs = div.text
        title_list.append(divs)

    nasa_data["news_titles"] = title_list

    teaser_soup = soup_news.find_all("div", class_="article_teaser_body")
    time.sleep(2)

    teaser_list = []
    for teaser in teaser_soup:
        teasers = teaser.text
        teaser_list.append(teasers)

    nasa_data["news_teasers"] = teaser_list

#Weather Report
    browser = init_browser()
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')    

    weather_report = []
    soup = BeautifulSoup(html, "html.parser")
    tweet_text = soup.find("div", class_="js-tweet-text-container")
    
    nasa_data["weather_report"] = tweet_text.p.text
    
#Featured Mars Image
    browser = init_browser()

    mars_pic = {}

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup_feature = BeautifulSoup(html, 'html.parser')
    src_url = 'https://www.jpl.nasa.gov'

    search_button = browser.find_by_xpath('//*[@id="full_image"]')
    search_button.click()
    time.sleep(7)

    html = browser.html
    try:
        img_soup = BeautifulSoup(html, "html.parser")
        elem = img_soup.find("div", class_="fancybox-inner")
        img_src = elem.find("img")["src"]
    except:
        img_src =""

    time.sleep(2)

    nasa_data["src"] = src_url + img_src
    
    #mars facts
    browser = init_browser()

    mars_facts = {}

    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    

    labels = []
    soup_facts = BeautifulSoup(html, "html.parser")
    div_locale = soup_facts.find("div", class_="post-content")
    label_locale = div_locale.find_all("td", class_="column-1")

    for row in label_locale:
        labels.append(row.get_text())

    facts = []
    fact_locale = div_locale.find_all("td", class_="column-2")

    for row in fact_locale:
        facts.append(row.get_text())

    nasa_data["facts"] = facts
    nasa_data["fact_labels"] = labels

    mars_df = pd.DataFrame({"label": labels})
    mars_df["facts"] = facts
    mars_table = mars_df.to_html(columns={"label", "facts"})

    nasa_data["fact_table"] = mars_table

    #hemisphere scrape
    browser = init_browser()

    hemi_pic = []

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup_hemi = BeautifulSoup(html, 'html.parser')
    hemi_src_url = 'https://astrogeology.usgs.gov'

    title_list = []
    title_d = soup_hemi.find_all("div", class_="description")
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
    full_url = hemi_src_url + img_src
    hemi_pic.append(full_url)

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

    full_url = hemi_src_url + img_src
    hemi_pic.append(full_url)

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

    full_url = hemi_src_url + img_src
    hemi_pic.append(full_url)

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

    full_url = hemi_src_url + img_src
    hemi_pic.append(full_url)

    hemisphere_image_urls = []
    for i in range(0, len(hemi_pic)):
        item = {"title": title_list[i],
               "image_url": hemi_pic[i]}
        hemisphere_image_urls.append(item)

    nasa_data["hemispheres"] = hemisphere_image_urls

    return nasa_data

   


