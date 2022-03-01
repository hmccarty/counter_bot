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

## Supported Counting Types

It's super easy to add types in `helpers/counts.py`, but the currently supported types are:

- `basic:` Single positive increments in base 10
- `backwards`: Single negative increments in base 10
- `binary`: Single positive increments in binary

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

---

To check your counting score:

```
.score
```

---

To check counting leaderboard:

```
.leaderboard
```