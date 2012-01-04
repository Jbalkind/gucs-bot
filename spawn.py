import subprocess

print subprocess.call(["python", "gucs-bot/bot.py",
                       "-sirc.freenode.org", "-nguts-bot", "##gucs"])
