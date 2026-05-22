# =========================================================
# HMC OBF BOT ULTIMATE FULL
# PYTHON 3 - ANDROID / PYDROID3
# =========================================================

# CÀI:
# pip install -U discord.py requests

# =========================================================
# IMPORT
# =========================================================

try:

    import discord
    from discord.ext import commands
    from discord import app_commands

except:

    print("CHƯA CÀI DISCORD.PY")
    print("CHẠY:")
    print("pip install -U discord.py")
    exit()

try:

    import requests

except:

    print("CHƯA CÀI REQUESTS")
    print("CHẠY:")
    print("pip install requests")
    exit()

import random
import string
import os
import base64
import json
import traceback
import zlib
import marshal

# =========================================================
# TOKEN BOT
# =========================================================

TOKEN = "MTUwNzAwNDMyNTk5NjUzMTcxMg.GxZUpC.BaORm3SbDXq2cjftaVUM__Q2iEjI8S8stXJP3s"

# =========================================================
# CONFIG
# =========================================================

PREFIX = "*"

OWNER_USERNAME = "hmc0086"

KEY_FILE = "keys.json"

USER_FILE = "users.json"

# =========================================================
# LOAD JSON
# =========================================================

def load_json(path):

    if not os.path.exists(path):

        with open(path, "w") as f:

            json.dump({}, f)

    try:

        with open(path, "r") as f:

            return json.load(f)

    except:

        return {}

# =========================================================
# SAVE JSON
# =========================================================

def save_json(path, data):

    with open(path, "w") as f:

        json.dump(data, f, indent=4)

# =========================================================
# DATABASE
# =========================================================

VIP_KEYS = load_json(KEY_FILE)

VIP_USERS = load_json(USER_FILE)

# =========================================================
# BOT
# =========================================================

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(

    command_prefix=PREFIX,
    intents=intents,
    help_command=None

)

# =========================================================
# RANDOM STRING
# =========================================================

def random_string(length=20):

    chars = string.ascii_letters + string.digits

    return ''.join(

        random.choice(chars)

        for _ in range(length)

    )

# =========================================================
# CHECK OWNER
# =========================================================

def is_owner(user):

    return user.name.lower() == OWNER_USERNAME.lower()

# =========================================================
# CHECK VIP
# =========================================================

def is_vip(user_id):

    return str(user_id) in VIP_USERS

# =========================================================
# GET FILE EXT
# =========================================================

def get_ext(url):

    if ".lua" in url:

        return ".lua"

    if ".py" in url:

        return ".py"

    return ".txt"

# =========================================================
# DOWNLOAD FILE
# =========================================================

def download_file(url):

    try:

        headers = {

            "User-Agent": "Mozilla/5.0"

        }

        r = requests.get(

            url,
            headers=headers,
            timeout=20

        )

        if r.status_code == 200:

            return r.text

    except:

        return None

    return None

# =========================================================
# SAFE OBF
# =========================================================

def obf_code(code, level):

    shift = level + 3

    encoded = []

    for c in code:

        encoded.append(

            str(ord(c) + shift)

        )

    payload = ",".join(encoded)

    return f'''

# HMC SAFE OBF LEVEL {level}

data = [{payload}]

source = ""

for i in data:

    source += chr(i - {shift})

exec(source)

'''

# =========================================================
# STRING ENCRYPTION
# =========================================================

def se_code(code, level):

    encoded = base64.b64encode(

        code.encode("utf8")

    ).decode()

    junk = ""

    if level >= 9:

        for _ in range(100):

            junk += (

                random_string(10)
                + "="
                + str(random.randint(1000,9999))
                + "\\n"

            )

    return f'''

# HMC STRING ENCRYPTION LEVEL {level}

{junk}

import base64

exec(

    base64.b64decode(

        "{encoded}"

    ).decode("utf8")

)

'''

# =========================================================
# HX ENCRYPTION
# =========================================================

