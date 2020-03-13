from requests_oauthlib import OAuth1Session
import os
import json
import urllib
import credentials

twitter = OAuth1Session(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET,
                        credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
root_dir_name = "dir"


def get_dir_name():
    if not os.path.isdir(root_dir_name):
        os.mkdir(root_dir_name)
    i = 0
    while True:
        if not os.path.isdir(root_dir_name + "/dir" + str(i)):
            os.mkdir(root_dir_name + "/dir" + str(i))
            return "/dir" + str(i)
        i += 1


def get_tweets(params):
    # Premium search API Resource URL
    url = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json"
    return json.loads(twitter.get(url, params=params).text)['results']


def save_images_from_tweets(tweets, dir_name):
    print(tweets)
    i = 0
    saved_image_urls = []
    for tweet in tweets:
        try:
            for media in tweet['extended_entities']['media']:
                image_url = media['media_url']
                if image_url in saved_image_urls:
                    continue
                with open(root_dir_name + dir_name + '/image_' + str(i) + '_' + os.path.basename(image_url), 'wb') as f:
                    f.write(urllib.request.urlopen(image_url + ':orig').read())
                saved_image_urls.append(image_url)
                i += 1
            print('ツイートに含まれる画像を保存しました')
        except KeyError:
            print('画像を含まないツイートです')
        except:
            print('不明なエラーが発生しました')
    return


if __name__ == '__main__':
    params = {
        'query': ''
    }
    save_images_from_tweets(get_tweets(params), get_dir_name())
