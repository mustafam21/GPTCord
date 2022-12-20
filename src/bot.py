import discord
import asyncio
from src import log, discord_client
from discord import app_commands
import openai
import json


# Initialize the logger
logger = log.setup_logger(__name__)

def get_config() -> dict:
    import os
    # get config.json path
    config_dir = os.path.abspath(__file__ + "/../../")
    config_name = 'config.json'
    config_path = os.path.join(config_dir, config_name)

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config

# Get the config data
config = get_config()

openai.api_key = config['openAI_key']

# Set the default value for the isPrivate variable
is_private = False

async def send_message(message, user_message):
    """Send a response to a user's message."""
    # Make the response ephemeral (visible only to the sender) if is_private is set to True
    await message.response.defer(ephemeral=is_private)
    try:
        # Build the response message
        response = f"> **{user_message}** - <@{message.user.id}>\n\n"
        # Use asyncio to run the `handle_response` function concurrently
        response += await asyncio.create_task(handle_response(user_message))
        # If the response is too long, split it into smaller chunks and send them separately
        if len(response) > 1900:
            if "```" in response:
                # Split the response if the code block exists
                parts = response.split("```")
                # Send the first message
                await message.followup.send(parts[0])
                # Send the code block in a separate message
                code_block = parts[1].split("\n")
                formatted_code_block = ""
                # Split long lines into smaller chunks
                for line in code_block:
                    while len(line) > 1900:
                        # Split the line at the 50th character
                        formatted_code_block += line[:1900] + "\n"
                        line = line[1900:]
                    formatted_code_block += line + "\n"  # Add the line and separate with new line
                if (len(formatted_code_block) > 2000):
                    code_block_chunks = [
                        formatted_code_block[i : i + 1900]
                        for i in range(0, len(formatted_code_block), 1900)
                    ]
                    for chunk in code_block_chunks:
                        await message.followup.send(f"```{chunk}```")
                else:
                    await message.followup.send(f"```{formatted_code_block}```")
                # Send the remaining of the response in another message
                if len(parts) >= 3:
                    await message.followup.send(parts[2])
            else:
                response_chunks = [
                    response[i : i + 1900] for i in range(0, len(response), 1900)
                ]
                for chunk in response_chunks:
                    await message.followup.send(chunk)
        else:
                    await message.followup.send(response)
    except Exception as e:
        await message.followup.send("> **Error: Something went wrong, please try again later!**")
        logger.exception(f"Error while sending message: {e}")



async def handle_response(message) -> str:

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.75,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # remove newline characters
    responseMessage = response.choices[0].text.strip()

    return responseMessage



def run_discord_bot():
    client = discord_client.DiscordClient()

    @client.event
    async def on_ready():
        await client.tree.sync()
        logger.info(f"{client.user} is now running!")

    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' in {channel}"
        )
        await send_message(interaction, user_message)

    
    

    TOKEN = config['discord_bot_token']
    client.run(TOKEN)
