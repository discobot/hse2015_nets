import sys
import uuid
import requests

SERVER_URL="http://localhost:8080"
USER="slon"

def post_message(text):
    msg_id = uuid.uuid4()
    for i in range(3):
        try:
            requests.post(SERVER_URL, data={
                "id": msg_id,
                "user": USER,
                "msg": text,
            })
        except requests.exceptions.ConnectionError:
            if i < 2:
                print "Post request failed, retrying"
            else:
                raise

def get_messages():
    for i in range(3):
        try:
            return requests.get(SERVER_URL).json()
        except requests.exceptions.ConnectionError:
            if i < 2:
                print "Get request failed, retrying"
            else:
                raise

if __name__ == "__main__":
    if sys.argv[1] == "get":
        print get_messages()
    elif sys.argv[1] == "post":
        post_message(sys.argv[2])
