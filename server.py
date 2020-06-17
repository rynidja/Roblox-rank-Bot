#created by rayane866(rynpix)
from flask import Flask, request
import logging, bot

cookie = "" # your cookie here
groupId = None # your group id here(instead of "None")[NOT REQUIRED]

try:
	bot.main(cookie)
except:
	pass

app = Flask(__name__)

@app.route("/bot/ranker", methods = ["GET"])
def BotApi():
	groupid = request.args.get("groupid", type=int)
	userid = request.args.get("userid", type=int)
	rank = request.args.get("rank", type=int)
	if userid and rank and groupid:
		bot.rank(groupid, userid, rank)
	elif userid and rank and groupId:
		bot.rank(groupId, userid, rank)
	else:
		if not userid:
			logging.warning(f"Invalid userid:{userid}.")
		if not rank:
			logging.warning(f"Invalid rank:{rank}.")
		if not (groupid or groupId):
			logging.warning("Invalid group id.")	

	return ""


if __name__ == '__main__':
	app.run(host="0.0.0.0")