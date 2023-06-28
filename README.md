# Waifus Paradise

This repository contains my Discord bot written in python, with various functionalities, including displaying artwork from multiple websites, music commands, and moderation commands such as muting, unmuting, banning, kicking, and clearing messages.

## Features

### Art
- `!art` - Displays a random sfw art.
- `!r34 <tag>` - Displays a random artwork from the rule34.

### Music Commands
The bot can play music in voice channels. It supports the following commands:
- `!play <song>` - Plays the specified song in the voice channel or adds it to queue if one is already playing.
- `!pause` - Pauses the currently played song.
- `!resume` - Resumes the paused song.
- `!stop` - Stops playing music and clears the queue.
- `!skip` - Skips the currently playing song.
- `!queue` - Displays the current music queue.

### Moderation Commands
The bot has moderation capabilities to manage the server. It supports the following commands:
- `!mute <user> <duration> <reason>` - Mutes the specified user for the given duration with the provided reason.
- `!unmute <user> <reason>` - Unmutes the specified user with the provided reason.
- `!ban <user> <reason>` - Bans the specified user from the server with the provided reason.
- `!kick <user> <reason>` - Kicks the specified user from the server with the provided reason.
- `!clear <number>` - Deletes the specified number of messages from the channel.

## Installation

To use this bot, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `python -m pip install -r requirements.txt`.
3. Create a new Discord bot and obtain the bot token.
4. Customize the bot's behavior and settings in the `config.py` file.
5. Make sure that you are in the directory the bot is installed in.
6. Start the bot by running `python Waifus_Paradise.py`.

## Configuration

The `config.py` file contains various settings that can be customized according to your needs. Modify the values to configure the bot's behavior, such as the bot token and more.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
