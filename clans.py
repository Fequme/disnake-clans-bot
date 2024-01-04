import requests
import time
import disnake
from pymongo import MongoClient
import pymongo
from disnake import File, ButtonStyle
from disnake.ui import Button, View
from disnake import components
from PIL import Image, ImageChops, ImageDraw, ImageFont
import io
import asyncio
from io import BytesIO
import time
import random
from datetime import datetime, timedelta
from datetime import date
from delorean import Delorean
import disnake
import config
from config import *
from disnake.ext import commands, tasks
import os
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())
bot.remove_command('help')
test_guild = 1112739235741573152
client = pymongo.MongoClient(
    "mongodb+srv://clans:clans@clans.fi8pc3i.mongodb.net/?retryWrites=true&w=majority")
coll = client.lan.balance
m = client.lan.balance
tr = client.lan.transiction
mar = client.lan.lhistory
loves = client.lan.loves
clans = client.lan.clans


async def fu(interaction):
    embed = disnake.Embed(
        description=f"{interaction.user.mention}, Вы **не можете** использовать данную **кнопку.**", color=0x2F3136)
    await interaction.send(embed=embed, ephemeral=True)


class ButtonPaginato:
    def __init__(
        self,
        segments,
        title="",
        color=0x000000,
        prefix="",
        suffix="",
        target_page=1,
        timeout=300,
        button_style=disnake.ButtonStyle.gray,
        invalid_user_function=fu,
    ):
        self.embeds = []
        self.current_page = target_page
        self.timeout = timeout
        self.button_style = button_style
        self.invalid_user_function = invalid_user_function

        for segment in segments:
            if isinstance(segment, disnake.Embed):
                self.embeds.append(segment)
            else:
                x = disnake.Embed(title=title, color=color,
                                  description=prefix + segment)

                x.set_thumbnail(url=suffix)
                self.embeds.append(x)

        if self.current_page > len(segments) or self.current_page < 1:
            self.current_page = 1

        class PaginatorView(disnake.ui.View):
            def __init__(this, interaction):
                super().__init__()

                this.timeout = self.timeout
                this.interaction = interaction

            async def on_timeout(this):
                for button in this.children:
                    button.disabled = True
                await this.interaction.edit_original_message(embed=self.embeds[self.current_page-1], view=this)
                return await super().on_timeout()

            def update_page(this):
                for button in this.children:
                    if button.label:
                        if button.label.strip() != "":
                            button.label = f"Страница {self.current_page}/{len(self.embeds)}"

            @disnake.ui.button(emoji="<:left:1048306852691202058>", style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def previous_button(this, _, button_interaction):
                if button_interaction.user != this.interaction.user:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page -= 1
                if self.current_page < 1:
                    self.current_page = int(1)
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)

            @disnake.ui.button(emoji="<:trash:1048306861478264863>", style=disnake.ButtonStyle.grey)
            async def previous_buttons(this, _, button_interaction):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return
                await this.interaction.delete_original_message()

            @disnake.ui.button(emoji="<:right:1048306859628564520>", style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def next_button(this, _, button_interaction):
                if button_interaction.user != this.interaction.user:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page += 1
                if self.current_page > len(self.embeds):
                    self.current_page = len(self.embeds)
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)

        self.view = PaginatorView

    async def start(self, interaction, ephemeral=False, deferred=False):
        if not deferred:
            await interaction.response.send_message(embed=self.embeds[self.current_page-1], view=self.view(interaction), ephemeral=ephemeral)
        else:
            await interaction.edit_original_message(embed=self.embeds[self.current_page-1], view=self.view(interaction))


async def return_mesto(member_id):
    finds = clans.find(limit=2000).sort("online", -1)
    finds = list(finds)
    try:
        if finds:
            find = clans.find_one({"owner_id": member_id})
            if find:
                index = finds.index(find)+1
                if index > 1000:
                    return index
                else:
                    return index
            else:
                return index
        else:
            return 'Ошибка'
    except:
        return '100'


def circle(pfp, size=(250, 250)):

    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[- 1])
    pfp.putalpha(mask)
    return pfp


async def get_mem(members, interaction):
    try:
        uid = str(members).split("@")[1].split(">")[0]
    except:
        uid = members
    member = interaction.guild.get_member(uid)
    return member


def circle(pfp, size=(250, 250)):

    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[- 1])
    pfp.putalpha(mask)
    return pfp


