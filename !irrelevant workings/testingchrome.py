from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random

def waiting_func(by_variable, attribute):
    try:

        WebDriverWait(driver, 10).until(lambda x: x.find_element(by=by_variable,  value=attribute))
        
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()

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

def like(driver):
    #likes the first tweet on the homepage 
    waiting_func('css selector', "[data-testid=like]")

    like_element = driver.find_element_by_css_selector("[data-testid=like]")
    like_element.click()

    print("LIKED A TWEET!")

def retweet(driver):
    #retweets the first tweet on the homepage

    waiting_func('css selector', "[data-testid=retweet]")

    retweet_element = driver.find_element_by_css_selector("[data-testid=retweet]")
    retweet_element.click()

    retweet_confirm = driver.find_element_by_css_selector("[data-testid=retweetConfirm]")
    retweet_confirm.click()
    
    print("RETWEETED A TWEET!")

def reply(driver):
    #replies to the first tweet on the homepage

    waiting_func('css selector', "[data-testid=reply]")

    reply_element = driver.find_element_by_css_selector("[data-testid=reply]")
    reply_element.click()
    
    waiting_func('css selector', "[data-testid=tweetTextarea_0]")
    reply_message = driver.find_element_by_css_selector("[data-testid=tweetTextarea_0]")
    reply_message.send_keys("wow")

    waiting_func('css selector', "[data-testid=tweetButton]")
    tweet_button = driver.find_element_by_css_selector("[data-testid=tweetButton]")
    tweet_button.click()

    print("REPLIED WOW TO A TWEET!")

url = r'https://twitter.com/login'
driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
driver.get(url)
    
try:
    waiting_func('name', 'session[username_or_email]')
    email = driver.find_element_by_name("session[username_or_email]")
    email.send_keys('Chai915Chloe')

    waiting_func('name', 'session[password]')
    password = driver.find_element_by_name("session[password]")
    password.send_keys('tweeter123', Keys.ENTER)

except: 
    waiting_func('class name', 'js-username-field')
    email = driver.find_element_by_class_name('js-username-field')
    email.send_keys('Chai915Chloe')

    waiting_func('class name', 'js-password-field')
    password = driver.find_element_by_class_name('js-password-field')
    password.send_keys('tweeter123', Keys.ENTER)

waiting_func('css selector', "[data-testid=AppTabBar_Explore_Link]")
explore_element = driver.find_element_by_css_selector("[data-testid=AppTabBar_Explore_Link]")
explore_element.click()

waiting_func('css selector', "[data-testid=SearchBox_Search_Input]")
searchBox = driver.find_element_by_css_selector("[data-testid=SearchBox_Search_Input]")
searchBox.send_keys('japan', Keys.ENTER)

i = 0

while i < 3:
    perform_action(driver)
    i += 1
