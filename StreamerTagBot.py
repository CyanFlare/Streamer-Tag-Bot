import discord
import asyncio
import config

client = discord.Client()
    
@client.event
async def on_ready():
    print("Streamer Tag Bot Online!")
    print("Scanning for users that are streaming.\n\n")

def titleEnabled(members):
    if config.enableTitle is True:
        return config.title in str(members.activities)
    else:
        return True

def gameEnabled(members):
    game = "name=\'" + config.gameName + "\'"
    if config.enableGame is True:
        return game in str(members.activities)
    else:
        return True

async def twitchCheck():
    await client.wait_until_ready()
    guild = client.get_guild(config.guildID)
    role = discord.utils.get(guild.roles, id=config.roleID)
    while not client.is_closed():
        try:
            guildMembers = guild.members
            for members in guildMembers:
                isStreaming = "Streaming" in str(members.activities)
                hasRole = role in members.roles
                isBot = members.bot is True
  
                if ((titleEnabled(members) and gameEnabled(members)) and isStreaming) and not hasRole and not isBot:
                    print("Added role to " + str(members.name))
                    await members.add_roles(role)
                if ((not titleEnabled(members) or not gameEnabled(members)) or not isStreaming) and hasRole and not isBot:
                    print("Removed role from " + str(members.name))
                    await members.remove_roles(role)
                        
            await asyncio.sleep(config.updateDelay)
        except Exception as e:
            print(e)
            await asyncio.sleep(1)

client.loop.create_task(twitchCheck())
client.run(config.botToken)
