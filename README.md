# Discord Counting Bot

Tired of robots taking your jobs? Want payback?

Take their jobs (with the assistance of this one additional bot)!

## Setup

Invite your bot on servers using the following invite:
https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot&permissions=67648

Configuration handled in `config.json`:

| Variable           | Definition                                                            |
| ------------------ | ----------------------------------------------------------------------|
| bot_prefix         | Indicator of a bot command (default: ".")                             |
| bot_token          | Discord token application                                             |
| db                 | Database file location (default: "./bot.db)                           |
| application_id     | Provided by discord                                                   |
| permissions        | Permissions integer assigned to bot                                   |

<br />

Before running the bot, install required dependencies:

```
pip install -r requirements.txt
```

Then start the bot using the following command:

```
python bot.py
```

## How to set up

To set up the bot I made it as simple as possible. I now created a [config.json](config.json) file where you can put the
needed things to edit.

Here is an explanation of what everything is:

| Variable                  | What it is                                                            |
| ------------------------- | ----------------------------------------------------------------------|
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands                        |
| YOUR_BOT_TOKEN_HERE       | The token of your bot                                                 |
| YOUR_BOT_PERMISSIONS_HERE | The permissions integer your bot needs when it gets invited           |
| YOUR_APPLICATION_ID_HERE  | The application ID of your bot                                        |
| OWNERS                    | The user ID of all the bot owners                                     |

In the [blacklist](blacklist.json) file you now can add IDs (as integers) in the `ids` list.

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
pip install -r requirements.txt
```

If you have multiple versions of python installed (2.x and 3.x) then you will need to use the following command:

```
python3 bot.py
```

or eventually

```
python3.8 bot.py
```

<br>

If you have just installed python today, then you just need to use the following command:

```
python bot.py
```

## Supported Counting Types

It's super easy to add types in `helpers/counts.py`, but the currently supported types are:

- "basic": Single positive increments
- "backwards": Single negative increments

## Usage

To add a counting channel:

```
.createchannel #channel-to-set <type> <starting-count (optional)> <starting-score (optional>
```

Starting counting is where the counting begins and score is initial score to set for the channel. You should only use starting score if you have been counting before adding bot.

As an example:
```
.createchannel #counting basic 1 0
```