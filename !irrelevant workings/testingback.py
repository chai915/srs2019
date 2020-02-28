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

#PART 1        
# Access to Twitter
url = r'https://twitter.com/login'
driver = webdriver.Chrome('/Users/chloe/Desktop/chromedriver')
driver.get(url)

# Find login box
waiting_func('class name', 'js-username-field')
email = driver.find_element_by_class_name('js-username-field')
email.send_keys('putitatropica')
waiting_func('class name', 'js-password-field')
password = driver.find_element_by_class_name('js-password-field')
password.send_keys('tweety123', Keys.ENTER)

#Gets the tweets on dashboard

waiting_func('css selector', "[data-testid=tweet]")

last_height = driver.execute_script("return document.body.scrollHeight")

homepage_source = driver.page_source

tutorial_soup = BeautifulSoup(driver.page_source, 'html.parser')

tweets = tutorial_soup.findAll("div", {"data-testid":"tweet"})
list_of_tweets = []

for tweet in tweets:
    count = 0
    print("tweet")

    #check if promoted, get username and display name
    tweet_info = tweet.find_all('span',{"class":'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'})

    display_name = tweet_info[0].text.strip()
    user_name = tweet_info[2].text.strip()

    check_promoted = tweet_info[-1].text.strip()
    promoted_status = False
    hyperlink_val = ""

    if check_promoted == "Promoted":
        promoted_status = True

        # tweet_hyperlink = tweet.find_all("div", {"class":'css-1dbjc4n'})
        # print(len(tweet_hyperlink))
        # hyperlink_val = tweet_hyperlink.attribute('href')
        # print(hyperlink_val)

        print(" !!!!! Promoted Tweet ALERT !!!!!")

    print("Display Name: ", display_name)
    print("User Name: ", user_name)
    print("Promoted Status: ", promoted_status)
    print()

    #Get tweet text

    raw_tweet_text = tweet.find('div', {"class":'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})

    tweet_text = ""
    
    for x in raw_tweet_text:
        info = x.text.strip()
        tweet_text += info + " "

    print(tweet_text)
    print()

    tweet_info_list = [promoted_status, display_name, user_name, tweet_text] #, hyperlink_val]
    list_of_tweets += [tweet_info_list]


#PART 2
#write to file
with open('/Users/chloe/Desktop/SRS Project/tweet_file.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Promoted", "Display Name", "Username", "Tweet Text"]) #, "Attachment"])
    for tw in list_of_tweets:
        #if tw[3] == True: #as in, if its promoted write it to the file?
        writer.writerow([tw[0], tw[1], tw[2], tw[3]]) #, tw[4])




    