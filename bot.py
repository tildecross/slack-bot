#!bot/bin/python3

import os
import sys
import time
from slackclient import SlackClient

if len(sys.argv) >= 2:
    BOT_NAME = sys.argv[1]
    BOT_ID = os.environ.get("SLACK_{0}_ID".format(
        BOT_NAME.upper()
    ))
    AT_BOT = "<@{0}>".format(BOT_ID)
    RUNNING = False
    
    def cmd_do(action):
        return "I will try to do *{0}*".format(action)
        
    def cmd_stop(action):
        global RUNNING
        RUNNING = False
        return "Process stopping..."
    
    COMMANDS = {
        "do": cmd_do,
        "stop": cmd_stop
    }
    
    slack_client = SlackClient(os.environ.get("SLACK_{0}_TOKEN".format(
        BOT_NAME.upper()
    )))

    def handle_command(command, channel):
        response = "I don't know what you mean. Try using: \n"
        for cmd, func in COMMANDS.items():
            response += "> *{0}*\n".format(cmd)
            
        command_split = command.split(" ")
        command_name = command_split[0].strip().lower()
        command_rest = None
        
        if len(command_split) > 1:
            command_rest = command_split[1].strip().lower()
        
        for cmd in COMMANDS:
            if not command.startswith(cmd):
                continue
            else:
                response = COMMANDS[command_name](command_rest)
                break
                
        slack_client.api_call("chat.postMessage", channel=channel,
            text=response, as_user=True)
    
    def parse_slack_output(slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and "text" in output and AT_BOT in output["text"]:
                    output_text = output["text"].split(AT_BOT)[1].strip().lower()
                    return output_text, output["channel"]
        return None, None
                
    if __name__ == "__main__":
        READ_WEBSOCKET_DELAY = 1 # 1 second
        if slack_client.rtm_connect():
            print("Tildex :: Zero connected and running")
            RUNNING = True
            
            while RUNNING:
                rtm_read = slack_client.rtm_read()
                command, channel = parse_slack_output(rtm_read)
                if command and channel:
                    handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("ERROR: Connection failed. Invalid token or id.")