def hx_encrypt(code, level):

    # LEVEL 1
    if level == 1:

        enc = base64.b64encode(
            code.encode()
        ).decode()

        return f'''

import base64

exec(
    base64.b64decode(
        "{enc}"
    ).decode()
)

'''

    # LEVEL 2
    elif level == 2:

        comp = zlib.compress(
            code.encode()
        )

        enc = base64.b64encode(comp).decode()

        return f'''

import zlib
import base64

exec(
    zlib.decompress(
        base64.b64decode(
            "{enc}"
        )
    ).decode()
)

'''

    # LEVEL 3-4
    elif level <= 4:

        compiled = compile(
            code,
            "<HMC>",
            "exec"
        )

        marsh = marshal.dumps(compiled)

        comp = zlib.compress(marsh)

        enc = base64.b64encode(comp).decode()

        junk = ""

        for _ in range(80):

            junk += (
                random_string(12)
                + "="
                + str(random.randint(1000,9999))
                + "\\n"
            )

        return f'''

# HX LEVEL {level}

{junk}

import marshal
import zlib
import base64

exec(
    marshal.loads(
        zlib.decompress(
            base64.b64decode(
                "{enc}"
            )
        )
    )
)

'''

    # LEVEL 5-7
    else:

        key = level + 15

        xor_data = []

        for c in code:

            xor_data.append(
                str(ord(c) ^ key)
            )

        payload = ",".join(xor_data)

        junk = ""

        for _ in range(250):

            junk += (
                random_string(15)
                + "="
                + str(random.randint(1000,9999))
                + "\\n"
            )

        return f'''

# HX ULTRA LEVEL {level}

{junk}

data = [{payload}]

source = ""

for i in data:

    source += chr(i ^ {key})

compiled = compile(
    source,
    "<HX>",
    "exec"
)

exec(compiled)

'''

# =========================================================
# READY
# =========================================================

@bot.event
async def on_ready():

    print("====================")

    print("BOT ONLINE")

    print(bot.user)

    print("====================")

    try:

        synced = await bot.tree.sync()

        print(f"SYNC {len(synced)} SLASH COMMAND")

    except Exception as e:

        print(e)

# =========================================================
# GETKEY
# =========================================================

@bot.tree.command(

    name="getkey",
    description="Lấy key VIP"

)
async def getkey(interaction: discord.Interaction):

    try:

        if not is_owner(interaction.user):

            return await interaction.response.send_message(

                "CHỈ @hmc0086 DÙNG ĐƯỢC",

                ephemeral=True

            )

        key = "vip-" + random_string(20)

        key = str(key).strip().lower()

        VIP_KEYS[key] = {

            "used": False

        }

        save_json(KEY_FILE, VIP_KEYS)

        await interaction.user.send(

            f"""

KEY VIP CỦA BẠN:

`{key}`

DÙNG:

`*redeem-key {key}`

"""

        )

        await interaction.response.send_message(

            "ĐÃ GỬI KEY VIP QUA TIN NHẮN RIÊNG",

            ephemeral=True

        )

    except:

        print(traceback.format_exc())

# =========================================================
# VIP LIST
# =========================================================

@bot.tree.command(

    name="viplist",
    description="Danh sách VIP"

)
async def viplist(interaction: discord.Interaction):

    try:

        if not is_owner(interaction.user):

            return await interaction.response.send_message(

                "KHÔNG CÓ QUYỀN",

                ephemeral=True

            )

        if len(VIP_USERS) == 0:

            return await interaction.response.send_message(

                "CHƯA CÓ USER VIP",

                ephemeral=True

            )

        text = "DANH SÁCH VIP\\n\\n"

        for uid, data in VIP_USERS.items():

            text += (

                f"{data['username']}\\n"

            )

        await interaction.response.send_message(

            text,

            ephemeral=True

        )

    except:

        print(traceback.format_exc())

# =========================================================
# HELP
# =========================================================

@bot.tree.command(

    name="help",
    description="Hướng dẫn sử dụng bot"

)
async def help_slash(interaction: discord.Interaction):

    try:

        text = """

========================

HMC OBF BOT

========================

SLASH COMMAND

/getkey
/viplist
/help

========================

LỆNH THƯỜNG

*redeem-key vip-xxxx

*obf level url

*SE level url

*HX level url

========================

OBF

1-28 = FREE
29-30 = VIP

========================

SE

1-8 = FREE
9-10 = VIP

========================

HX

1-2 = FREE
3-7 = VIP

========================

"""

        await interaction.response.send_message(

            text,

            ephemeral=True

        )

    except:

        print(traceback.format_exc())

# =========================================================
# REDEEM KEY
# =========================================================

