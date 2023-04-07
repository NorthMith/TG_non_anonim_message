Anonymous(not) Message Forwarding Telegram Bot
=========================================

This Telegram bot allows users to send anonymous messages to the specified administrator. It forwards the user's message to the administrator's chat, either displaying the user's username (if available) or their first name. If the user doesn't have a username, the bot also provides a button with the user's ID that directs to their profile. Additionally, the bot allows the administrator to block or unblock users directly from the chat.

Features
--------

1. Forward anonymous messages from users to the administrator.
2. Display either the username or first name of the sender.
3. Provide a button with the user's ID to navigate to their profile when a username is not available.
4. Allow the administrator to block or unblock users directly from the chat.

Usage
-----

1. Replace the `TOKEN` and `ADMIN_CHAT_ID` values in the `config.py` file with your bot's token and desired administrator ID.
2. Deploy the bot on a server or run it locally.
3. Users can start a chat with the bot and send messages, which will be forwarded to the specified administrator.
4. The administrator can block or unblock users by interacting with the inline buttons provided in the chat.
