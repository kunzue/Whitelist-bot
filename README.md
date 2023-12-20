# Whitelisting Bot for Discord

This repository contains the source code for a Discord bot developed using discord.py. The bot is designed to manage whitelisting on your Discord server, ensuring only approved members have access to your server.

## Features

- Easy setup and use
- Clean and intuitive interface
- Ability to add or remove users from the whitelist
- Hybrid Commands: The bot supports both slash commands and normal commands. This means you can use the bot's commands both with a prefix (like !whitelist) and without a prefix (as a slash command).

## Installation

1. Create a new Discord application and bot. You can do this by visiting the [Discord Developer Portal](https://discord.com/developers/applications) and clicking on "New Application"
2. Install the [discord.py](https://github.com/Rapptz/discord.py) library by running `pip install discord.py`
3. Clone the repository: `git clone https://github.com/PixonGamer/Whitelist-bot`
4. Navigate to the cloned directory
5. Install the required dependencies: `pip install -r requirements.txt`
6. Follow the configuration guide below
7. Run `bot.py`

## Configuration

Before running the bot, you need to fill in the `config.py` file with your bot's token and other optional settings. Here's what you need to do:

1. Open the `config.py` file in your project directory.
2. Replace `'YOUR_BOT_TOKEN_HERE'` with your bot's token. This is the only necessary field.
3. The `prefix` field is optional and is pre-filled with `"!"`. You can change this to any prefix you prefer.
4. The `status` field is also optional and is pre-filled with `'Whitelist in action, only allowing trusted members.'`. You can change this to any status message you prefer.

After filling in the `config.py` file, you can run the bot.

Please note that you should keep your bot's token secret. Do not share it with anyone or publish it online. If your bot's token is compromised, someone else could use it to control your bot.

## Usage

The bot uses hybrid commands, which means you can use the bot's commands both with a prefix (like !whitelist) and without a prefix (as a slash command).

Once the bot is running, you can use the following commands:

- `!whitelist add user_id` or : Adds a user to the whitelist.
- `!whitelist remove user_ID`: Removes a user from the whitelist.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

If you have any questions or suggestions, feel free to open an issue.