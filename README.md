# Anthony Commission

## Getting Started
- First, you need to setup the bot on [Discord Developer Portal](https://discord.com/developers/applications)
    - Click on "New Application" towards the top right of your screen.
    - Name it whatever you want and accept the Terms of Service.
    - Click "Bot" and "Reset Token". Place token in "TOKEN" section of config.yml.
    - Scroll down and enable "PRESENCE INTENT", "SERVER MEMBERS INTENT", and "MESSAGE CONTENT INTENT"
    - Click "OAuth2" and choose "bot" and "applications.commands". Select "Administrator" as the bot does not check permissions.
    - Copy link, paste in web browser and invite bot to server.
- Next, you need to install the required packages.
    - Simply run `pip install -r requirements.txt` in a Command Prompt/Terminal window.
- Lastly, fill out the config to your liking and run the bot.