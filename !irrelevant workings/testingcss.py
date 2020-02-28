#Simple assignment
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re
from bs4 import BeautifulSoup


# Function of waiting until the present of the element on the web page
def waiting_func(driver, by_variable, attribute):
    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


def find_login(driver):  # Find login box
    try: 
        waiting_func(driver, 'class name', 'js-username-field')
        email = driver.find_element_by_class_name('js-username-field')
        email.send_keys('putitatropica')

        waiting_func(driver, 'class name', 'js-password-field')
        password = driver.find_element_by_class_name('js-password-field')
        password.send_keys('tweety123', Keys.ENTER)

    except:
        waiting_func(driver, 'name', 'session[username_or_email]')
        email = driver.find_element_by_name("session[username_or_email]")
        email.send_keys('chloelovesminja@gmail.com')

        waiting_func(driver, 'name', 'session[password]')
        password = driver.find_element_by_name("session[password]")
        password.send_keys('tweety123', Keys.ENTER)

def scroll_function(driver):

    last_height = driver.execute_script("return document.body.scrollHeight")

    driver.execute_script("window.scrollTo(0, {})".format(last_height/5))
    time.sleep(3)
    
    #new_height = driver.execute_script("return document.body.scrollHeight")

    #return new_height
        # if last_height == new_height:
    #     break

def get_page_source(driver): 

    waiting_func(driver, 'css selector', "[data-testid=tweet]")    
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
    #Gets the tweets on dashboard
    actual_tweets = []

    for tweet in tweet_list:
        # count = 0
        print("=== Tweet ===")
        print()

        #check if promoted, get username and display name
        tweet_info = tweet.find_all('span',{"class":'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})

        display_name = tweet_info[0].text.strip()
        user_name = tweet_info[2].text.strip()

        check_promoted = tweet_info[-1].text.strip()
        promoted_status = False

        if check_promoted == "Promoted":
            promoted_status = True
            print(" !!!!! Promoted Tweet ALERT !!!!!")

        print("Display Name: ", display_name)
        print("User Name: ", user_name)
        print("Promoted Status: ", promoted_status)
        print()

        #Get tweet text
        raw_tweet_text = tweet.find('div', {"class":'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})

        tweet_text = ""
        
        if raw_tweet_text != None:
            for x in raw_tweet_text:
                info = x.text.strip()
                tweet_text += info + " "
        else:
            tweet_text = ""
        
        print(tweet_text)
        print()

        #check for embedded media
        outside_link = ""
        for link in tweet.findAll('a', attrs={'href': re.compile("^(https://t.co/)[A-Za-z0-9?=]+")}): 
            outside_link = link.get('href')

        tweet_info_list = [display_name, user_name, tweet_text, outside_link, promoted_status]
        actual_tweets += [tweet_info_list]

    write_to_file(actual_tweets)

# PART 2
def write_to_file(actual_tweets): # write to file
    with open('/Users/chloe/Desktop/SRS Project/tweet_file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Display Name", "Username", "Tweet Text", "Attached Link", "Promoted"])
        for tw in actual_tweets:
            #if tw[3] == True:
            writer.writerow([tw[0], tw[1], tw[2], tw[3], tw[4]])


def main():
    #PART 1: Access to Twitter
    url = r'https://twitter.com/login'
    driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
    driver.get(url)
    find_login(driver)

    #full_page_source = ""
    scrollCount = 0
    tweet_list = []

    while scrollCount < 20:
        current_soup = get_page_source(driver)
        tweet_list += find_tweets_in_source(current_soup, driver)
        scroll_function(driver) #, last_height)
        scrollCount += 1

    format_tweets(tweet_list, driver)

main()



    