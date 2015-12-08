# Introduction #

Adding new behaviour to gucs-bot is _easy_! The `callbacks` class allows you to register callbacks to the bot, which are executed when a `PRIVMSG` matches a given pattern.

# Callbacks #

To add a callback, add a tuple to the 'callback\_list.' The first element of the tuple should be a valid python regular expression to match an incoming message you want the bot to react to. The second element of the tuple should be the name of the 'callback function' to execute when this regular expression is matched.

Example:

```
callback_list = [("(p|P)roblem\?", umad), ... ]
```

Where the messages "problem?" or "Problem?" sent to a channel would trigger the 'umad' callback function.

Any callback function should accept as parameters a Bot instance, and a dictionary containing message data.

The Bot instance allows the use of the functions in the instance of the 'bot' class the message was received from. Crucially, it allows a message to be sent back to the channel.

The data dictionary contains information about the message received that matched the regular expression. It is structured as follows:

```
data = {"to", "from", "message"}
```

Where the 'to' entry is the channel the message was sent to, 'from' is the sending user, and 'message' is the message that they sent to the channel. This allows the response message to be sent the to the appropriate channel (if the bot should respond.)

Example:

```
def echo(bot, data):
    bot.send("%s: %s" % (data["from"], data["message"]), channel = data["to"])
```