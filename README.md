# slack-bot
Template for a Slack bot written in Python 3

```bash
python3 -m venv bot
bot/bin/pip3 install slackclient
chmod a+x bot.py
chmod a+x get_bot_id.py
export SLACK_<BOT_NAME>_ID=`bot/bin/python3 get_bot_id.py`
export SLACK_<BOT_NAME>_TOKEN=<BOT_TOKEN_HERE>
./bot.py <BOT_NAME>
```
