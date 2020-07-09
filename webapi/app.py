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

@app.route("/bot/rank", methods = ["GET"])
def rank():
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
		bot.logger.error(f"invalid cookie: '{cookie}'\n.Try changing your cookie and restarting the server.")

	log = jsonify(bot.logger_config.log_list)
	bot.logger_config.log_list = []

	return log

@app.route("/bot/promote", methods = ["GET"])
def promote():
	if bot.logged:
		groupid = request.args.get("groupid", type=int)
		userid = request.args.get("userid", type=int)
		if groupid:
			bot.promote(groupid, userid)
		elif main_groupId:
			bot.promote(main_groupId, userid)
		else:
			bot.logger.warning("No group id found")
	else:
		bot.logger.error(f"invalid cookie: '{cookie}'\n.Try changing your cookie and restarting the server.")

	log = jsonify(bot.logger_config.log_list)
	bot.logger_config.log_list = []

	return log

@app.route("/bot/demote", methods = ["GET"])
def demote():
	if bot.logged:
		groupid = request.args.get("groupid", type=int)
		userid = request.args.get("userid", type=int)
		if groupid:
			bot.demote(groupid, userid)
		elif main_groupId:
			bot.demote(main_groupId, userid)
		else:
			bot.logger.warning("No group id found")
	else:
		bot.logger.error(f"invalid cookie: '{cookie}'\n.Try changing your cookie and restarting the server.")

	log = jsonify(bot.logger_config.log_list)
	bot.logger_config.log_list = []

	return log


@app.route("/bot/log")
def download_log():
	return send_file(log_name, as_attachment=True)


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)