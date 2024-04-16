from TwitterAPI import TwitterAPI
from tkinter import *

# Your Twitter API credentials
api_key = 'Your API Key'
api_key_secret = 'Your API Key Secret'
access_token = 'Your Access Token'
access_token_secret = 'Your Access Token Secret'

# Create an instance of TwitterAPI with your credentials
api = TwitterAPI(api_key, api_key_secret, access_token, access_token_secret)

def display_account_details():
    # Get user details
    r = api.request('account/verify_credentials')
    if r.status_code == 200:
        user = r.json()
        account_details_label.config(text=f"Authenticated Account Details:\nName: {user['name']}\nUsername: {user['screen_name']}")
        print("Authenticated Account Details:")
        print("Name:", user['name'])
        print("Username:", user['screen_name'])
    else:
        account_details_label.config(text="Failed to fetch account details")
        print("Failed to fetch account details")

def follow_followers():
    # Follow all followers
    r = api.request('followers/list')
    if r.status_code == 200:
        followers = r.json()['users']
        for follower in followers:
            api.request('friendships/create', {'user_id': follower['id']})
        print("Followed everyone that is following")
    else:
        print("Failed to get followers:", r.text)

# Function to retrieve text from Entry 1
def getE1():
    return E1.get()

def mainFunction():
    # Retrieve values from GUI entry fields
    search = getE1()
    numberOfTweets = int(E2.get())
    phrase = E3.get()
    reply = E4.get().lower()
    retweet = E5.get().lower()
    favorite = E6.get().lower()
    follow = E7.get().lower()
    
    # Rest of the function code...


    if follow == "yes":
        follow_followers()

    if reply == "yes":
        # Reply to tweets
        r = api.request('search/tweets', {'q': search, 'count': numberOfTweets})
        if r.status_code == 200:
            tweets = r.json()['statuses']
            for tweet in tweets:
                tweetId = tweet['id']
                username = tweet['user']['screen_name']
                api.request('statuses/update', {'status': "@" + username + " " + phrase, 'in_reply_to_status_id': tweetId})
                print("Replied with " + phrase)
        else:
            print("Failed to search tweets:", r.text)

    if retweet == "yes":
        # Retweet tweets
        r = api.request('search/tweets', {'q': search, 'count': numberOfTweets})
        if r.status_code == 200:
            tweets = r.json()['statuses']
            for tweet in tweets:
                tweetId = tweet['id']
                api.request('statuses/retweet/:' + str(tweetId))
                print("Retweeted the tweet")
        else:
            print("Failed to search tweets:", r.text)

    if favorite == "yes":
        # Favorite tweets
        r = api.request('search/tweets', {'q': search, 'count': numberOfTweets})
        if r.status_code == 200:
            tweets = r.json()['statuses']
            for tweet in tweets:
                tweetId = tweet['id']
                api.request('favorites/create', {'id': tweetId})
                print("Favorited the tweet")
        else:
            print("Failed to search tweets:", r.text)

# GUI Setup
root = Tk()

label1 = Label(root, text="Search")
E1 = Entry(root, bd=5)

label2 = Label(root, text="Number of Tweets")
E2 = Entry(root, bd=5)

label3 = Label(root, text="Response")
E3 = Entry(root, bd=5)

label4 = Label(root, text="Reply?")
E4 = Entry(root, bd=5)

label5 = Label(root, text="Retweet?")
E5 = Entry(root, bd=5)

label6 = Label(root, text="Favorite?")
E6 = Entry(root, bd=5)

label7 = Label(root, text="Follow?")
E7 = Entry(root, bd=5)

submit_button = Button(root, text="Submit", command=mainFunction)

account_details_label = Label(root, text="Authenticated Account Details:\nName: \nUsername: ")
fetch_details_button = Button(root, text="Fetch Account Details", command=display_account_details)

label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
label4.pack()
E4.pack()
label5.pack()
E5.pack()
label6.pack()
E6.pack()
label7.pack()
E7.pack()
submit_button.pack()
fetch_details_button.pack()
account_details_label.pack()

root.mainloop()
