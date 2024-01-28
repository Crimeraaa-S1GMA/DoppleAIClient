# DoppleAIClient


Python API wrapper for Dopple.AI


You can install it using pip with the `pip install dopple_ai_client` command.


## Example usage



```py
import dopple_ai_client

client = dopple_ai_client.DoppleClient("TOKEN", "EMAIL")

for bot in client.get_bots_chatted_with(): # Print out the bot IDs
    print(bot)
```


## How to get credentials


The token can be found in the "Authorization" parameter of any fetch request to ml.dopple.ai. Copy the token after the "Bearer" part, which you should ignore.


As for the e-mail, you should use the one you registered with for Dopple.AI.
