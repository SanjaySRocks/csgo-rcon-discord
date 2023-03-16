import discord
from discord.ext import commands
import json
import valve.rcon


# Main Code
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # enable the Messages intent


with open('config.json', 'r') as f:
    config = json.load(f)

PREFIX = config['PREFIX']
TOKEN = config['TOKEN']
allowed_id = config['allowed_id']
RCON_CHANNEL = config['RCON_CHANNEL']

client = commands.Bot(command_prefix=PREFIX, intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.command()
async def rc(ctx, id:int = 1, *, command:str = 'status'):
        
        if ctx.author.id != int(allowed_id):
             return await ctx.send("You're are not authorized to access this command!")
        

        with open('servers.json', 'r') as f:
            servers = json.load(f)

        ip = servers['servers'][id-1]['ip']
        port = servers['servers'][id-1]['port']
        password = servers['servers'][id-1]['rcon']

        
        if password is None or password == "":
            return await ctx.send("rcon password not set for this server")

        if "rcon_password" in command:
            return

        await ctx.send(f"{ip}:{port} Command Sent!!!")

        server_address = (ip, int(port))

        try:
            with valve.rcon.RCON(server_address, password) as rcon: 
                res = rcon.execute(f'{command}')
                rcon_data = res.body.decode('utf-8', 'ignore')
            
            await ctx.send("```"+rcon_data+"```")
        except valve.rcon.RCONAuthenticationError as e: 
             print("Incorrect rcon password!")


client.run(config['TOKEN'])