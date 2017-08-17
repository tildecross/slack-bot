#!bot/bin/python3

import os
import sys
from slackclient import SlackClient

if len(sys.argv) >= 2:
    BOT_NAME = sys.argv[1]

    slack_client = SlackClient(os.environ.get("SLACK_{0}_TOKEN".format(
        BOT_NAME.upper()
    )))

    if __name__ == "__main__":
        api_call = slack_client.api_call("users.list")
        if api_call.get("ok"):
            users = api_call.get("members")
            for user in users:
                if "name" in user and user.get("name") == BOT_NAME:
                    print("Bot ID for {0} is {1}".format(
                        user["name"], user.get("id")))
        else:
            print("Could not find your bot")
else:
    print("Missing arguments")
