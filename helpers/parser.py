from bs4 import BeautifulSoup
from selenium import webdriver


def parser(username):   
    data = {}
    parsed_data = [None]

    #Chrome Driver
    driver = webdriver.Chrome()


    #Driver Manipulation
    driver.get(f"https://nitter.poast.org/{username}")
    respose = driver.page_source
    driver.close()

    #Parsing...
    soup = BeautifulSoup(respose, "html.parser")

    #Profile Name and Handle
    name_handle = soup.find("div", {"class": "profile-card-tabs-name"})
    try:
        data["profile_name"] = name_handle.find("a", {"class": "profile-card-fullname"}).text
    except:
        data["profile_name"] = None
    try:
        data["profile_handle"] = name_handle.find("a", {"class": "profile-card-username"}).text
    except:
        data["profile_handle"] = None

    #Following and Follower Count
    following_followers = soup.find("div", {"class": "profile-card-extra-links"})
    try:
        data["profile_following"] = following_followers.find("li", {"class": "following"}).find("span", {"class": "profile-stat-num"}).text
    except:
        data["profile_following"] = None
    try:
        data["profile_followers"] = following_followers.find("li", {"class": "followers"}).find("span", {"class": "profile-stat-num"}).text
    except:
        data["profile_followers"] = None

    #Most Recent Tweet
    tweet = soup.find("div", {"class": "tweet-body"})
    try:
        data["most_recent_tweet"] = tweet.find("div", {"class", "tweet-content media-body"}).text
    except:
        data["most_recent_tweet"] = None

    #Image
    image = soup.find("div", {"class":"tweet-body"})
    try:
        data["image"] = image.find("a", {"class":"still-image"}).get("href")
    except:
        data["image"] = None

    #Video
    video = soup.find("div", {"class":"tweet-body"})
    try:
        data["video"] = video.find("div", {"class":"attachment video-container"}).text
    except: 
        data["video"] = None

    #Tweet Link 
    link = soup.find("div", {"class":"timeline"})
    try:
        data["link"] = link.find("a", {"class":"tweet-link"}).get("href")
    except:
        data["link"] = None

    #Quote Tweets
    quotetweet = soup.find("div", {"class":"tweet-body"})
    try: 
        data["quotetweeted"] = quotetweet.find("a", {"class":"quote-link"}).get("href")
    except:
        data["quotetweeted"] = None

    #Retweet
    retweet = soup.find("div", {"class":"tweet-body"})
    try:
        data["retweeted"] = retweet.find("div", {"class":"retweet-header"}).text
    except:
        data["retweeted"] = None
    try:
        data["retweet"] = retweet.find("div", {"class":"icon-container"}).text
    except:
        data["retweet"] = None
    
    #Data Manipulation
    parsed_data[0] = data

    for items in parsed_data:
        for keys in items:
            relayed_name = items["profile_name"]
            relayed_handle = items["profile_handle"]
            relayed_following = items["profile_following"]
            relayed_followers = items["profile_followers"]
            relayed_tweet = items["most_recent_tweet"]
            relayed_image = items["image"]
            relayed_video = items["video"]
            relayed_link = items["link"]
            relayed_quotetweeted = items["quotetweeted"]
            relayed_retweeted = items["retweeted"]
            relayed_retweet = items["retweet"]

    if relayed_quotetweeted != None:
        sent_tweet =  f"**{relayed_name}** ({relayed_handle}): {relayed_tweet}\nQuote Tweet: https://nitter.moomoo.me{relayed_quotetweeted}\nFollowing: {relayed_following} and Followers: {relayed_followers}"

    elif relayed_retweeted != None:
        sent_tweet = f"**{relayed_name}** ({relayed_handle}): :repeat:{relayed_retweet}\nRetweet: https://nitter.moomoo.me{relayed_link}\nFollowing: {relayed_following} and Followers: {relayed_followers}"
                    
    elif relayed_video != None:
        sent_tweet = f"**{relayed_name}** ({relayed_handle}): {relayed_tweet} https://nitter.moomoo.me{relayed_link}\nFollowing: {relayed_following} and Followers: {relayed_followers}"
                    
    elif relayed_image != None:                    
        sent_tweet = f"**{relayed_name}** ({relayed_handle}): {relayed_tweet} https://nitter.moomoo.me{relayed_image}\nFollowing: {relayed_following} and Followers: {relayed_followers}"

    else:
        sent_tweet = f"**{relayed_name}** ({relayed_handle}): {relayed_tweet}\nFollowing: {relayed_following} and Followers: {relayed_followers}"

    return sent_tweet
