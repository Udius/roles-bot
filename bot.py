# cd D:\Python\discord
# python bot.py

import discord, os
from discord import utils

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)

                if(len([i for i in member.roles if i.id not in EXCROLES]) <= .MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=ROLES[emoji]) # объект выбранной роли (если есть)

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

# RUN
POST_ID = 713786296094425149

ROLES = {
	'🍉': 713447505106436198, # Cr Ops
	'🎵': 713447556922736711, # PUBG
	'🎮': 713447748623663124 # Standoff 2
}

EXCROLES = {}

MAX_ROLES_PER_USER = 3333

client = MyClient()
TOKEN = os.environ.get('BOT_TOKEN')
client.run(TOKEN)
