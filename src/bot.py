#created by rayane866(rynpix)
import robloxapi, asyncio, logger_config

async def get_info():
    '''Getting bot's info'''
    global bot_info, bot_id, bot_name
    bot_info = await bot.get_self()
    bot_id = bot_info.id
    bot_name = bot_info.name

async def bot_group_info(groupid):
    '''Check if bot is a valid member of the group and if group exists.'''
    try:
        group = await bot.get_group(groupid)
        try:
            bot_role = await group.get_role_in_group(bot_id)
            bot_rank = bot_role.rank
            return True, group, bot_rank
        except:
            logger.error(f"Bot is not a valid member the group[{groupid}].")
            return False, group, None
    except robloxapi.utils.errors.NotFound:
            logger.error(f"group[{groupid}] is not valid.")
            return False, None, None
    except robloxapi.utils.errors.BadStatus:
            logger.warning(f"Failed to load group[{groupid}]")
            await asyncio.sleep(0.01)
            logger.info(f"Retrying to load group[{groupid}]")
            return await bot_group_info(groupid)
    
async def user_check(group, userid, bot_rank, rankChange=None):
    '''Check if the user is a valid member of the group and get his info'''
    user_info = await bot.get_user_by_id(userid)
    if user_info:
        async for member in group.get_members():
            if userid == member.id:
                user_grole = await group.get_role_in_group(userid)
                user_rank = user_grole.rank
                if userid != bot_id:
                    if user_rank < bot_rank :
                        return True, user_info.name, user_rank, user_grole.name
                    elif not rankChange:
                        logger.warning(f"Attempt to change a higher rank player:{user_info.name}[{userid}] rank[{user_rank}].")
                    elif rankChange:
                        logger.warning(f"Attempt to Kick a higher rank player:{user_info.name}[{userid}] rank[{user_rank}].")
                    return False, user_info.name, user_rank, user_grole.name

                elif userid == bot_id:
                    if not rankChange:
                        logger.warning("Attempt to change bot rank.")
                    return False, user_info.name, user_rank, user_grole.name
        logger.warning(f"{user_info.name}[{userid}] is not valid member of the group[{group.id}].")
        return False, user_info.name, None, None
    logger.warning(f"Invalid user [{userid}].")
    return False, None, None, None

async def mote_check(groupid, userid):
    '''Do checks for remote and demote funcions'''
    await asyncio.sleep(0.01)
    stat, group, bot_rank = await bot_group_info(groupid)
    plr_valid = False

    if stat:
        plr_valid, plr_name, plr_rank, _ = await user_check(group, userid, bot_rank)        
        groles = await group.get_group_roles()
        roles={role.name : role.rank for role in groles}
    else:
        user_info = await bot.get_user_by_id(userid)
        if user_info:
            plr_name = user_info.name
        else:
            logger.warning(f"Invalid user [{userid}].")
            plr_name = None

    return stat, group, plr_valid, plr_name, plr_rank, roles

async def rank_main(groupid:int, userid:int, rank:int):
    '''rank func main'''
    await asyncio.sleep(0.01)
    stat, group, bot_rank = await bot_group_info(groupid)
    plr_valid = False
    rank_valid = False

    if stat:
        plr_valid, plr_name, plr_rank, _ = await user_check(group, userid, bot_rank)        

        roles={}
        groles = await group.get_group_roles()
        for role in groles:
            if role.rank < bot_rank and rank == role.rank and rank!=0:
                rank_valid = True
            roles.update({role.name : role.rank})

        if not rank_valid:
            if not rank > 0 or not rank < 255 :
                logger.warning(f"Invalid rank[{rank}].")
            elif not rank < bot_rank:
                logger.warning(f"Attempt to change {plr_name}[{userid}] rank to bot's rank or higher rank[{rank}].")
            else:
                logger.warning(f"Invalid rank[{rank}].")

    else:
        user_info = await bot.get_user_by_id(userid)
        if user_info:
            plr_name = user_info.name
        else:
            logger.warning(f"Invalid user [{userid}].")
            plr_name = None

    if plr_valid and rank_valid and stat:
        if not plr_rank == rank:
            r = await group.set_rank_by_id(userid, rank)
            if r == 200:
                logger.info(f"successfully ranked {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(rank)]}[{rank}] in group[{groupid}].")
            else:
                logger.warning(f"Failed to rank {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(rank)]}[{rank}] in group[{groupid}].")
        else:
            logger.info(f"{plr_name}[{userid}] is already {list(roles.keys())[list(roles.values()).index(rank)]}[{rank}] in group[{groupid}].")
    else:
        logger.warning(f"Failed to rank {plr_name}[{userid}] to [{rank}] in group[{groupid}].")

