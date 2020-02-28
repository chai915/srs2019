#CURRENT FAVOURITE

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

import pickle
import pandas as pd
import random
import scipy

'''Features'''
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import label_binarize
from sklearn.feature_extraction.text import TfidfTransformer


'''Classifiers'''
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB

'''Metrics/Evaluation'''
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
from itertools import cycle


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
        email.send_keys('ShanStewart00')

        waiting_func(driver, 'name', 'session[password]')
        password = driver.find_element_by_name("session[password]")
        password.send_keys('ilovebts', Keys.ENTER)

    except: 
        waiting_func(driver, 'class name', 'js-username-field')
        email = driver.find_element_by_class_name('js-username-field')
        email.send_keys('ShanStewart00')

        waiting_func(driver, 'class name', 'js-password-field')
        password = driver.find_element_by_class_name('js-password-field')
        password.send_keys('ilovebts', Keys.ENTER)

def scroll_function(driver, height): #, last_height):
    #Scroll down the page, get tweets

    tweets = []
    #new_height = driver.execute_script("return document.body.scrollHeight")
    # print(" scrollHeight of Doc: ", new_height)

    # if last_height == new_height:
    #     return tweets, new_height

    # else: 

    driver.execute_script("window.scrollTo(0, {})".format(height))
    time.sleep(3)

    tutorial_soup = get_page_source(driver, "[data-testid=tweet]")
    tweets = find_tweets_in_source(tutorial_soup, driver)

    return tweets #, new_height

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

        #Check for attached links 
        # attchd_link = ""
        # for link in tweet.findAll('a', attrs={'href': re.compile("^(https://t.co/)[A-Za-z0-9?=]+")}): 
        #     attchd_link = link.get('href')
        
        # if attchd_link != "":
        #     tweet_text += "\nAttachment: " + attchd_link

        #Check for embedded photos
        # photo_links = []

        # for pic_link in tweet.findAll('img', {"alt":"Image"}):
        #     photo_links += [pic_link.get('src')]

        # if len(photo_links) != 0:
        #     for link in photo_links:
        #         tweet_text += "\nPhoto Src: " + link
        
        #Check for embedded video
        # vid_src = ""

        # for vid_link in tweet.findAll('video', {"aria-label":"Embedded video"}):
        #     vid_src = vid_link.get('src')

        # if vid_src != "":
        #     tweet_text += "\nVideo Src: " + vid_src

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
    try:
        with open(file_name, 'r') as read_obj:
                # read first character
                one_char = read_obj.read(1)
                # if not fetched then file is empty
                if not one_char:
                    return True
                else:
                    return False
    except:
        return False

def write_to_file(file_name): 
    # write headers to file
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Display Name", "Username", "Tweet Text", "Promoted", "Tweet Category", "Opposite Category"])

    file.close()

def append_to_file(actual_tweets, file_name): 
    # append tweets to file note: only will do if promoted

    #file_name = '/Users/chloe/Desktop/SRS Project/tweet_file.csv'
    empty_status = is_empty(file_name)
    
    if empty_status == False:
        write_to_file(file_name)
        
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for tw in actual_tweets:
            writer.writerow([tw[0], tw[1], tw[2], tw[3], tw[4], tw[5]])
                
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

#PART 4

def classify_tweet(promotedTweet):
    #classify the tweet into a category
    filename = '/Users/chloe/Desktop/SRS Project/finalized_sgdclassifier.pkl'
    loaded_classifier = pickle.load(open(filename, 'rb'))

    filename2 = '/Users/chloe/Desktop/SRS Project/tfidf_thing.pkl'
    loaded_tfidf = pickle.load(open(filename2, 'rb'))

    transformed_tweet = loaded_tfidf.transform([promotedTweet])

    pred_cat = loaded_classifier.predict(transformed_tweet)

    #print("Predicted Category is: ", pred_cat)
    return str(pred_cat[0])
    

def search_tweet(category_to_search, driver): 
    waiting_func(driver, 'css selector', "[data-testid=AppTabBar_Explore_Link]")
    explore_element = driver.find_element_by_css_selector("[data-testid=AppTabBar_Explore_Link]")
    explore_element.click()

    waiting_func(driver, 'css selector', "[data-testid=SearchBox_Search_Input]")
    searchBox = driver.find_element_by_css_selector("[data-testid=SearchBox_Search_Input]")
    searchBox.send_keys(category_to_search, Keys.ENTER)

    print("Prom Tweet actions:")
    perform_action(driver)

    driver.get("https://twitter.com")

def main():
    url = r'https://twitter.com/login'
    driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
    driver.get(url)
    find_login(driver)

    scrollCount = 0
    height = 0
    tweet_list = []
    #last_height = None

    while scrollCount < 10:
        
        height = height + (500 * scrollCount)

        raw_tweets = scroll_function(driver, height) #, last_height)

        if len(raw_tweets) == 0:
            break

        else:
            #last_height = new_height
            non_unique_tweets = format_tweets(raw_tweets, driver)
            unique_tweets = check_uniqueness(tweet_list, non_unique_tweets)
            tweet_list = unique_tweets

            scrollCount += 1

    prom_tweet_list = []
    normal_tweet_list = []

    for tw in tweet_list: 
        tweet_category_num = classify_tweet(tw[2])

        tweet_category = "cats"

        f = open('correlations.csv')
        csv_f = csv.reader(f)

        for row in csv_f:
            if row[0] == str(tweet_category_num):
                tweet_category = row[1]
                opposite_category = row[3]

        tw += [tweet_category, opposite_category]

        if tw[3] == True:
            prom_tweet_list += [tw]

        elif tw[3] == False:
            normal_tweet_list += [tw]

    print("Normal Tw List Len: ", len(normal_tweet_list))

    if len(prom_tweet_list) > 0:
        append_to_file(prom_tweet_list, '/Users/chloe/Desktop/SRS Project/PromoTweetsFile4.csv')

        for prom in prom_tweet_list:
            search_tweet(prom[5], driver)
            
    elif len(prom_tweet_list) == 0:
        print("No Promoted Tweets This Round")

    append_to_file(normal_tweet_list, '/Users/chloe/Desktop/SRS Project/nonPromoTweetsFile4.csv')

    perform_action(driver)
    
main()



    