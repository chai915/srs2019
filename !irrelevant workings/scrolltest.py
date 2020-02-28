#Simple assignment
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time 
import csv
from bs4 import BeautifulSoup


# Function of waiting until the present of the element on the web page
def waiting_func(by_variable, attribute):
    try:

        WebDriverWait(driver, 10).until(lambda x: x.find_element(by=by_variable,  value=attribute))
        
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


def waiting_func_for_loading(by_variable, attribute):
    try:
        WebDriverWait(driver, 10)
        
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()

def tweet_mod(driver, tweets):
    if len(tweets) != None:
        print("No. of tweets in list = ", len(tweets))

    tw_list= []

    for tweet in tweets:
        #count = 0
        # print("tweet")

        #check if promoted, get username and display name
        tweet_info = tweet.find_all('span',{"class":'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})

        display_name = tweet_info[0].text.strip()
        user_name = tweet_info[2].text.strip()

        check_promoted = tweet_info[-1].text.strip()
        promoted_status = False

        if check_promoted == "Promoted":
            promoted_status = True
            print(" !!!!! Promoted Tweet ALERT !!!!!")

        # print("Display Name: ", display_name)
        # print("User Name: ", user_name)
        # print("Promoted Status: ", promoted_status)
        # print()

        #Get tweet text

        raw_tweet_text = tweet.find('div', {"class":'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})

        tweet_text = ""
        
        if raw_tweet_text != None:
            for x in raw_tweet_text:
                info = x.text.strip()
                tweet_text += info + " "
        
        # print(tweet_text)
        # print()

        tweet_info_list = [display_name, user_name, tweet_text, promoted_status]
        tw_list += [tweet_info_list]

    print("Len of TW List: ", len(tw_list))
    return tw_list


def scrolling(driver, initial_height):

    driver.execute_script("window.scrollTo(0, {})".format(initial_height))
    time.sleep(3)

    waiting_func('css selector', "[data-testid=tweet]")

    tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')
    tweets = tutorial_soup.findAll("div", {"data-testid":"tweet"})

    return tweets


def check_uniqueness(list_twww, non_unique_tweets):
    
    for x in non_unique_tweets:
        if len(list_twww) == 0:
            print("empty list - currently appending the tweet")
            list_twww.append(x)

        else:
            if x in list_twww:
                break
            else:
                list_twww.append(x)

    return list_twww


def append_to_file(actual_tweets): # write to file
    with open('/Users/chloe/Desktop/SRS Project/tweet_file.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for tw in actual_tweets:
            #if tw[3] == True:
            writer.writerow([tw[0], tw[1], tw[2], tw[3]])

#PART 1        
# Access to Twitter
url = r'https://twitter.com/login'
driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
driver.get(url)

# Find login box
try:
    waiting_func('name', 'session[username_or_email]')
    email = driver.find_element_by_name("session[username_or_email]")
    email.send_keys('chloelovesminja@gmail.com')

    waiting_func('name', 'session[password]')
    password = driver.find_element_by_name("session[password]")
    password.send_keys('tweety123', Keys.ENTER)

except:
    waiting_func('class name', 'js-username-field')
    email = driver.find_element_by_class_name('js-username-field')
    email.send_keys('chloelovesminja@gmail.com')
    waiting_func('class name', 'js-password-field')
    password = driver.find_element_by_class_name('js-password-field')
    password.send_keys('tweety123', Keys.ENTER)
    
#Gets the tweets on dashboard

with open('/Users/chloe/Desktop/SRS Project/tweet_file.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Display Name", "Username", "Tweet Text", "Promoted"])

initial_height = 0
count = 0
tweets = []

list_of_tweets = []

while count < 30:    
    tweets_list = scrolling(driver, initial_height + (500 * count))
    non_unique_tweets = tweet_mod(driver, tweets_list)
    
    unique_tweets = check_uniqueness(list_of_tweets, non_unique_tweets)
    list_of_tweets = unique_tweets

    print(len(list_of_tweets))
    
    count += 1

print("Current TweetList Length", len(list_of_tweets))
print("======= Tweets ========")
for tw in list_of_tweets:
    print(tw)

append_to_file(list_of_tweets)
    


    







    