async def promote_main(groupid, userid):
    """Promote main"""
    await asyncio.sleep(0.01)
    stat, group, plr_valid, plr_name, plr_rank, roles = await mote_check(groupid, userid)

    if stat and plr_valid:
        try:
            await group.promote(userid)
            logger.info(f"Successfully promoted {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(plr_rank)+1]}[{list(roles.values())[list(roles.values()).index(plr_rank)+1]}] in group[{groupid}].")
        except:
            logger.warning(f"Can't promote {plr_name}[{userid}] to bots rank or higher [{list(roles.keys())[list(roles.values()).index(plr_rank)+1]}[{list(roles.values())[list(roles.values()).index(plr_rank)+1]}]] in group[{groupid}].")
            logger.warning(f"Failed to promote {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(plr_rank)+1]}[{list(roles.values())[list(roles.values()).index(plr_rank)+1]}] in group[{groupid}].")
    else:
        logger.warning(f"Failed to promote {plr_name}[{userid}] in group[{groupid}].")

async def demote_main(groupid, userid):
    """Demote main"""
    await asyncio.sleep(0.01)
    stat, group, plr_valid, plr_name, plr_rank, roles = await mote_check(groupid, userid)

    if stat and plr_valid:
        try:
            await group.demote(userid)
            logger.info(f"Successfully demoted {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(plr_rank)-1]}[{list(roles.values())[list(roles.values()).index(plr_rank)-1]}] in group[{groupid}].")
        except:
            logger.warning(f"Can't demote {plr_name}[{userid}] to [{list(roles.keys())[list(roles.values()).index(plr_rank)-1]}[{list(roles.values())[list(roles.values()).index(plr_rank)-1]}]] in group[{groupid}].")
            logger.warning(f"Failed to demote {plr_name}[{userid}] to {list(roles.keys())[list(roles.values()).index(plr_rank)-1]}[{list(roles.values())[list(roles.values()).index(plr_rank)-1]}] in group[{groupid}].")
    else:
        logger.warning(f"Failed to demote {plr_name}[{userid}] in group[{groupid}].")

def rank(groupid=None, userid=None, rank=None):
    """Ranking func"""
    if (type(groupid) is int) and (type(userid) is int) and (type(rank) is int):
        loop.run_until_complete(rank_main(groupid, userid, rank))
    else:
        if not groupid:
            logger.warning(f"Invalid group id[{groupid}].")
        if not userid:
            logger.warning(f"Invalid userid[{userid}].")
        if not rank:
            logger.warning(f"Invalid rank[{rank}].")

def promote(groupid=None, userid=None):
    """Promote func"""
    if (type(groupid) is int) and (type(userid) is int):
        loop.run_until_complete(promote_main(groupid, userid))
    else:
        if not groupid:
            logger.warning(f"Invalid group id[{groupid}].")
        if not userid:
            logger.warning(f"Invalid userid[{userid}].")

def demote(groupid=None, userid=None):
    """Demote func"""
    if (type(groupid) is int) and (type(userid) is int):
        loop.run_until_complete(demote_main(groupid, userid))
    else:
        if not groupid:
            logger.warning(f"Invalid group id[{groupid}].")
        if not userid:
            logger.warning(f"Invalid userid[{userid}].")

def main(log_name, max_lines, cookie:str):
    """The main func"""
    global logger, logged,loop, bot
    logger_config.main(log_name, max_lines)
    logger = logger_config.logger
    if cookie:
        try:
            bot = robloxapi.Client(cookie)
            logged = True
        except:
            logged = False
            bot.logger.error(f"invalid cookie: '{cookie}'\n.Try changing your cookie and restarting the server.")
    else:
        bot.logger.error(f"invalid cookie: '{cookie}'\n.Try changing your cookie and restarting the server.")
    if logged:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_info())
        logger.info(f"Logged in as: {bot_name}")
    logger_config.log_list = []
