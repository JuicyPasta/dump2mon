# Dump2Mon
======================
## Purpose
Twitter bot that proactively and retroactively monitors dumpmon in search of identifiable information.

## Usage
watchlist.txt - a list of strings you would like to keep an eye out for
```txt
emails
usernames
ip addresses
mac addresses
hostnames
```

keys.py - twitter api keys and email(gmail for now) credentials
```py
CONSUMER_KEY = '...'
CONSUMER_SECRET = '...'
ACCESS_TOKEN = '...'
ACCESS_TOKEN_SECRET = '...'

STREAM_KEY = '...'
STREAM_SECRET = '...'
GMAIL_USER = '...'
GMAIL_PASSWORD = '...'
```

Start the listener, start searching for identifiers, emails you if anything turns up.
```py
./listener.py
```
