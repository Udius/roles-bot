# cd D:\Python\discord\раздатчик ролей
# python bot.py

import discord, os
from discord import utils   
from os import environ

import config

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for i in client.get_guild(664769832377384990).channels:
            if i.name == 'data' or i.name == 'DATA':
                channel = i
                self.DataChannel = channel

                async for message in channel.history():
                    if message.content.split()[0] == '**[ROLEDATA]**':
                        post_id = int(message.content.split()[1])
                        role_id = int(message.content.split()[2])

                        config.POST_ID.append(post_id)
                        config.ROLES[post_id] = role_id

                break

    async def on_raw_reaction_add(self, payload):
        if payload.message_id in config.POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

            try:
                role = utils.get(message.guild.roles, id=config.ROLES[payload.message_id]) # объект выбранной роли (если есть)
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
        if payload.message_id in config.POST_ID:
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

    async def on_message(self, message):
        if message.content[0:2] == '//':
            #category = message.category
            channel = message.channel
            member = message.author.name

            perm = False

            for role in message.author.roles:
                if role.id in config.HIGHTROLES:
                    perm = True

            if perm:
                if message.content.split()[0] == '//write' or message.content.split()[0] == '//wr' or message.content.split()[0] == '!!!':

                    text = message.content.split(' ')[1:].copy()
                    text = ' '.join(text)

                    await channel.send(text)
                    await message.delete()

                    print('[SUCCESS] Message by {0}: {1}'.format(member, text))

                elif message.content.split()[0] == '//pin' or message.content.split()[0] == '//p':
                    if len(message.content.split()) == 3:

                        post_id = int(message.content.split()[1])
                        role_id = int(message.content.split()[2])

                        await message.delete()

                        config.POST_ID.append(post_id)
                        config.ROLES[post_id] = role_id

                        await self.DataChannel.send('**[ROLEDATA]** ' + ' '.join(message.content.split()[1:]))

                        print('[SUCCESS] Pinrole by {0}'.format(member))

                    else:
                        await channel.send('**[ERROR]** Wrong format!')
                        print('[ERROR] Wrong format by ' + member)

                elif message.content.split()[0] == '//cleanrole' or message.content.split()[0] == '//clrole':

                    config.POST_ID = []
                    config.ROLES = {}

                    async for mes in self.DataChannel.history():
                        if mes.content.split()[0] == '[ROLEDATA]':
                            await mes.delete()

                    await channel.send('**[SUCCESS]** All roles has been dellited from posts')

                    print('[SUCCESS] All roles has been deleted from posts by', member)

                elif message.content == '//clear room' or message.content == '//cl room':

                    async for mes in channel.history():
                        await mes.delete()

                    print('[SUCCESS] Channel has been cleaned')

                elif message.content.split()[0] == '//get':
                    if message.content.split()[1] == 'botlist':
                        bots = list()

                        for mem in client.get_all_members():
                            if mem.bot:
                                bots.append('@' + str(mem) + ' - ' + str(mem.id))

                        await channel.send('**[SUCCESS]** Bot list:\n' + '\n '.join(bots))
                        await message.delete()

                        print('[SUCCESS] Get botlist has ben donned by', member)

            else:
                print('[ERROR] Low permissions by ' + member)


# RUN
client = MyClient()
TOKEN = environ.get('BOT_TOKEN')
client.run(TOKEN)

# python bot.py
# cd D:\Python\discord\раздатчик ролей
