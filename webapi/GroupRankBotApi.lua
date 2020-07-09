--[[
This is a module script
To use:
	local GroupRankBot = require(PATH TO THIS MODULE SCRIPT)
	GroupRankBot.url = "YOUR URL" --u can include "/"
	GroupRankBot.rank(userid, rank)
		
--]]

local GroupRankBot = {url=""}
local http_service = game:GetService("HttpService")

function get_output(output)
	for i, v in pairs(output) do
		local level = v["level"]
		local msg = v["msg"]
		
		if level == "INFO" then
			print(msg)
		elseif level == "WARNING" then
			warn(msg)
		elseif level == "ERROR" then
			error(msg.."\nCeck out "..GroupRankBot.url.."/bot/log for the log")
		end
	end
end

GroupRankBot.rank = function(userid, rank)
	local url = GroupRankBot.url.."/bot/rank?userid="..userid.."&rank="..rank
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

GroupRankBot.promote = function(userid)
	local url = GroupRankBot.url.."/bot/promote?userid="..userid
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

GroupRankBot.demote = function(userid)
	local url = GroupRankBot.url.."/bot/demote?userid="..userid
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

GroupRankBot.grank = function(groupid, userid, rank)
	local url = GroupRankBot.url.."/bot/rank?userid="..userid.."&rank="..rank.."&groupid="..groupid
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

GroupRankBot.gpromote = function(groupid, userid)
	local url = GroupRankBot.url.."/bot/promote?userid="..userid.."&groupid="..groupid
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

GroupRankBot.gdemote = function(groupid, userid)
	local url = GroupRankBot.url.."/bot/demote?userid="..userid.."&groupid="..groupid
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end


return GroupRankBot