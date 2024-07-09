# DoppleAIClient


Python API wrapper for Dopple.AI


You can install it using pip with the `pip install dopple_ai_client` command.


## Example usage



```py
import dopple_ai_client

client = dopple_ai_client.DoppleClient(email="EMAIL/USERNAME", password="PASSWORD")

for bot in client.get_user_chat_dopple_ids(): # Print out the bot IDs
    print(bot)
```


## Planned features


This library is actively maintained, and will add new features over time. Here are some of the planned things:

- Editing Dopples (possibly creating them too)
- Support for Dopple Reactions and Dopple Voice
- Utility functions
