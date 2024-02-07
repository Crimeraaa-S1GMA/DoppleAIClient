# DoppleAIClient


Python API wrapper for Dopple.AI


You can install it using pip with the `pip install dopple_ai_client` command.


## Example usage



```py
import dopple_ai_client

client = dopple_ai_client.DoppleClient("TOKEN", "USER_ID")

for bot in client.get_bots_chatted_with(): # Print out the bot IDs
    print(bot)
```


## How to get credentials - step by step


To use this API wrapper, you'll need your Dopple.AI user token and user ID. This is required in order to authenticate you correctly. Don't worry, all the requests are made ONLY to dopple.ai and nowhere else.


Here are the steps you need to follow in order to 


- Open the browser console
- Select the network tab. Preferably filter the requests shown to XHR/Fetch.
- Open [the site](https://beta.dopple.ai). Sign out of your account if you're logged in.
- Sign in again, this time with the network tab looking for fetch requests.
- Find a request to `https://be.dopple.ai/api/users/login`, `https://be.dopple.ai/api/users/google`, etc. Depends on how you signed in.
- Obtain the accessToken and id values from the JSON response and paste them into a DoppleClient object.
- All done! Now you can freely access the Dopple.AI API from Python.


## Planned features


This library is actively maintained, and will add new features over time. Here are some of the planned things:

- Find a better way of obtaining Dopple info. Right now the metadata is scraped from an HTML page, which has performance implications and isn't very tidy.
- Add the ability sign-in with e-mail and password.
- Editing Dopples (possibly creating them too)
- Support for Dopple Reactions and Dopple Voice
- Utility functions
