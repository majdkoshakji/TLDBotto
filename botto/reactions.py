import asyncio
import logging
import random

from discord import Message

import tld_botto
from food import SpecialAction

log = logging.getLogger("MottoBotto").getChild("reactions")
log.setLevel(logging.DEBUG)


async def skynet_prevention(botto: tld_botto, message: Message):
    log.info(f"{message.author} attempted to activate Skynet!")
    await message.add_reaction(botto.config["reactions"]["reject"])
    await message.add_reaction(botto.config["reactions"]["skynet"])
    if botto.config["should_reply"]:
        await message.reply("Skynet prevention")


async def snail(botto: tld_botto, message: Message):
    log.info(f"Snail from: {message.author}")
    await message.add_reaction("🐌")


async def poke(botto: tld_botto, message: Message):
    log.info(f"Poke from: {message.author}")
    await message.add_reaction(random.choice(botto.config["reactions"]["poke"]))


async def love(botto: tld_botto, message: Message):
    log.info(f"Apology/love from: {message.author}")
    await message.add_reaction(random.choice(botto.config["reactions"]["love"]))


async def hug(botto: tld_botto, message: Message):
    log.info(f"Hug from: {message.author}")
    await message.add_reaction(random.choice(botto.config["reactions"]["hug"]))


async def party(botto: tld_botto, message: Message):
    log.info(f"Party from: {message.author}")
    tasks = []
    for _ in range(5):
        tasks.append(
            message.add_reaction(random.choice(botto.config["reactions"]["party"]))
        )
    await asyncio.wait(tasks)


async def food(botto: tld_botto, message: Message, food_item: str):
    reactions = botto.regexes.food.lookup[food_item]
    for reaction in reactions:
        if reaction == SpecialAction.echo:
            await message.add_reaction(food_item)
        elif reaction == SpecialAction.party:
            await party(botto, message)
        else:
            await message.add_reaction(reaction)


async def unrecognised_food(botto: tld_botto, message: Message):
    await message.add_reaction("😵")


async def not_reply(botto: tld_botto, message: Message):
    log.info(
        f"Suggestion from {message.author} was not a reply (Message ID {message.id})"
    )
    await message.add_reaction(botto.config["reactions"]["unknown"])
    if botto.config["should_reply"]:
        await message.reply("I see no motto!")


async def fishing(botto: tld_botto, message: Message):
    log.info(f"Motto fishing from: {message.author}")
    await message.add_reaction(botto.config["reactions"]["reject"])
    await message.add_reaction(botto.config["reactions"]["fishing"])


async def invalid(botto: tld_botto, message: Message):
    log.info(f"Motto from {message.author} is invalid according to rules.")
    await message.add_reaction(botto.config["reactions"]["reject"])
    await message.add_reaction(botto.config["reactions"]["invalid"])


async def duplicate(botto: tld_botto, message: Message):
    log.debug("Ignoring motto, it's a duplicate.")
    await message.add_reaction(botto.config["reactions"]["repeat"])
    await message.remove_reaction(botto.config["reactions"]["pending"], botto.user)


async def deleted(botto: tld_botto, message: Message):
    log.debug("Ignoring motto, it's been deleted.")
    await message.add_reaction(botto.config["reactions"]["deleted"])
    await message.add_reaction(botto.config["reactions"]["reject"])
    await message.remove_reaction(botto.config["reactions"]["pending"], botto.user)


async def stored(botto: tld_botto, message: Message, motto_message: Message):
    await message.remove_reaction(botto.config["reactions"]["pending"], botto.user)
    await message.add_reaction(botto.config["reactions"]["success"])
    if special_reactions := botto.config["special_reactions"].get(
            str(motto_message.author.id)
    ):
        await message.add_reaction(random.choice(special_reactions))
    log.debug("Reaction added")
    if botto.config["should_reply"]:
        await message.reply(f'"{motto_message.content}" will be considered!')
    log.debug("Reply sent")


async def pending(botto: tld_botto, message: Message, motto_message: Message):
    await message.add_reaction(botto.config["reactions"]["pending"])
    log.debug("Reaction added")


async def invalid_emoji(botto: tld_botto, message: Message):
    log.info(f"Invalid emoji requested from {message.author}")
    await message.add_reaction(botto.config["reactions"]["invalid_emoji"])


async def valid_emoji(botto: tld_botto, message: Message):
    log.info(f"Valid emoji requested from {message.author}")
    await message.add_reaction(botto.config["reactions"]["valid_emoji"])


async def rule_1(botto: tld_botto, message: Message):
    for emoji in botto.config["reactions"]["rule_1"]:
        await message.add_reaction(emoji)
    log.info(f"Someone broke rule #1")


async def favorite_band(botto: tld_botto, message: Message):
    for letter in botto.config["reactions"]["favorite_band"]:
        await message.add_reaction(letter)
    log.info(f"Someone asked for favorite band")


async def off_topic(botto: tld_botto, message: Message):
    await message.add_reaction(random.choice(botto.config["reactions"]["off_topic"]))


async def unknown_dm(botto: tld_botto, message: Message):
    log.info(f"I don't know how to handle {message.content} from {message.author}")
    await message.add_reaction(botto.config["reactions"]["unknown"])
