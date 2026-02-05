import discord
import os
from freecell import FreeCell

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

games = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_id = message.channel.id

    if message.content.startswith('$deal'):
        games[channel_id] = FreeCell()
        await message.channel.send('New FreeCell game started!')
        await message.channel.send(games[channel_id].get_game_state())

    if message.content.startswith('$board'):
        if channel_id in games:
            await message.channel.send(games[channel_id].get_game_state())
        else:
            await message.channel.send('No game in progress. Start a new game with `$deal`.')

    if message.content.startswith('$move'):
        if channel_id in games:
            try:
                parts = message.content.split()
                if len(parts) == 3:
                    _, from_col, to_col = parts
                    games[channel_id].move(from_col, to_col)
                elif len(parts) == 4:
                    _, from_col, card_index, to_col = parts
                    games[channel_id].move(from_col, to_col, int(card_index))
                else:
                    await message.channel.send("Invalid move command. Use `$move <from> <to>` or `$move <from> <card_index> <to>`.")
                    return

                await message.channel.send(games[channel_id].get_game_state())
                if games[channel_id].check_win():
                    await message.channel.send('Congratulations! You won!')
                    del games[channel_id]
            except ValueError as e:
                await message.channel.send(f"Invalid move: {e}")
            except Exception as e:
                await message.channel.send(f"An error occurred: {e}")
        else:
            await message.channel.send('No game in progress. Start a new game with `$deal`.')

# Replace "YOUR_DISCORD_TOKEN" with your actual Discord bot token
token = os.getenv('DISCORD_TOKEN')
print(token)
if not token:
    print("Error: DISCORD_TOKEN environment variable not set.")
    exit
client.run(token)
