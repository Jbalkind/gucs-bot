import subprocess

print subprocess.call(["python", "bot.py",
                       "-sirc.freenode.org", "-ngucs-bot", "##gucs"])
