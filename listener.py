from tweepy import API, Stream, OAuthHandler, StreamListener, Cursor
import urllib.request
import urllib.error
from smtplib import SMTP
import re

from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from keys import GMAIL_USER, GMAIL_PASSWORD

WATCHLIST = 'watchlist.txt'
DUMPMON_USER_ID = '1231625892'


def main():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = API(auth)

    stream_listener = TwitterStreamListener()
    stream = Stream(auth=auth, listener=stream_listener)
    stream.filter(follow=[DUMPMON_USER_ID], async=True)

    for status in Cursor(api.user_timeline, id=DUMPMON_USER_ID).items():
        parse_status(status)


class TwitterStreamListener(StreamListener):
    def on_status(self, status):
        parse_status(status)

    def on_error(self, status_code):
        print(status_code)


def send_email(message, subject="DUMP2MON IDENTIFIER FOUND ========", message_from='dump2mon', message_to=GMAIL_USER):
    full_message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (message_from, message_to, subject, message)
    server = SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)
    server.sendmail(GMAIL_USER, GMAIL_USER, full_message)
    server.close()


# https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
def contains_str(string):
    string = string.decode('utf-8')
    if not hasattr(contains_str, 'watchlist'):
        contains_str.watchlist = [re.compile(s[:-1], re.IGNORECASE) for s in open(WATCHLIST, 'r').readlines()]

    return [s.pattern for s in contains_str.watchlist if s.search(string)]


def parse_status(status):
    url = re.search("(https://t.co/[a-zA-Z0-9]{10})", status.text).group(0)
    request = urllib.request.Request(url, method='GET')
    try:
        contains_list = contains_str(urllib.request.urlopen(request).read())
        if len(contains_list) > 0:
            send_email("found " + ','.join(contains_list) + " in " + url)
    except urllib.error.URLError as e:
        print(e)


if __name__ == "__main__":
    main()


