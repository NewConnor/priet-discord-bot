import discord
import json
import random

with open('token.txt', 'r', encoding='utf-8') as file:
    TOKEN = file.read()
data = None

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

default = discord.Intents.all()
client = discord.Client(intents=default)

@client.event
async def on_ready():
    print(f"{client.user.name}로 로그인")

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="노동자")
    await member.add_roles(role)

@client.event
async def on_message(message):
    global data
    if message.author == client.user:
        return

    if message.content.startswith('프리엣'):

        text = message.content[4:].split()
        
        if text[0] == '도움말':
            await message.channel.send("아직 지원하지 않는 기능입니다.")
            
        elif text[0] == '새로고침':
            await message.channel.send("새로고침 중...")
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            await message.channel.send("완료.")

        elif text[0] == '배워':
            key = text[1]
            value = " ".join(text[2:])
            data[key] = value
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            await message.channel.send(f"`{key}`-->`{value}`")

        elif text[0] == '잊어':
            del data[text[1]]
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            await message.channel.send(f"`{text[1]}` 기억 삭제.")

        elif text[0] == '공장짓기' or text[0] == '공장생성' or text[0] == '공장만들기':
            have_permission = 0
            for role in message.author.roles:
                if role.name == "부르주아": have_permission = 1
            if have_permission:    
                fac_name = " ".join(text[1:])
            
                guild = message.guild
            
                role1 = await guild.create_role(name=f"{fac_name} 소속")
                role2 = discord.utils.get(guild.roles, name='노동자')

                overwrites = {
                    role1: discord.PermissionOverwrite(view_channel=True, manage_channels=False, manage_permissions=False, manage_webhooks=False, create_instant_invite=False, send_messages=True, embed_links=True, attach_files=True, add_reactions=True, external_emojis=True, mention_everyone=False, manage_messages=False, read_message_history=True, send_tts_messages=True, connect=True, speak=True, stream=True, use_voice_activation=True, priority_speaker=False, mute_members=False, deafen_members=False, move_members=False),
                    role2: discord.PermissionOverwrite(view_channel=False, manage_channels=False, manage_permissions=False, manage_webhooks=False, create_instant_invite=False, send_messages=False, embed_links=False, attach_files=False, add_reactions=False, external_emojis=False, mention_everyone=False, manage_messages=False, read_message_history=False, send_tts_messages=False, connect=False, speak=False, stream=False, use_voice_activation=False, priority_speaker=False, mute_members=False, deafen_members=False, move_members=False)
                }

                category = await guild.create_category(fac_name, overwrites=overwrites)
                await guild.create_text_channel(f"💬{fac_name}-대화💬", category=category)
                await guild.create_text_channel(f"{fac_name}-전화망", category=category)
                await message.channel.send(f'`{fac_name}` 공장을 지었습니다.')

        elif text[0] == '공장철거' or text[0] == '공장부수기' or text[0] == '공장없애기':
            have_permission = 0
            for role in message.author.roles:
                if role.name == "부르주아": have_permission = 1
            if have_permission:
                fac_name = " ".join(text[1:])
                guild = message.guild
                category = discord.utils.get(guild.categories, name=fac_name)
                role = discord.utils.get(guild.roles, name=f"{fac_name} 소속")
                if role: await role.delete()
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
                await message.channel.send(f'`{fac_name}` 공장을 철거했습니다.')
            
        else:
            await say(message.content[4:], message.channel)
            
async def say(text, channel):
    try:
        await channel.send(data[text])
    except:
        await channel.send(f"`{text}` ? 잘 모르겠습니다. '배워' 명령어를 사용해주세요.")

client.run(TOKEN)
