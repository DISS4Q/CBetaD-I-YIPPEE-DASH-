import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)
    #Example: DISS: ?add 23 9 BOTkibidideidad: 32

@bot.command()
async def multiply(ctx, left: float, right: float):
    """Multiplies two numbers."""
    result = left * right
    await ctx.send(f"{left} × {right} = {result}")

@bot.command()
async def subtract(ctx, left: float, right: float):
    """Subtracts the second number from the first."""
    result = left - right
    await ctx.send(f"{left} - {right} = {result}")

@bot.command()
async def divide(ctx, numerator: float, denominator: float):
    """Divides one number by another."""
    if denominator == 0:
        await ctx.send("❌ No se puede dividir entre 0.")
        return

    result = numerator / denominator
    await ctx.send(f"{numerator} ÷ {denominator} = {result}")

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)
    #Example: DISS: ?roll 2d9 BOTkibidideidad: 1, 9

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))
    #Example: DISS: ?choose pizza hamburguesa tacos. BOTkibidideidad: tacos



@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
    #Example: DISS: ?repeat 3 hola BOTkibidideidad: hola hola hola


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')
    #Example: DISS: ?joined @Usuario BOTkibidideidad: Usuario joined June 5, 2024 3:15 PM

bot.run('TOKEN')
