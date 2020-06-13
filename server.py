#created by rayane866(rynpix)
from flask import Flask, request
import bot

cookie = ""# your cookie here
groupId =  # your group id here

app = Flask(__name__)
bot.main(cookie)

@app.route("/bot/api", methods = ["GET"])
def BotApi():
	userid = request.args.get("userid", type=int)
	rank = request.args.get("rank", type=int)
	if userid and rank:
		bot.rank(groupId, userid, rank)

	return ""


if __name__ == '__main__':
	app.run()