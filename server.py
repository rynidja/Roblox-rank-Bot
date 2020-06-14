#created by rayane866(rynpix)
from flask import Flask, request
import logging, bot

cookie = ""# your cookie here
groupId =  # your group id here

app = Flask(__name__)
bot.main(cookie)

@app.route("/bot/api", methods = ["GET"])
def BotApi():
	groupid = request.args.get("groupid", type=int)
	userid = request.args.get("userid", type=int)
	rank = request.args.get("rank", type=int)
	if userid and rank and not groupId:
		if groupid:
			bot.rank(groupid, userid, rank)
		else:
			logging.wan(f"No group id")
	elif userid and rank and groupId:
		bot.rank(groupId, userid, rank)

	return ""


if __name__ == '__main__':
	app.run()