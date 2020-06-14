#created by rayane866(rynpix)
import robloxapi, asyncio, logging

async def get_info():
	global bot_info, bot_id
	bot_info = await bot.get_self()
	bot_id = bot_info.id

async def rank_main(groupid, userid, rank):
	await asyncio.sleep(0.01)
	group = await bot.get_group(groupid)
	
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

	if not bot_valid:
		logging.warn(f"Bot is not a valid member the group:{groupid}")
	else:
		if not plr_valid:
			if not userid != bot_id:
				logging.warn("Attempt to change bot rank.")
			elif user_in_group:
				if not user_rank < bot_rank:
					logging.warn(f"Attempt to change higher rank player:{userid} rank.")
			else:
				logging.warn(f"User:{userid} is not valid member of the group:{groupid}.")

		if not rank_valid:
			if rank < 1 or rank > 255:
				logging.warn(f"Rank:{rank} is not valid.")
			elif not rank < bot_rank:
				logging.warn(f"Attempt to change user:{userid} rank to bot's rank or higher rank:{rank}.")
			else:
				logging.warn(f"Rank:{rank} is not valid.")

	if plr_valid and rank_valid and bot_valid:
		await group.set_rank_by_id(userid, rank)
		logging.info(f"Changed user:{userid} rank to :{rank} in group:{groupid}.")
	else:
		logging.warn(f"Failed to change user:{userid} rank to :{rank} in group:{groupid}.")



def rank(groupid, userid, rank):
	loop.run_until_complete(rank_main(groupid, userid, rank))


def main(cookie):
	global loop, bot
	logging.basicConfig(filename='bot.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
	bot = robloxapi.Client(cookie)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(get_info())
