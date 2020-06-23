#created by rayane866(rynpix)
import robloxapi, asyncio, logger_config

async def get_info():
	global bot_info, bot_id, bot_name
	bot_info = await bot.get_self()
	bot_id = bot_info.id
	bot_name = bot_info.name

async def rank_main(groupid:int, userid:int, rank:int):
	await asyncio.sleep(0.01)
	try:
		group = await bot.get_group(groupid)
	except:
		logger.error(f"group[{groupid}] is not valid.")
		return None
	
	try:
		bot_role = await group.get_role_in_group(bot_id)
		bot_rank = bot_role.rank
		bot_valid = True
	except:
		bot_valid = False

	plr_valid = False
	user_in_group = False
	rank_valid = False

	async for member in group.get_members():
		if userid == member.id and userid != bot_id and bot_valid:
			user_role = await group.get_role_in_group(userid)
			user_rank = user_role.rank
			if user_rank < bot_rank:
				user_in_group = True
				plr_valid = True
				break			

	group_roles = await group.get_group_roles()
	for role in group_roles:
		if bot_valid:
			if rank == role.rank and rank < bot_rank:
				rank_valid = True
				break
		else:
			break
	
	user_info = await bot.get_user_by_id(userid)
	user_name = user_info.name

	if not bot_valid:
		logger.warning(f"Bot is not a valid member the group[{groupid}].")
	else:
		if not plr_valid:
			if not userid != bot_id:
				logger.warning("Attempt to change bot rank.")
			elif user_in_group:
				if not user_rank < bot_rank:
					logger.warning(f"Attempt to change higher rank player:{user_name}[{userid}] rank[{user_rank}].")
			else:
				logger.warning(f"{user_name}[{userid}] is not valid member of the group[{groupid}].")

		if not rank_valid:
			if rank < 1 or rank > 255:
				logger.warning(f"Rank[{rank}] is not valid.")
			elif not rank < bot_rank:
				logger.warning(f"Attempt to change {user_name}]{userid}] rank to bot's rank or higher rank[{rank}].")
			else:
				logger.warning(f"Rank[{rank}] is not valid.")

	if plr_valid and rank_valid and bot_valid:
		await group.set_rank_by_id(userid, rank) 
		await asyncio.sleep(0.01)

		plr_grole = await group.get_role_in_group(userid)
		plr_role = plr_grole.name
		plr_rank = plr_grole.rank

		if plr_rank == rank:
			logger.info(f"successfully ranked {user_name}[{userid}] to {plr_role}[{rank}] in group[{groupid}].")
		else:
			logger.warning(f"Failed to rank {user_name}[{userid}] to [{rank}] in group[{groupid}].")
	else:
		logger.warning(f"Failed to rank {user_name}[{userid}] to [{rank}] in group[{groupid}].")



def rank(groupid:int, userid:int, rank:int):
	if (type(groupid) is int) and (type(userid) is int) and (type(rank) is int):
		loop.run_until_complete(rank_main(groupid, userid, rank))
	else:
		if not groupid:
			logger.warning(f"Invalid group id[{groupid}].")
		if not userid:
			logger.warning(f"Invalid userid[{userid}].")
		if not rank:
			logger.warning(f"Invalid rank[{rank}].")

def main(log_name, max_lines, cookie:str):
	global logger, logged,loop, bot
	logger_config.main(log_name, max_lines)
	logger = logger_config.logger
	try:
		bot = robloxapi.Client(cookie)
		logged = True
	except:
		logged = False
		logger.error(f"invalid cookie: '{cookie}'")

	if logged:
		loop = asyncio.get_event_loop()
		loop.run_until_complete(get_info())
		logger.info(f"Logged in as: {bot_name}")
	logger_config.log_list = []