@bot.command(name="redeem-key")
async def redeem_key(ctx, *, key=None):

    try:

        if key is None:

            return await ctx.reply(

                "DÙNG:\\n`*redeem-key vip-xxxx`"

            )

        user_id = str(ctx.author.id)

        key = str(key).strip().lower()

        # ĐÃ NHẬP
        if user_id in VIP_USERS:

            return await ctx.reply(

                "BẠN ĐÃ NHẬP KEY TRƯỚC ĐÓ"

            )

        # KEY KHÔNG TỒN TẠI
        if key not in VIP_KEYS:

            return await ctx.reply(

                "KEY KHÔNG ĐÚNG"

            )

        # KEY ĐÃ DÙNG
        if VIP_KEYS[key]["used"]:

            return await ctx.reply(

                "KEY NÀY ĐÃ ĐƯỢC SỬ DỤNG"

            )

        # SAVE USER
        VIP_USERS[user_id] = {

            "username": str(ctx.author),
            "key": key

        }

        # SAVE KEY
        VIP_KEYS[key]["used"] = True

        # SAVE FILE
        save_json(KEY_FILE, VIP_KEYS)

        save_json(USER_FILE, VIP_USERS)

        await ctx.reply(

            "KÍCH HOẠT VIP THÀNH CÔNG"

        )

    except:

        print(traceback.format_exc())

# =========================================================
# OBF
# =========================================================

@bot.command()
async def obf(ctx, level:int=None, url:str=None):

    try:

        if level is None or url is None:

            return await ctx.reply(
                "DÙNG:\\n*obf level url"
            )

        if level < 1 or level > 30:

            return await ctx.reply(
                "LEVEL CHỈ 1-30"
            )

        if level >= 29:

            if not is_vip(ctx.author.id):

                return await ctx.reply(
                    "CẦN VIP"
                )

        wait = await ctx.reply(
            "ĐANG OBF..."
        )

        code = download_file(url)

        if not code:

            return await wait.edit(
                content="LỖI TẢI FILE"
            )

        output = obf_code(code, level)

        ext = get_ext(url)

        filename = f"obf_{level}{ext}"

        with open(
            filename,
            "w",
            encoding="utf8"
        ) as f:

            f.write(output)

        await ctx.send(
            file=discord.File(filename)
        )

        os.remove(filename)

        await wait.delete()

    except:

        print(traceback.format_exc())

# =========================================================
# SE
# =========================================================

@bot.command(name="SE")
async def se(ctx, level:int=None, url:str=None):

    try:

        if level is None or url is None:

            return await ctx.reply(
                "DÙNG:\\n*SE level url"
            )

        if level < 1 or level > 10:

            return await ctx.reply(
                "LEVEL CHỈ 1-10"
            )

        if level >= 9:

            if not is_vip(ctx.author.id):

                return await ctx.reply(
                    "CẦN VIP"
                )

        wait = await ctx.reply(
            "ĐANG MÃ HÓA..."
        )

        code = download_file(url)

        if not code:

            return await wait.edit(
                content="LỖI TẢI FILE"
            )

        output = se_code(code, level)

        ext = get_ext(url)

        filename = f"SE_{level}{ext}"

        with open(
            filename,
            "w",
            encoding="utf8"
        ) as f:

            f.write(output)

        await ctx.send(
            file=discord.File(filename)
        )

        os.remove(filename)

        await wait.delete()

    except:

        print(traceback.format_exc())

# =========================================================
# HX
# =========================================================

@bot.command(name="HX")
async def hx(ctx, level:int=None, url:str=None):

    try:

        if level is None or url is None:

            return await ctx.reply(
                "DÙNG:\\n*HX level url"
            )

        if level < 1 or level > 7:

            return await ctx.reply(
                "LEVEL HX CHỈ 1-7"
            )

        if level >= 3:

            if not is_vip(ctx.author.id):

                return await ctx.reply(
                    "HX VIP CẦN VIP"
                )

        wait = await ctx.reply(
            "ĐANG HX ENCRYPTION..."
        )

        code = download_file(url)

        if not code:

            return await wait.edit(
                content="LỖI TẢI FILE"
            )

        output = hx_encrypt(code, level)

        ext = get_ext(url)

        filename = f"HX_{level}{ext}"

        with open(
            filename,
            "w",
            encoding="utf8"
        ) as f:

            f.write(output)

        await ctx.send(
            file=discord.File(filename)
        )

        os.remove(filename)

        await wait.delete()

    except:

        print(traceback.format_exc())

# =========================================================
# ERROR HANDLER
# =========================================================

@bot.event
async def on_command_error(ctx, error):

    try:

        if isinstance(
            error,
            commands.CommandNotFound
        ):
            return

        print(traceback.format_exc())

        await ctx.reply(
            f"LỖI:\\n```{error}```"
        )

    except:
        pass

# =========================================================
# START BOT
# =========================================================

try:

    bot.run(TOKEN)

except Exception as e:

    print("BOT LỖI:")
    print(e)