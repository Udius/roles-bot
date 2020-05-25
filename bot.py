# cd D:\Python\discord
# python bot.py
    
import discord, os
from discord import utils

import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id in config.POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

            try:
                role = utils.get(message.guild.roles, id=config.ROLES[payload.message_id]) # объект выбранной роли (если есть)
                print(role)
                if (len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
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
            role = utils.get(message.guild.roles, id=config.ROLES[payload.message_id]) # объект выбранной роли (если есть)

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + str(payload.message_id))
        except Exception as e:
            print(repr(e))

    #async def on_guild_join(self, guild): # событие подключения к серверу
    #    category = guild.categories[0] # выбирает первую категорию из сервера, к которому подключился
    #    channel = category.channels[0] # получает первый канал в первой категории
    #    await channel.send("Something") # отправка самого сообщения

    async def on_message(self, message):
        #category = message.category
        channel = message.channel

        if message.content.split()[0] == 'writehere' or message.content.split()[0] == 'wrhere':
            text = message.content.split(' ')[1:].copy()
            text = ' '.join(text)
            member = message.author.name

            await channel.send(text)
            await message.delete()
            print('[SUCCESS] Message by {0}: {1}'.format(member, text))

        elif message.content.split()[0] == 'pinrole' or message.content.split()[0] == 'prole':
            perm = False
            member = message.author.name

            for role in message.author.roles:
                if role.id in config.HIGHTROLES:
                    perm = True

            if perm:
                post_id = int(message.content.split()[1])
                role_id = int(message.content.split()[2])
                
                await message.delete()
                
                config.POST_ID.append(post_id)
                config.ROLES[post_id] = role_id
                
                print('[SUCCESS] Pinrole by {0}'.format(member))

            else:
                print('[ERROR] Low permissions to pinrole: {0}'.format(member))

# RUN
client = MyClient()
TOKEN = os.environ.get('BOT_TOKEN')
client.run(TOKEN)

# python bot.py
# cd D:\Python\discord