class clan_button_back(disnake.ui.View):
    def __init__(self, find, bot, member: disnake.Member):
        self.find = find
        self.bot = bot
        self.member = member
        super().__init__(timeout=None)

    @disnake.ui.button(label="Назад", style=ButtonStyle.gray)
    async def bu1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        role = interaction.guild.get_role(self.find['role'])
        emb = disnake.Embed(
            title=f'Управление Кланом — {self.find["room_name"]}',
            description=f'Дата создания: <t:{self.find["time_create"]}:F>\nСлоты: **{len(role.members)} / 30**\nСоздатель: <@{self.find["owner_id"]}>\nРоль: <@&{self.find["role"]}>', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.response.edit_message(embed=emb, view=clan_button(self.find, self.bot, self.member))


class clan_button2(disnake.ui.View):
    def __init__(self, find, bot, member: disnake.Member):
        self.find = find
        self.bot = bot
        self.member = member
        super().__init__(timeout=None)

    @disnake.ui.button(label="Пригласить в клан", style=ButtonStyle.gray, row=1)
    async def bu1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        role = interaction.guild.get_role(self.find['role'])
        if len(role.members) >= 30:
            embed = disnake.Embed(title="Пригласить в клан", description=f"{interaction.author.mention}, **превышен** лимит **участников**.",  color=0x2f3136).set_thumbnail(
                url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
        else:
            emb = disnake.Embed(
                title='Пригласить участника в клан',
                description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=emb, view=None)
            try:
                res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
                await res.delete()
                id_mem = res.content \
                    .replace("<", "") \
                    .replace("@", "") \
                    .replace("!", "") \
                    .replace(">", "")
                try:
                    member = await interaction.guild.fetch_member(int(id_mem))
                except:
                    emb = disnake.Embed(
                        title='Ошибка!',
                        description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    raise
                if member.bot:
                    embed = disnake.Embed(title="Пригласить участника в клан",
                                          description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(title="Пригласить участника в клан",
                                          description=f"{interaction.author.mention}, Вы **не можете** пригласить **сами у себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                channel = interaction.guild.get_channel(
                    int(self.find['channel']))
                if member:
                    role = interaction.guild.get_role(self.find['role'])
                    if role in member.roles:
                        emb = disnake.Embed(
                            title='Пригласить участника в клан',
                            description=f'{interaction.author.mention}, у {member.mention} **уже есть** роль клана <#{self.find["channel"]}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        post = {
                            "id": member.id,
                            "online": 0,
                            "pair": "Отсутствует",
                            "clan": "Отсутствует",
                            "balance": 0,
                            "rooms": [],
                            "clan_room_id": 0,
                            "message": 0,
                            "status": "Отсутствует"

                        }
                        if coll.count_documents({"id": member.id}) == 0:
                            coll.insert_one(post)
                        if int(m.find_one({"id": member.id})['clan_room_id']) != 0:
                            emb = disnake.Embed(
                                title='Пригласить участника в клан',
                                description=f'{interaction.author.mention}, у {member.mention} **уже есть** роль клана <#{self.find["channel"]}>', color=0x2f3136
                            )
                            emb.set_thumbnail(
                                url=interaction.author.display_avatar)
                            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        else:

                            emb = disnake.Embed(
                                title='Пригласить участника в клан',
                                description=f'{interaction.author.mention}, {member.mention} **был** успешно **приглашен** в клан <#{self.find["channel"]}>', color=0x2f3136
                            )
                            emb.set_thumbnail(
                                url=interaction.author.display_avatar)
                            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                            #print(self.find["channel"])
                            clanch = self.bot.get_channel(self.find["channel"])
                            #print(clanch.name)
                            coll.update_one({"id": member.id}, {"$set": {"clan": clanch.name, "clan_room_id": channel.id}})
                            await member.add_roles(role)
                            await channel.set_permissions(member, connect=True, view_channel=True)
                else:
                    emb = disnake.Embed(
                        title='Ошибка!',
                        description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            except asyncio.TimeoutError:
                emb = disnake.Embed(
                    title='Пригласить участника в клан',
                    description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Исключить из клана", style=ButtonStyle.gray, row=1)
    async def bu12(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return

        channel = interaction.guild.get_channel(int(self.find['channel']))
        emb = disnake.Embed(
            title='Исключить из клана',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, Вы **не можете** исключить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(self.find['role'])
                if role in member.roles:
                    emb = disnake.Embed(
                        title='Исключить из клана',
                        description=f'{interaction.author.mention}, {member.mention} **Был** успешно **исключен** из клана <#{channel.id}>', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    
                    embm = disnake.Embed(
                        title = "Уведомление",
                        description = f"{member.mention}, вы были исключены из клана **{role.name}** пользователем {interaction.author.mention}",
                        color = 0x2f3136
                    )

                    embm.set_thumbnail(url=member.display_avatar)
                    
                    await member.send(embed=emb)
                    
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    await channel.set_permissions(member, connect=False, view_channel=False)
                    coll.update_one({"id": member.id}, {
                                    "$set": {"clan_room_id": 0}})
                    for i in clans.find({"manage_id": member.id, "guild_id": interaction.guild.id, "prava": 1}):
                        clans.delete_one(i)
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
                else:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, **Не** состоит в **вашем** клане. ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Исключить из клана',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Добавить совладельца", style=ButtonStyle.gray, disabled=True, row=1)
    async def bu122(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        okss = []
        for i in clans.find({"channel": channel.id, "prava": 1}):
            okss.append(i)
        if len(okss) == 1:
            emb = disnake.Embed(
                title='Добавить совладельца',
                description=f'{interaction.author.mention}, **Вы** превысили **лимит** совладельцов.', color=0x2f3136
            )
            emb.set_thumbnail(
                url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            return
        emb = disnake.Embed(
            title='Добавить совладельца',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.response.edit_message(embed=emb, components=[])
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Добавить совладельца", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Добавить совладельца", description=f"{interaction.author.mention}, Вы **не можете** добавить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(self.find['role'])
                if role in member.roles:
                    finds = clans.find_one(
                        {"guild_id": member.guild.id, "prava": 1, "room_name": self.find['room_name']})
                    if finds:
                        emb = disnake.Embed(
                            title='Добавить совладельца',
                            description=f'{interaction.author.mention}, пользователь {member.mention} уже является **СоВладельцем** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        emb = disnake.Embed(
                            title='Добавить совладельца',
                            description=f'{interaction.author.mention}, вы **выдали** пользователю {member.mention} **СоВладельца** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        oks = []
                        for i in clans.find({"manage_id": member.id, "guild_id": interaction.guild.id}):
                            oks.append(i)
                        zx = len(oks)

                        post = {
                            "manage_id": member.id,
                            "prava": 1,
                            "channel": channel.id,
                            "role": role.id,
                            "guild_id": interaction.guild.id,
                            "counte": zx + 1,
                            "room_name": self.find['room_name']
                        }
                        clans.insert_one(post)
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Добавить совладельца',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Удалить совладельца", style=ButtonStyle.gray, disabled=True, row=2)
    async def bu1222(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        emb = disnake.Embed(
            title='Удалить совладельца',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            num1 = self.find
            self.l_room = clans
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Удалить совладельца", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Удалить совладельца", description=f"{interaction.author.mention}, Вы **не можете** удалить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(num1['role'])
                if role in member.roles:
                    finds = self.l_room.find_one(
                        {"manage_id": member.id, "guild_id": interaction.guild.id, "prava": 1})
                    if not finds:
                        emb = disnake.Embed(
                            title='Удалить совладельца',
                            description=f'{interaction.author.mention}, пользователь {member.mention} **не** является **СоВладельцем** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        emb = disnake.Embed(
                            title='Удалить совладельца',
                            description=f'{interaction.author.mention}, вы **удалили** с пользователя {member.mention} **СоВладельца** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        self.l_room.delete_one(finds)
                else:
                    emb = disnake.Embed(
                        title='Удалить совладельца',
                        description=f'{interaction.author.mention}, **Не** состоит в **клане.**', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Удалить совладельца',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Изменить название", style=ButtonStyle.gray, disabled=True, row=2)
    async def bu1222zx(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        num1 = self.find
        self.l_room = clans
        emb = disnake.Embed(
            title='Изменить нзвание клана',
            description=f'{interaction.author.mention}, **введите** новое название.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            name = res.content
            await channel.edit(name=f'{name}')
            self.l_room.update_one({"room_name": num1['room_name']}, {
                                   "$set": {"room_name": name}})
            emb5 = disnake.Embed(
                title='Изменить нзвание клана',
                description=f'{interaction.author.mention}, **Вы** успешно **изменили** название клана на: **{name}**.', color=0x2f3136
            )
            emb5.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb5, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Изменить нзвание клана',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Изменить цвет", style=ButtonStyle.gray, disabled=True, row=2)
    async def bu1222zxzxhj(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return

        channel = interaction.guild.get_channel(int(self.find['channel']))
        num1 = self.find
        self.l_room = clans
        emb = disnake.Embed(
            title='Изменить цвет',
            description=f'{interaction.author.mention}, **введите** новый цвет.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)

        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            col = res.content
            colors = col\
                .replace("#", "")
            role = interaction.guild.get_role(num1['role'])
            color = int(f"{colors}", 16)
            await role.edit(color=disnake.Color(color))
            emb = disnake.Embed(
                title='Изменить цвет',
                description=f'{interaction.author.mention}, **Вы** успешно **изменили** цвет **клана** на **{col}**.', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Смена Цвета Роли',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Закрыть", style=ButtonStyle.red, row=3)
    async def bu1222zxzx(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        await interaction.delete_original_message()


class clan_button(disnake.ui.View):
    def __init__(self, find, bot, member: disnake.Member):
        self.find = find
        self.bot = bot
        self.member = member
        super().__init__(timeout=None)

    @disnake.ui.button(label="Пригласить в клан", style=ButtonStyle.gray, row=1)
    async def bu1(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        role = interaction.guild.get_role(self.find['role'])
        if len(role.members) >= 30:
            embed = disnake.Embed(title="Пригласить в клан", description=f"{interaction.author.mention}, **превышен** лимит **участников**.",  color=0x2f3136).set_thumbnail(
                url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
        else:
            emb = disnake.Embed(
                title='Пригласить участника в клан',
                description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=emb, view=None)
            try:
                res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
                await res.delete()
                id_mem = res.content \
                    .replace("<", "") \
                    .replace("@", "") \
                    .replace("!", "") \
                    .replace(">", "")
                try:
                    member = await interaction.guild.fetch_member(int(id_mem))
                except:
                    emb = disnake.Embed(
                        title='Ошибка!',
                        description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    raise
                if member.bot:
                    embed = disnake.Embed(title="Пригласить участника в клан",
                                          description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(title="Пригласить участника в клан",
                                          description=f"{interaction.author.mention}, Вы **не можете** пригласить **сами у себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                channel = interaction.guild.get_channel(
                    int(self.find['channel']))
                if member:
                    role = interaction.guild.get_role(self.find['role'])
                    if role in member.roles:
                        emb = disnake.Embed(
                            title='Пригласить участника в клан',
                            description=f'{interaction.author.mention}, у {member.mention} **уже есть** роль клана <#{self.find["channel"]}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        post = {
                            "id": member.id,
                            "online": 0,
                            "pair": "Отсутствует",
                            "clan": "Отсутствует",
                            "balance": 0,
                            "rooms": [],
                            "clan_room_id": 0,
                            "message": 0,
                            "status": "Отсутствует"

                        }
                        if coll.count_documents({"id": member.id}) == 0:
                            coll.insert_one(post)
                        if int(m.find_one({"id": member.id})['clan_room_id']) != 0:
                            emb = disnake.Embed(
                                title='Пригласить участника в клан',
                                description=f'{interaction.author.mention}, у {member.mention} **уже есть** роль клана <#{self.find["channel"]}>', color=0x2f3136
                            )
                            emb.set_thumbnail(
                                url=interaction.author.display_avatar)
                            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        else:

                            emb = disnake.Embed(
                                title='Пригласить участника в клан',
                                description=f'{interaction.author.mention}, {member.mention} **был** успешно **приглашен** в клан <#{self.find["channel"]}>', color=0x2f3136
                            )
                            emb.set_thumbnail(
                                url=interaction.author.display_avatar)
                            msg = await interaction.edit_original_message(embed=emb)
                            #print(self.find["channel"])

                            bud = View(timeout=100)
                            accept = Button(label='Да')
                            cancel = Button(label='Нет')
                            bud.add_item(accept)
                            bud.add_item(cancel)

                            emb1 = disnake.Embed(
                                title=f'Приглашение в клан',
                                description=f'{interaction.user.mention}, вы уверены что хотите пригласить {member.mention} в клан?', color=0x2f3136)
                            emb1.set_thumbnail(
                                url=interaction.user.display_avatar)
                            emb1.set_footer(
                                text=f'Если у пользователя закрыто лс, Вы получите извещение об этом в лс.')
                            await msg.edit(embed=emb1, view=bud)  

                            async def accept_button_(push):
                                if push.author != interaction.author:
                                    pass
                                    return

                                emb1 = disnake.Embed(
                                    title = "Приглашение в клан",
                                    description = f"{interaction.user.mention}, ваше приглашение успешно было отправлено пользователю {member.mention}", 
                                    color=0x2f3136
                                )

                                emb1.set_thumbnail(url=interaction.user.display_avatar)
                                await msg.edit(embed=emb1, view=None)

                                # ======

                                buds = View(timeout=300)
                                accepts = Button(label='Да')
                                cancels = Button(label='Нет')
                                buds.add_item(accepts)
                                buds.add_item(cancels)
                                # =======
                                emb = disnake.Embed(
                                    title='Приглашение в клан',
                                    description=f'{member.mention}, пользователь {interaction.user.mention} отправил **вам** приглашение вступить в клан!', color=0x2f3136)
                                emb.set_thumbnail(url=member.avatar)
                                try:
                                    msg_mem = await member.send(embed=emb, view=buds)
                                except:
                                    await interaction.user.send(f'**Не удалось** отправить ваше предложение о вступление в клан пользователю {member.mention} в лс! Возможно у него оно закрыто!')
                                # =====

                                async def accepts_button_(push):
                                    if push.author != member:
                                        pass
                                        return

                                    clanch = self.bot.get_channel(self.find["channel"])
                                    #print(clanch.name)
                                    coll.update_one({"id": member.id}, {"$set": {"clan": clanch.name, "clan_room_id": channel.id}})
                                    await member.add_roles(role)
                                    await channel.set_permissions(member, connect=True, view_channel=True)

                                    emb = disnake.Embed(
                                        title='Приглашение в клан',
                                        description=f'{member.mention}, Вы успешно **вступили** в клан, в который вас пригласил(-а) {interaction.user.mention}!', color=0x2f3136)
                                    emb.set_thumbnail(url=member.avatar)

                                    emb1 = disnake.Embed(
                                        title='Приглашение в клан',
                                        description=f'{interaction.user.mention}, пользователь {member.mention} вступил в ваш клан', color=0x2f3136)
                                    emb1.set_thumbnail(url=member.avatar)
                                    await msg_mem.edit(embed=emb, view=None)
                                    await msg.edit(embed=emb1, view=None)
                                    # =====

                                accepts.callback = accepts_button_

                                async def cancels_button_(push):
                                    if push.author != member:
                                        pass
                                        return
                                    emb = disnake.Embed(
                                        title='Приглашение в клан',
                                        description=f'{member.mention}, Вы **отказались** от предложения {interaction.user.mention} вступить в клан!', color=0x2f3136)
                                    emb.set_thumbnail(url=member.avatar)
                                    await msg_mem.edit(embed=emb, view=None)
                                    # ====
                                    emb = disnake.Embed(
                                        title='Приглашение в клан',
                                        description=f'{interaction.user.mention}, пользователь {member.mention} **отказал** вам в приглашении в клан!', color=0x2f3136)
                                    emb.set_thumbnail(url=member.avatar)
                                    await interaction.user.send(embed=emb)
                                    await msg.edit(embed=emb, view=None)
                                cancels.callback = cancels_button_

                            async def cancel_button_(push):
                                if push.author != interaction.author:
                                    pass
                                    return
                                emb = disnake.Embed(
                                    title='Приглашение в клан',
                                    description=f'{interaction.user.mention}, **Вы** отменили приглашение пользователю {member.mention}!', color=0x2f3136)
                                emb.set_thumbnail(
                                    url=interaction.user.display_avatar)
                                await msg.edit(embed=emb, view=None)
                            cancel.callback = cancel_button_
                            accept.callback = accept_button_
                else:
                    emb = disnake.Embed(
                        title='Ошибка!',
                        description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            except asyncio.TimeoutError:
                emb = disnake.Embed(
                    title='Пригласить участника в клан',
                    description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Исключить из клана", style=ButtonStyle.gray, row=1)
    async def bu12(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return

        channel = interaction.guild.get_channel(int(self.find['channel']))
        emb = disnake.Embed(
            title='Исключить из клана',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, Вы **не можете** исключить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(self.find['role'])
                if role in member.roles:
                    emb = disnake.Embed(
                        title='Исключить из клана',
                        description=f'{interaction.author.mention}, {member.mention} **Был** успешно **исключен** из клана <#{channel.id}>', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    await channel.set_permissions(member, connect=False, view_channel=False)
                    coll.update_one({"id": member.id}, {
                                    "$set": {"clan": "Отсутствует", "clan_room_id": 0}})
                    for i in clans.find({"manage_id": member.id, "guild_id": interaction.guild.id, "prava": 1}):
                        clans.delete_one(i)
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
                else:
                    embed = disnake.Embed(
                        title="Исключить из клана", description=f"{interaction.author.mention}, **Не** состоит в **вашем** клане. ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Исключить из клана',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Добавить совладельца", style=ButtonStyle.gray, row=1)
    async def bu122(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        okss = []
        for i in clans.find({"channel": channel.id, "prava": 1}):
            okss.append(i)
        if len(okss) == 1:
            emb = disnake.Embed(
                title='Добавить совладельца',
                description=f'{interaction.author.mention}, **Вы** превысили **лимит** совладельцов.', color=0x2f3136
            )
            emb.set_thumbnail(
                url=interaction.author.display_avatar)
            await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            return
        emb = disnake.Embed(
            title='Добавить совладельца',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.response.edit_message(embed=emb, components=[])
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Добавить совладельца", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Добавить совладельца", description=f"{interaction.author.mention}, Вы **не можете** добавить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(self.find['role'])
                if role in member.roles:
                    finds = clans.find_one(
                        {"guild_id": member.guild.id, "prava": 1, "room_name": self.find['room_name']})
                    if finds:
                        emb = disnake.Embed(
                            title='Добавить совладельца',
                            description=f'{interaction.author.mention}, пользователь {member.mention} уже является **СоВладельцем** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        emb = disnake.Embed(
                            title='Добавить совладельца',
                            description=f'{interaction.author.mention}, вы **выдали** пользователю {member.mention} **СоВладельца** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        oks = []
                        for i in clans.find({"manage_id": member.id, "guild_id": interaction.guild.id}):
                            oks.append(i)
                        zx = len(oks)

                        post = {
                            "manage_id": member.id,
                            "prava": 1,
                            "channel": channel.id,
                            "role": role.id,
                            "guild_id": interaction.guild.id,
                            "counte": zx + 1,
                            "room_name": self.find['room_name']
                        }
                        clans.insert_one(post)
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Добавить совладельца',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            msg = await interaction.response.edit_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Удалить совладельца", style=ButtonStyle.gray, row=2)
    async def bu1222(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        emb = disnake.Embed(
            title='Удалить совладельца',
            description=f'{interaction.author.mention}, **упомяните** пользователя.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            num1 = self.find
            self.l_room = clans
            id_mem = res.content \
                .replace("<", "") \
                .replace("@", "") \
                .replace("!", "") \
                .replace(">", "")
            try:
                member = await interaction.guild.fetch_member(int(id_mem))
            except:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                raise
            if member:
                if member.bot:
                    embed = disnake.Embed(
                        title="Удалить совладельца", description=f"{interaction.author.mention}, Вы **не можете** провести **данную** операцию с **ботом...** ", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                if member == interaction.author:
                    embed = disnake.Embed(
                        title="Удалить совладельца", description=f"{interaction.author.mention}, Вы **не можете** удалить **сами себя**.", color=0x2f3136)
                    embed.set_thumbnail(url=interaction.author.display_avatar)
                    return await interaction.edit_original_message(embed=embed, view=clan_button_back(self.find, self.bot, self.member))
                role = interaction.guild.get_role(num1['role'])
                if role in member.roles:
                    finds = self.l_room.find_one(
                        {"manage_id": member.id, "guild_id": interaction.guild.id, "prava": 1})
                    if not finds:
                        emb = disnake.Embed(
                            title='Удалить совладельца',
                            description=f'{interaction.author.mention}, пользователь {member.mention} **не** является **СоВладельцем** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                    else:
                        emb = disnake.Embed(
                            title='Удалить совладельца',
                            description=f'{interaction.author.mention}, вы **удалили** с пользователя {member.mention} **СоВладельца** в клане <#{channel.id}>', color=0x2f3136
                        )
                        emb.set_thumbnail(
                            url=interaction.author.display_avatar)
                        await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
                        self.l_room.delete_one(finds)
                else:
                    emb = disnake.Embed(
                        title='Удалить совладельца',
                        description=f'{interaction.author.mention}, **Не** состоит в **клане.**', color=0x2f3136
                    )
                    emb.set_thumbnail(url=interaction.author.display_avatar)
                    await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
            else:
                emb = disnake.Embed(
                    title='Ошибка!',
                    description=f'{interaction.author.mention}, я **не могу** найти данного пользователя! Попробуйте ещё раз.', color=0x2f3136
                )
                emb.set_thumbnail(url=interaction.author.display_avatar)
                await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Удалить совладельца',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Изменить название", style=ButtonStyle.gray, row=2)
    async def bu1222zx(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        channel = interaction.guild.get_channel(int(self.find['channel']))
        num1 = self.find
        self.l_room = clans
        emb = disnake.Embed(
            title='Изменить нзвание клана',
            description=f'{interaction.author.mention}, **введите** новое название.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            name = res.content
            await channel.edit(name=f'{name}')
            self.l_room.update_one({"room_name": num1['room_name']}, {
                                   "$set": {"room_name": name}})
            emb5 = disnake.Embed(
                title='Изменить нзвание клана',
                description=f'{interaction.author.mention}, **Вы** успешно **изменили** название клана на: **{name}**.', color=0x2f3136
            )
            emb5.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb5, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Изменить нзвание клана',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Изменить цвет", style=ButtonStyle.gray, row=2)
    async def bu1222zxzxhj(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return

        channel = interaction.guild.get_channel(int(self.find['channel']))
        num1 = self.find
        self.l_room = clans
        emb = disnake.Embed(
            title='Изменить цвет',
            description=f'{interaction.author.mention}, **введите** новый цвет.', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)

        msg = await interaction.response.edit_message(embed=emb, view=None)
        try:
            res = await self.bot.wait_for("message", check=lambda i: i.author == interaction.author, timeout=60)
            await res.delete()
            col = res.content
            colors = col\
                .replace("#", "")
            role = interaction.guild.get_role(num1['role'])
            color = int(f"{colors}", 16)
            await role.edit(color=disnake.Color(color))
            emb = disnake.Embed(
                title='Изменить цвет',
                description=f'{interaction.author.mention}, **Вы** успешно **изменили** цвет **клана** на **{col}**.', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))
        except asyncio.TimeoutError:
            emb = disnake.Embed(
                title='Смена Цвета Роли',
                description=f'{interaction.author.mention}, время **вышло**!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await msg.edit(embed=emb, view=clan_button_back(self.find, self.bot, self.member))

    @disnake.ui.button(label="Закрыть", style=ButtonStyle.red, row=3)
    async def bu1222zxzx(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.member:
            pass
            return
        await interaction.delete_original_message()


class Dropdown(disnake.ui.Select):
    def __init__(self, interaction, finds, bot, member: disnake.Member):
        self.interaction = interaction
        self.finds = finds
        self.client = pymongo.MongoClient(
            "mongodb+srv://test:test@kolund.c04hlak.mongodb.net/?retryWrites=true&w=majority")
        self.l_room = self.client.lan.clans
        self.g_count = self.client.lan.guild_count
        self.bot = bot
        self.member = member
        optioons = []
        names = []
        for index, r in enumerate(self.finds):
            if r['prava'] == 2:
                own = 'Владелец'
            elif r['prava'] == 1:
                own = 'СоВладелец'
            names.append({"name": r['room_name']})
            optioons.append(disnake.SelectOption(
                label=r['room_name'], value=f"select_l_room_1", description=f"Вы: {own} данного клана"))
        super().__init__(
            options=optioons,
            placeholder="Выберите клан!",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        names = []
        for index, r in enumerate(self.finds):
            if r['prava'] == 2:
                own = 'Владелец'
            elif r['prava'] == 1:
                own = 'СоВладелец'
            names.append({"name": r['room_name']})
        if self.values[0] == 'select_l_room_1':
            abc = names[0]
        if self.values[0] == 'select_l_room_2':
            abc = names[1]
        elif self.values[0] == 'select_l_room_3':
            abc = names[2]
        elif self.values[0] == 'select_l_room_4':
            abc = names[3]
        elif self.values[0] == 'select_l_room_5':
            abc = names[4]
        elif self.values[0] == 'select_l_room_6':
            abc = names[5]
        elif self.values[0] == 'select_l_room_7':
            abc = names[6]
        elif self.values[0] == 'select_l_room_8':
            abc = names[7]
        elif self.values[0] == 'select_l_room_9':
            abc = names[8]
        elif self.values[0] == 'select_l_room_10':
            abc = names[9]
        if own == "СоВладелец":
            num1 = clans.find_one(
                {"room_name": abc['name'], "guild_id": interaction.guild.id, "manage_id": interaction.author.id})
            print(num1['channel'])
            channel = interaction.guild.get_channel(int(num1['channel']))
        else:
            num1 = clans.find_one(
                {"room_name": abc['name'], "guild_id": interaction.guild.id, "manage_id": interaction.author.id, "romes": 0})
            print(num1['channel'])
            channel = interaction.guild.get_channel(num1['channel'])

        role = interaction.guild.get_role(num1['role'])
        if own == "СоВладелец":
            emb = disnake.Embed(
                title=f'Управление Кланом — {num1["room_name"]}',
                description=f'Нажмите **любую** кнопку.', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            msg = await interaction.response.edit_message(embed=emb, view=clan_button2(num1, self.bot, self.member))
        else:
            emb2 = disnake.Embed(
                title=f'Управление Кланом — {num1["room_name"]}',
                description=f'Дата создания: <t:{num1["time_create"]}:F>\nСлоты: **{len(role.members)} / 30**\nСоздатель: <@{num1["owner_id"]}>\nРоль: <@&{num1["role"]}>', color=0x2f3136
            )
            emb2.set_thumbnail(url=interaction.author.display_avatar)
            msg = await interaction.response.edit_message(embed=emb2, view=clan_button(num1, self.bot, self.member))


class DropdownView(disnake.ui.View):
    def __init__(self, interaction, finds, bot, member: disnake.Member):
        super().__init__()
        self.interaction = interaction
        self.finds = finds
        self.bot = bot
        self.member = member
        self.add_item(Dropdown(self.interaction,
                      self.finds, self.bot, self.member))


@tasks.loop(seconds=60)
async def clanvoice():
    for guild in bot.guilds:
        if guild.id == 930455019038326885:
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.voice.channel.category.id == 930455019776516138:
                        clans.update_one({"channel": member.voice.channel.id}, {"$inc": {"online": 60}})

@bot.event
async def on_ready():
    print("connect")
    clanvoice.start()


@bot.slash_command(name="clan")
async def clan(interaction):
    pass


@clan.sub_command(name="create", description="Создать пользователю клан.")
@commands.has_permissions(administrator=True)
async def clan_cr(self, interaction, member: disnake.Member = commands.Param(name="пользователь", description="будущий овнер клана"), color: str = commands.Param(name="цвет", description="цвет роли и клана."), *, name=commands.Param(name="имя", description="имя клана")):
    await interaction.response.defer()
    okey = []
    for i in clans.find({"owner_id": member.id, "guild_id": interaction.guild.id}):
        okey.append(i)
    if len(okey) == 1:
        emb = disnake.Embed(
            title='Создать клан', description=f'{interaction.author.mention}, {member.mention} **уже** имеет **клан.**', color=0x2f3136)
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.edit_original_message(embed=emb)
        return

    color = color \
        .replace("#", "")
    try:
        color = int(f"{color}", 16)
    except:
        emb = disnake.Embed(
            title=f'Создание Клана',
            description=f'{interaction.user.mention}, **укажите** [HEX-COLOR](https://csscolor.ru/) в **цвет** роли.', color=0x2f3136)
        emb.set_thumbnail(url=interaction.user.avatar)
        await interaction.edit_original_message(embed=emb, view=None)
        raise
    category = disnake.utils.get(
        interaction.guild.categories, id=930803186640506910)
    channel2 = await interaction.guild.create_voice_channel(name=f'{name}', category=category, reason='Кланы')
    role = await interaction.guild.create_role(name=name, color=disnake.Color(color))
    emb = disnake.Embed(
        title='Создание Клана',
        description=f'{interaction.author.mention}, вы **создали** клан <#{channel2.id}> с ролью {role.mention} для пользователя {member.mention}', color=0x2f3136)
    emb.set_thumbnail(url=interaction.author.display_avatar)
    await interaction.edit_original_message(embed=emb)
    await member.add_roles(role)
    everyone = interaction.guild.get_role(interaction.guild.id)
    await channel2.set_permissions(role, connect=True, view_channel=True)
    await channel2.set_permissions(everyone, connect=False, view_channel=False)
    coll.update_one({"id": member.id}, {"$set": {"clan_room_id": channel2.id}})
    coll.update_one({"id": member.id}, {"$set": {"clan": name}})
    post = {
        "owner_id": member.id,
        "manage_id": member.id,
        "prava": 2,
        "channel": channel2.id,
        "role": role.id,
        "time_create": int(time.time()),
        "time_end": int(time.time()) + 2592000,
        "room_name": name,
        "counte": len(okey) + 1,
        "guild_id": interaction.guild.id,
        "online": 0,
        "romes": 0,
        "balance": 0
    }
    clans.insert_one(post)
    emb = disnake.Embed(
        title='Создать клан',
        description=f'{member.mention}, {interaction.author.mention} **создал** клан  {channel2.mention} с ролью **{role.mention}**', color=0x2f3136)
    emb.set_thumbnail(url=member.display_avatar)
    await member.send(embed=emb)


@clan.sub_command(
    name='manage',
    description=f'Управление кланом.',
    guild_ids=test_guild
)
async def room_manage(self, interaction):
    await interaction.response.defer()
    emb_load = disnake.Embed(
        title='Загрузка....',
        description=f'{interaction.author.mention}, происходит загрузка списка кланов! **Ожидайте**!', color=0x2f3136
    )
    emb_load.set_thumbnail(url=interaction.author.display_avatar)
    msg = await interaction.edit_original_message(embed=emb_load)
    finds = []
    for i in clans.find({"manage_id": interaction.author.id, "guild_id": interaction.guild.id}):
        finds.append(i)
    if not finds:
        emb = disnake.Embed(
            title='Ошибка',
            description=f'{interaction.author.mention}, у вас **нет** клана!',
            color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await msg.edit(embed=emb)
    else:
        emb2 = disnake.Embed(
            title='Управление кланом',
            description=f'{interaction.author.mention}, **выберите** клан, с которым хотите взаимодействовать, ниже!', color=0x2f3136
        )
        emb2.set_thumbnail(url=interaction.author.display_avatar)
        optioons = []
        names = []
        for index, r in enumerate(finds):
            if r['prava'] == 2:
                own = 'Владелец'
            elif r['prava'] == 1:
                own = 'СоВладелец'
            names.append({"name": r['room_name']})
            optioons.append(disnake.SelectOption(
                label=r['room_name'], value=f"select_l_room_{r['counte']}", description=f"Вы: {own} данного клана"))
        await msg.edit(embed=emb2, view=DropdownView(interaction, finds, bot, interaction.author))


@clan.sub_command(
    name='leave',
    description=f'Покинуть клан.',
    guild_ids=test_guild
)
async def room_managezxcv(self, interaction):
    await interaction.response.defer()
    room = int(m.find_one({"id": interaction.author.id})['clan_room_id'])
    if room == 0:
        emb2 = disnake.Embed(
            title='Покинуть клан',
            description=f'{interaction.author.mention}, **У** вас **отсутствует** клан.', color=0x2f3136
        )
        emb2.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.edit_original_message(embed=emb2)
        return

    clan_room = clans.find_one({"channel": room, "romes": 0})
    if clan_room['owner_id'] == interaction.author.id:
        emb2 = disnake.Embed(
            title='Покинуть клан',
            description=f'{interaction.author.mention}, **Вы** не можете **покинуть** свой же **клан**.', color=0x2f3136
        )
        emb2.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.edit_original_message(embed=emb2)
        return

    role = interaction.guild.get_role(clan_room['role'])
    channel = interaction.guild.get_channel(clan_room['channel'])
    emb = disnake.Embed(
        title='Покинуть клан',
        description=f'{interaction.author.mention}, **Вы** успешно **покинули** клан <#{channel.id}>', color=0x2f3136
    )
    emb.set_thumbnail(url=interaction.author.display_avatar)
    member = interaction.author
    await interaction.edit_original_message(embed=emb)
    await channel.set_permissions(member, connect=False, view_channel=False)
    finds = []
    for i in clans.find({"manage_id": interaction.author.id, "guild_id": interaction.guild.id, "prava": 1}):
        clans.delete_one(i)
    coll.update_one({"id": member.id}, {"$set": {"clan_room_id": 0}})
    try:
        await member.remove_roles(role)
    except:
        pass


@clan.sub_command(
    name='edit',
    description=f'Удалить/Продлить клан пользователю'
)
@commands.has_permissions(administrator=True)
async def redit(self, interaction, channel: disnake.VoiceChannel = commands.Param(name="канал", description="Укажите канал или его ID"), status: int = commands.Param(name="тип", description="Удалить или Продлить личную комнату пользователю", choices=[disnake.OptionChoice(name="Продлить", value=1), disnake.OptionChoice(name="Удалить", value=2)])):
    finds = clans.find_one({"channel": channel.id})
    if finds:
        if status == 1:
            emb = disnake.Embed(
                title='Продление клана',
                description=f'{interaction.author.mention}, вы **продлили** клан <#{channel.id}> на месяц!', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.send(embed=emb)
            clans.update_one({"channel": channel.id}, {
                             "$inc": {"time_end": 2592000}})
        elif status == 2:

            xm = clans.find_one({"channels": channel.id})

            role = interaction.guild.get_role(finds['role'])
            for member in role.members:
                coll.update_one({"id": member.id}, {
                                "$set": {"clan_room_id": 0}})
            emb = disnake.Embed(
                title='Удаление клана',
                description=f'{interaction.author.mention}, вы **удалили** клан <#{channel.id}> и её роль {role.mention}', color=0x2f3136
            )
            emb.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.send(embed=emb)
            await role.delete()
            await channel.delete()
            clans.delete_one(finds)
    else:
        emb = disnake.Embed(
            title='Ошибка',
            description=f'{interaction.author.mention}, данный клан **не является личной**!', color=0x2f3136
        )
        emb.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.send(embed=emb)


async def room_managezxcvzxzxzx(self, interaction):
    await interaction.response.defer()
    iters = 10
    # получаем список с рейтингом по убыванию. collestionuser коллекция с пользователями (на свое замените). в дискорде бесконечно нельзя выводить текст, так что давайте ограничим число мест в выводе
    rows = clans.find(limit=iters).sort("online", -1)
    count = 0
    text = ""
    em = {
        1: economy['number_one'],
        2: economy['number_two'],
        3: economy['number_free'],
        4: economy['number_four'],
        5: economy['number_five'],
        6: economy['number_six'],
        7: economy['number_seven'],
        8: economy['number_eight'],
        9: economy['number_nine'],
        10: economy['number_ten']
    }
    try:
        for place, x in enumerate(clans.find(limit=iters).sort("online", -1), start=1):
            nam = str(x["channel"])  # получаем имя
            if nam == None:  # если имя нельзя получить, т.е пользователь вышел с сервера, то пропускаем. Иначе вместо имени будет просто None
                continue
            try:
                lvl = x["online"]
            except:
                pass
            channel = interaction.author.guild.get_channel(int(nam))
            count += 1
            text += f"{em[place]} **・ {x['room_name']}**\n**{lvl // 3600}** ч. **{(lvl // 60) % 60}** мин. **{lvl % 60}** сек.\n"
            embed = disnake.Embed(
                title="ТОП-10 пользователей по онлайну в кланах.", description=f"{text}", color=0x2F3136)
            embed.set_thumbnail(url=bot.user.avatar)
        await interaction.edit_original_message(embed=embed)
    except:
        embed = disnake.Embed(
            title="ТОП-10 пользователей по онлайну в кланах.", description=f"Пусто...", color=0x2F3136)
        embed.set_thumbnail(url=bot.user.avatar)
        await interaction.edit_original_message(embed=embed)


@clan.sub_command(
    name='members',
    description=f'Список участников клана',
    guild_ids=test_guild
)
async def command_namez(self, interaction):
    room = int(m.find_one({"id": interaction.author.id})['clan_room_id'])
    if room == 0:
        emb2 = disnake.Embed(
            title='Профиль клана',
            description=f'{interaction.author.mention}, **У** вас **отсутствует** клан.', color=0x2f3136
        )
        emb2.set_thumbnail(url=interaction.author.display_avatar)
        await interaction.edit_original_message(embed=emb2)
        return
    clan_room = clans.find_one({"channel": room, "romes": 0})
    role = interaction.guild.get_role(clan_room['role'])
    pages = []
    page_content = ""
    number = 0
    for member in role.members:
        number += 1
        if (number > 0) and (number % 15 == 0):
            pages.append(page_content)
            page_content = ""
        if member.id == clan_room['owner_id']:
            page_content += f"<:point:1053335441765564457> {member.mention} - Создатель **клана**.\n"
        else:
            page_content += f"<:point:1053335441765564457> {member.mention} - Участник **клана**.\n"
    if (page_content != "") and not (page_content in pages):
        pages.append(page_content)
    paginator = ButtonPaginato(title=f"Всего {number} пользователей в клане {clan_room['room_name']}",
                               segments=pages, invalid_user_function=fu, suffix=interaction.author.avatar, color=0x2F3136)
    try:
        await paginator.start(interaction)
    except:
        embed = disnake.Embed(
            title=f"Всего {number} пользователей в клане {clan_room['room_name']}", description="Пусто.", color=0x2F3136)
        embed.set_thumbnail(url=interaction.author.avatar)
        await interaction.send(embed=embed, ephemeral=True)


@clan.sub_command(
    name='profile',
    description=f'Профиль клана.',
    guild_ids=test_guild
)
async def room_managezxcvzxzx(self, interaction, member: disnake.Member = None):
    post = {
        "id": interaction.author.id,
        "online": 0,
        "pair": "Отсутствует",
        "clan": "Отсутствует",
        "balance": 0,
        "rooms": [],
        "clan_room_id": 0,
        "message": 0,
        "status": "Отсутствует"

    }
    if coll.count_documents({"id": interaction.author.id}) == 0:
        coll.insert_one(post)
    if member is not None:
        await interaction.response.defer()
        interaction.author = member
        room = int(m.find_one({"id": interaction.author.id})['clan_room_id'])
        if room == 0:
            emb2 = disnake.Embed(
                title='Профиль клана',
                description=f'{interaction.author.mention}, **отсутствует** клан.', color=0x2f3136
            )
            emb2.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb2)
            return
        clan_room = clans.find_one({"channel": room, "romes": 0})

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'assets', 'clan_pr.png')
        base = Image.open(file_path).convert('RGBA')
        woner = interaction.guild.get_member(int(clan_room['owner_id']))
        url = str(woner.display_avatar.url)
        responese = requests.get(url, stream=True)
        responese = Image.open(io.BytesIO(responese.content))
        responese = responese.convert('RGBA')
        role = interaction.guild.get_role(clan_room['role'])
        pfp = responese
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype("ofont.ru_Arial.ttf", 24)
        font2 = ImageFont.truetype("ofont.ru_Arial.ttf", 33)
        font3 = ImageFont.truetype("ofont.ru_Arial.ttf", 18)
        nl = str(woner.name)
        find = clans.find_one({"channel": room, "prava": 1})
        if not find:
            pass
        else:
            member = interaction.guild.get_member(int(find['manage_id']))
            url1 = str(member.display_avatar.url)
            responese1 = requests.get(url1, stream=True)
            responese1 = Image.open(io.BytesIO(responese1.content))
            responese1 = responese1.convert('RGBA')
            pfp1 = responese1
            role = interaction.guild.get_role(clan_room['role'])
            nl2 = str(member.name)
            pfp1 = circle(pfp1, size=(42, 41))
            base.paste(pfp1, (103, 471), pfp1)
            name2 = f"{nl2[:20]}..." if len(nl2) > 20 else f"{nl2}"
            draw.text((160, 478), f"{name2}", font=font3)
        mesto = await return_mesto(int(clan_room['owner_id']))
        name = f"{nl[:20]}..." if len(nl) > 20 else f"{nl}"
        pfp = circle(pfp, size=(54, 53))
        draw.text(
            (515, 104), f"{clan_room['online'] // 3600} ч. {(clan_room['online'] // 60) % 60} мин.", font=font3)
        draw.text((118, 100), f"{str(clan_room['room_name'])}", font=font)
        draw.text((285, 230), f"{str(len(role.members))}", font=font2)
        draw.text((110, 401), f"{name}", font=font3)
        draw.text((778, 104), f"Место в топе: {mesto}", font=font3)
        base.paste(pfp, (43, 392), pfp)
        with BytesIO() as a:
            base.save('assets/bans.png')
            file_path = os.path.join(os.getcwd(), "assets/bans.png")
            file = disnake.File(file_path, filename="bans.png")
            await interaction.edit_original_message(file=file)
    else:
        await interaction.response.defer()
        room = int(m.find_one({"id": interaction.author.id})['clan_room_id'])
        if room == 0:
            emb2 = disnake.Embed(
                title='Профиль клана',
                description=f'{interaction.author.mention}, **У** вас **отсутствует** клан.', color=0x2f3136
            )
            emb2.set_thumbnail(url=interaction.author.display_avatar)
            await interaction.edit_original_message(embed=emb2)
            return
        clan_room = clans.find_one({"channel": room, "romes": 0})
        woner = interaction.guild.get_member(int(clan_room['owner_id']))
        base = Image.open("clan_pr.png").convert("RGBA")
        url = str(woner.display_avatar.url)
        responese = requests.get(url, stream=True)
        responese = Image.open(io.BytesIO(responese.content))
        responese = responese.convert('RGBA')
        role = interaction.guild.get_role(clan_room['role'])
        pfp = responese
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype("ofont.ru_Arial.ttf", 24)
        font2 = ImageFont.truetype("ofont.ru_Arial.ttf", 33)
        font3 = ImageFont.truetype("ofont.ru_Arial.ttf", 18)
        nl = str(woner.name)
        find = clans.find_one({"channel": room, "prava": 1})
        if not find:
            pass
        else:
            member = interaction.guild.get_member(int(find['manage_id']))
            url1 = str(member.display_avatar.url)
            responese1 = requests.get(url1, stream=True)
            responese1 = Image.open(io.BytesIO(responese1.content))
            responese1 = responese1.convert('RGBA')
            pfp1 = responese1
            role = interaction.guild.get_role(clan_room['role'])
            nl2 = str(member.name)
            pfp1 = circle(pfp1, size=(42, 41))
            base.paste(pfp1, (103, 471), pfp1)
            name2 = f"{nl2[:20]}..." if len(nl2) > 20 else f"{nl2}"
            draw.text((160, 478), f"{name2}", font=font3)
        mesto = await return_mesto(interaction.author.id)
        name = f"{nl[:20]}..." if len(nl) > 20 else f"{nl}"
        pfp = circle(pfp, size=(54, 53))
        draw.text(
            (515, 104), f"{clan_room['online'] // 3600} ч. {(clan_room['online'] // 60) % 60} мин.", font=font3)
        draw.text((118, 100), f"{str(clan_room['room_name'])}", font=font)
        draw.text((330, 230), f"{str(len(role.members))}", font=font2)
        draw.text((110, 401), f"{name}", font=font3)
        draw.text((778, 104), f"Место в топе: {mesto}", font=font3)
        base.paste(pfp, (47, 393), pfp)
        with BytesIO() as a:
            base.save('assets/bans.png')
            file_path = os.path.join(os.getcwd(), "assets/bans.png")
            file = disnake.File(file_path, filename="bans.png")
            await interaction.edit_original_message(file=file)


bot.run("")
