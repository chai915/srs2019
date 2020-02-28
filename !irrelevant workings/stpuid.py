#THE CURRENT FAVOURITE BEING MODIFIED

#Simple assignment
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re
import random
from bs4 import BeautifulSoup

# PART 1
def waiting_func(driver, by_variable, attribute):
    # Function of waiting until the present of the element on the web page
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()

def find_login(driver):  
    # Find login box and log in
    try:
        waiting_func(driver, 'name', 'session[username_or_email]')
        email = driver.find_element_by_name("session[username_or_email]")
        email.send_keys('Chai915Chloe')

        waiting_func(driver, 'name', 'session[password]')
        password = driver.find_element_by_name("session[password]")
        password.send_keys('tweeter123', Keys.ENTER)

    except: 
        waiting_func(driver, 'class name', 'js-username-field')
        email = driver.find_element_by_class_name('js-username-field')
        email.send_keys('Chai915Chloe')

        waiting_func(driver, 'class name', 'js-password-field')
        password = driver.find_element_by_class_name('js-password-field')
        password.send_keys('tweeter123', Keys.ENTER)

def scroll_function(driver, height, last_height):
    #Scroll down the page, get tweets

    tweets = []
    new_height = driver.execute_script("return document.body.scrollHeight")
    print(" scrollHeight of Doc: ", new_height)

    # if last_height == new_height:
    #     return tweets, new_height

    # else: 

    driver.execute_script("window.scrollTo(0, {})".format(height))
    time.sleep(3)

    tutorial_soup = get_page_source(driver, "[data-testid=tweet]")
    tweets = find_tweets_in_source(tutorial_soup, driver)

    return tweets, new_height

def get_page_source(driver, thing_to_find): 

    waiting_func(driver, 'css selector', thing_to_find)    
    homepage_source = driver.page_source
    tutorial_soup = BeautifulSoup(homepage_source, 'html.parser')

    return tutorial_soup
    
def find_tweets_in_source(page_source, driver):

    list_of_tweets = []
    tweets = page_source.findAll("div", {"data-testid":"tweet"})
    
    for raw_tweet in tweets:
        list_of_tweets.append(raw_tweet)

    return list_of_tweets

def format_tweets(tweet_list, driver):
    #Gets the tweet information from the dashboard

    actual_tweets = []

    for tweet in tweet_list:
        # print("=== Tweet ===")

        #check if promoted, get username and display name
        tweet_info = tweet.find_all('span',{"class":'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})

        display_name = tweet_info[0].text.strip()
        user_name = tweet_info[2].text.strip()

        check_promoted = tweet_info[-1].text.strip()
        promoted_status = False

        if check_promoted == "Promoted":
            promoted_status = True

        #Get tweet text
        raw_tweet_text = tweet.find('div', {"class":'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})

        tweet_text = ""
        
        if raw_tweet_text != None:
            for x in raw_tweet_text:
                info = x.text.strip()
                tweet_text += info + " "
        else:
            tweet_text = ""
        
        # print(tweet_text)
        # print()

        #Check for attached links 
        attchd_link = ""
        for link in tweet.findAll('a', attrs={'href': re.compile("^(https://t.co/)[A-Za-z0-9?=]+")}): 
            attchd_link = link.get('href')
        
        if attchd_link != "":
            tweet_text += attchd_link

        #Check for embedded photos
        photo_links = []

        for pic_link in tweet.findAll('img', {"alt":"Image"}):
            photo_links += [pic_link.get('src')]

        if len(photo_links) != 0:
            for link in photo_links:
                tweet_text += link
        
        #Check for embedded video
        vid_src = ""

        for vid_link in tweet.findAll('video', {"aria-label":"Embedded video"}):
            vid_src = vid_link.get('src')

        if vid_src != "":
            tweet_text += vid_src

        tweet_info_list = [display_name, user_name, tweet_text, promoted_status]
        actual_tweets += [tweet_info_list]

    return actual_tweets

def check_uniqueness(tweet_list, non_unique_tweets):
    
    for x in non_unique_tweets:
        if len(tweet_list) == 0:
            print("empty list - currently appending the tweet")
            tweet_list.append(x)

        else:
            if x in tweet_list:
                break
            else:
                tweet_list.append(x)

    return tweet_list



# PART 2
def is_empty(file_name):
    #check if file is empty
    with open(file_name, 'r') as read_obj:
            # read first character
            one_char = read_obj.read(1)
            # if not fetched then file is empty
            if not one_char:
                return True
    return False

def write_to_file(file_name): 
    # write headers to file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Display Name", "Username", "Tweet Text", "Promoted"])

def append_to_file(tweet): 
    # append tweets to file note: only will do if promoted

    file_name = '/Users/chloe/Desktop/SRS Project/tweet_file2.csv'
    empty_status = is_empty(file_name)
    
    if empty_status == True:
        write_to_file(file_name)

    elif empty_status == False:
        with open('/Users/chloe/Desktop/SRS Project/tweet_file2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tweet[0], tweet[1], tweet[2], tweet[3]])
                
# PART 3 
def perform_action(driver):
    #randomise action - like, reply, retweet
    act = random.randint(1,3)
    driver.execute_script("window.scrollTo(0, 0)")
    
    if act == 1:
        like(driver)
    elif act == 2:
        retweet(driver)
    elif act == 3:
        reply(driver)

    time.sleep(3)

def like(driver):
    #likes the first tweet on the homepage 
    waiting_func(driver, 'css selector', "[data-testid=like]")

    like_element = driver.find_element_by_css_selector("[data-testid=like]")
    like_element.click()

    print("LIKED A TWEET!")

def retweet(driver):
    #retweets the first tweet on the homepage

    waiting_func(driver, 'css selector', "[data-testid=retweet]")

    retweet_element = driver.find_element_by_css_selector("[data-testid=retweet]")
    retweet_element.click()

    retweet_confirm = driver.find_element_by_css_selector("[data-testid=retweetConfirm]")
    retweet_confirm.click()
    
    print("RETWEETED A TWEET!")

def reply(driver):
    #replies to the first tweet on the homepage

    waiting_func(driver, 'css selector', "[data-testid=reply]")

    reply_element = driver.find_element_by_css_selector("[data-testid=reply]")
    reply_element.click()
    
    waiting_func(driver, 'css selector', "[data-testid=tweetTextarea_0]")
    reply_message = driver.find_element_by_css_selector("[data-testid=tweetTextarea_0]")
    reply_message.send_keys("wow")

    waiting_func(driver, 'css selector', "[data-testid=tweetButton]")
    tweet_button = driver.find_element_by_css_selector("[data-testid=tweetButton]")
    tweet_button.click()

    print("REPLIED WOW TO A TWEET!")

def main():
    url = r'https://twitter.com/login'
    driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
    driver.get(url)
    find_login(driver)

    scrollCount = 0
    height = 0
    tweet_list = []
    last_height = None
    prom_tweet_count = 0

    while scrollCount < 30:
        
        height = height + (500 * scrollCount)

        raw_tweets, new_height = scroll_function(driver, height, last_height)

        if len(raw_tweets) == 0:
            break

        else:
            last_height = new_height
            non_unique_tweets = format_tweets(raw_tweets, driver)
            unique_tweets = check_uniqueness(tweet_list, non_unique_tweets)
            tweet_list = unique_tweets

            scrollCount += 1

    # while prom_tweet_count < 5:
    if len(tweet_list) > 0:
        for tw in tweet_list:
            if tw[3] == True:
                append_to_file(tw)
                prom_tweet_count += 1
            

    #perform_action(driver)
    
main()



    