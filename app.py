#created by rayane866(rynpix)
from flask import Flask, request, jsonify, send_file
import json, bot

with open("settings.json", "r") as json_file:
	settings = json.load(json_file)

cookie = settings["cookie"]
main_groupId = settings["MainGroupId"]
log_name = settings["log_name"]
max_log_lines = settings["max_log_lines"]

bot.main(log_name, max_log_lines, cookie)

app = Flask(__name__)

@app.route("/bot/ranker", methods = ["GET"])
def ranker():
	if bot.logged:
		groupid = request.args.get("groupid", type=int)
		userid = request.args.get("userid", type=int)
		rank = request.args.get("rank", type=int)
		if groupid:
			bot.rank(groupid, userid, rank)
		elif main_groupId:
			bot.rank(main_groupId, userid, rank)
		else:
			bot.logger.warning("No group id found")
	else:
		bot.logger.error(f"invalid cookie: '{cookie}'")

	log = jsonify(bot.logger_config.log_list)
	bot.logger_config.log_list = []

	return log

@app.route("/bot/log")
def download_log():
	return send_file(log_name, as_attachment=True)


if __name__ == '__main__':
	app.run(host="0.0.0.0")