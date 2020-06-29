--[[
This is a module script
To use:

	local GroupRankBot = require(PATH TO THIS MODULE SCRIPT)
	GroupRankBot.url = "YOUR URL"
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
			print("Ceck out "..GroupRankBot.url.."/bot/log for the log")
			error(msg)
		end
	end
end

GroupRankBot.rank = function(userid, rank)
	local url = GroupRankBot.url.."/bot/ranker?userid="..userid.."&rank="..rank
	local response = http_service:GetAsync(url)
	local output = http_service:JSONDecode(response)	
	get_output(output)
end

return GroupRankBot
