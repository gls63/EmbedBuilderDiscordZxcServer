import discord
import os
from discord.ext import commands
from discord import Embed, Option


# .env файл
# DISCORD_TOKEN=ваш_токен_бота
# GUILD_ID=ваш_ID_гильдии (опционально, для регистрации команд только на вашем сервере)

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all()) # Все интенты


@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов!')

    try:
       synced = await bot.tree.sync(guild=discord.Object(id=os.environ.get("GUILD_ID")))
       print(f"Синхронизировано {len(synced)} команд {'глобально' if not os.environ.get('GUILD_ID') else f'на сервере {os.environ.get("GUILD_ID")}'}.")

    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")



@bot.tree.command(name="send_embed", description="Отправить embed сообщение")
async def send_embed(
    interaction: discord.Interaction, 
    title: Option(str, "Заголовок embed", required=True),
    description: Option(str, "Описание embed", required=True),
    image: Option(str, "URL изображения", required=False),
    avatar: Option(str, "URL аватара", required=False),

):

    embed = Embed(title=title, description=description)
    if image:
        embed.set_image(url=image)
    if avatar:
        embed.set_thumbnail(url=avatar)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="edit_embed", description="Редактировать embed сообщение")
async def edit_embed(
        interaction: discord.Interaction,
        message_id: Option(str, "ID сообщения для редактирования", required=True),
        title: Option(str, "Новый заголовок", required=False),
        description: Option(str, "Новое описание", required=False),
        image: Option(str, "Новый URL изображения", required=False),
        avatar: Option(str, "Новый URL аватара", required=False)
):
    try:
        message = await interaction.channel.fetch_message(int(message_id)) # Получение сообщения

        # Создание нового embed на основе старого или нового, если указаны
        new_embed = message.embeds[0].to_dict() if message.embeds else {}

        if title:
            new_embed["title"] = title
        if description:
            new_embed["description"] = description
        if image:
            new_embed["image"] = {"url": image}
        if avatar:
            new_embed["thumbnail"] = {"url": avatar}


        await message.edit(embed=Embed.from_dict(new_embed)) # Изменение сообщения
        await interaction.response.send_message("Embed сообщение отредактировано!", ephemeral=True)

    except discord.NotFound:
        await interaction.response.send_message("Сообщение не найдено!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Произошла ошибка: {e}", ephemeral=True)



@bot.tree.command(name="json_embed", description="Показать JSON embed сообщения")
async def json_embed(interaction: discord.Interaction, message_id: Option(str, "ID сообщения", required=True)):
    try:
        message = await interaction.channel.fetch_message(int(message_id))

        if message.embeds:
           embed_json = message.embeds[0].to_dict()
           await interaction.response.send_message(f"```json\n{embed_json}\n```") # Отправка JSON в code block
        else:
            await interaction.response.send_message("У сообщения нет embed.", ephemeral=True)

    except discord.NotFound:
        await interaction.response.send_message("Сообщение не найдено.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Произошла ошибка: {e}", ephemeral=True)




# save_embed пока закомментирована из-за необходимости выбора способа сохранения
# @bot.tree.command(name="save_embed", description="Сохранить embed")
# async def save_embed(interaction: discord.Interaction, message_id: Option(str, "ID сообщения", required=True)):
#    # ... (логика сохранения embed, требует определения способа сохранения)
#    pass



bot.run(os.environ['DISCORD_TOKEN'])