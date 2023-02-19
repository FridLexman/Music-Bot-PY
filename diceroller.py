from discord import *                                                             
from discord.ext import commands
import random
import re

class diceroller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='roll')
    async def roll(self, ctx, dice_string: str):
        match_plus = re.match(r"(\d+)d(\d+)\+(\d+)", dice_string)
        match = re.match(r"(\d+)d(\d+)", dice_string)
        if match_plus:
            num_dice = int(match_plus.group(1))
            num_sides = int(match_plus.group(2))
            modifier = int(match_plus.group(3))
            total = modifier
            for _ in range(num_dice):
                roll = random.randint(1, num_sides)
                total += roll
            await ctx.send(f'Rolled {dice_string} and got {total}')
        elif match:
            num_dice = int(match.group(1))
            num_sides = int(match.group(2))
            total = 0
            for _ in range(num_dice):
                roll = random.randint(1, num_sides)
                total += roll
            await ctx.send(f'Rolled {dice_string} and got {total}')
        else:
            await ctx.send("Invalid input, please use format XdY or XdY+Z")
             
def setup(client):
    client.add_cog(diceroller(client))