import tweepy
from tweepy import OAuthHandler
from twarc import Twarc
import json
import time
 
consumer_key = 'YOUR CONSUMER KEY'
consumer_secret = 'YOUR CONSUMER SECRET'
 
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True)
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def scrape_data(word):
    data = []
    count = 0
    num_total_tweets = 10000
    back_off_counter = 1
    printProgressBar(0, num_total_tweets, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    try:
        for tweet in tweepy.Cursor(api.search, q = word, lan = 'en', show_user = False, wait_on_rate_limit=True, tweet_mode = 'extended').items(num_total_tweets):
            if(str(tweet.full_text.encode('utf-8')) + ' ~\n' not in data):
                tweet_text = str(tweet.full_text.encode('utf-8')).lower()
                if("sex" not in tweet_text):
                    data.append(str(tweet.full_text.encode('utf-8')) + ' ~\n')
            count += 1
            printProgressBar(count, num_total_tweets, prefix = 'Progress: ', suffix = 'Complete', length = 50)
    except tweepy.TweepError:
        time.sleep(60*back_off_counter)
        back_off_counter += 1

    print(str(len(data)) + " Unique Tweets Scraped")

    file_name = word + "_output.txt"
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def main():
    word = input("Keyword: ")
    scrape_data(word)

if __name__ == '__main__':
    main()