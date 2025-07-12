import typing
import time
import discord
import os
import asyncio
import constants
import inspect

def ansi_style(text, *styles):
    ansi_codes = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "reset": 0,
        "bold": 1,
        "dim": 2,
        "italic": 3,
        "underline": 4,
        "blink": 5,
        "reverse": 7,
        "hidden": 8,
        "strikethrough": 9,
    }

    codes = []
    for name in styles:
        code = ansi_codes.get(name.lower())
        if code is not None:
            codes.append(str(code))
    if not codes:
        codes = ["0"]
    return f"\033[{';'.join(codes)}m{text}\033[0m"


def write_log(message: str, level: typing.Literal["INFO", "WARN", "ERROR"]):
    file_name = os.path.basename(inspect.stack()[1].filename)

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if level == "INFO":
        result = ansi_style("INFO", "green", "bold") + ansi_style(": "+message, "green")
        log_txt = current_time + f" ({file_name}:{inspect.currentframe().f_back.f_lineno})" " INFO: " + message
    elif level == "WARN":
        result = ansi_style("WARN", "yellow", "bold") + ansi_style(": "+message, "yellow")
        log_txt = current_time + f" ({file_name}:{inspect.currentframe().f_back.f_lineno})" " WARN: " + message
    elif level == "ERROR":
        result = ansi_style("ERROR", "red", "bold") + ansi_style(": "+message, "red")
        log_txt = current_time + f" ({file_name}:{inspect.currentframe().f_back.f_lineno})" " ERROR: " + message

    result = current_time + f" ({file_name}:{inspect.currentframe().f_back.f_lineno})" + " " + result
    print(result)
    with open(constants.LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_txt + "\n")

def seperate_log():
    with open(constants.LOG_FILE_PATH, "a") as f:
        f.write("-"*constants.LOG_SEPARATOR_LENGTH+"\n")

def is_url(query: str) -> bool:
    return query.startswith("http://") or query.startswith("https://")

def has_djrole(member: discord.Member, roles: list[int]):
    member_role_ids = {role.id for role in member.roles}
    return any(role_id in member_role_ids for role_id in roles)

async def monitor_idle(vc: discord.VoiceClient, timeout_minutes: int):
    if timeout_minutes < 0:
        return  # No timeout

    interval = 10  # Check every 10 seconds
    empty_seconds = 0
    threshold = timeout_minutes * 60

    while vc.is_connected():
        non_bots = [m for m in vc.channel.members if not m.bot]

        if not non_bots:
            empty_seconds += interval
            if empty_seconds >= threshold:
                await vc.disconnect(force=True)
                write_log(f"Disconnected from {vc.guild.name} due to idle timeout", "INFO")
                await vc.channel.send("⛔ Bot has been disconnected due to inactivity.")
                break
        else:
            empty_seconds = 0  # Reset the timer if a user joins

        await asyncio.sleep(interval)
