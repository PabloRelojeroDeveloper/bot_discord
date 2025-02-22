import os
import discord
import asyncio
import requests
import json
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord import app_commands
from mcrcon import MCRcon
import random
from datetime import datetime, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect
import threading
from spotipy import Spotify
import openai
import aiohttp
import googletrans
import wavelink
import logging
from discord.utils import get
import yt_dlp
from discord.ui import View, button
import spotdl
import subprocess
from spotipy import SpotifyClientCredentials
from spotipy import Spotify
from collections import deque
import concurrent.futures
from discord import Embed
import aiohttp
from mcstatus import JavaServer



TOKEN = 'MTMxODEzOTg5OTQzMzQ1MTU4MQ.GgoCY3.rIZaSWxBU6vC-uEXtIKnIHt0n5sCTrZhkQdkqQ'
MINECRAFT_SERVER_DIR = r"C:\Users\pablo\OneDrive\Escritorio\network (pokemon y apocalypsis en un server)\server con suuuubs"
MINECRAFT_JAR = "server.jar"
SERVER_PORT = 25565
WHITELIST_CHANNEL_ID = 1328213312810258553
INSTAGRAM_URL = "https://www.instagram.com/sselkie_/"
ADMIN_USER_ID = 537046092752093202
RCON_HOST = "localhost" 
RCON_PORT = 25575       
RCON_PASSWORD = "ASD"
autorizados = [537046092752093202]
queue = ["Canción 1", "Canción 2", "Canción 3"]
current_song = 0
SPOTIFY_CLIENT_ID = 'e3c81e068f304cf995700605c333d69a'
SPOTIFY_CLIENT_SECRET = '63f95196aa7b4ed6bfbd55899c9db159'
SPOTIFY_TOKEN = "BQCJuXbP7FxsO-1mG14bqu-If8BzRtGWgEpJ2EuAdBHjfcACTMIxvdRnhBm4B18ijnksv2C-idZxDbCSUBENGNHrN2WvnX_5hCYAeOmzz6PFkOXXvjM"
url = 'https://api.spotify.com/v1/tracks/7epHo3miOIJ3fYEPAdCAf9'
NEWS_FILE_PATH = "C:/xampp/htdocs/launcher/news-launcher/news.json"
CHANNEL_ID_UPDATES = 1334548036558524566
TWITCH_CLIENT_ID = "te0vq04pnmg33rie4e2q59owgtlxil"
TWITCH_CLIENT_SECRET = "7i328ush3npaok2pqtbnej5ga8rnf8"
TWITCH_USER = "selkie_"
DISCORD_CHANNEL_ID = 1090826565270642698
CHANNEL_ID = 1337051754939813921


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


token_url = "https://id.twitch.tv/oauth2/token"
stream_url = "https://api.twitch.tv/helix/streams?user_login=" + TWITCH_USER

token_data = {
    "client_id": TWITCH_CLIENT_ID,
    "client_secret": TWITCH_CLIENT_SECRET,
    "grant_type": "client_credentials"
}

import discord
from discord.ui import Button, View
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch
import asyncio

class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch = None
        self.streamers_status = {}
        
    async def initialize_twitch(self, client_id, client_secret, streamers):
        self.twitch = await Twitch(client_id, client_secret)
        self.streamers_status = {streamer.lower(): False for streamer in streamers}
        self.check_streams.start()

    @tasks.loop(seconds=1)  # Ahora revisará cada 10 segundos en vez de 1 minuto
    async def check_streams(self):
        if not self.twitch:
            return
            
        try:
            users = []
            async for user in self.twitch.get_users(logins=list(self.streamers_status.keys())):
                users.append(user)
            
            if not users:
                return
                
            user_map = {str(user.id): user.login for user in users}
            
            live_streams = {}
            async for stream in self.twitch.get_streams(user_id=list(user_map.keys())):
                live_streams[str(stream.user_id)] = stream
            
            channel = self.bot.get_channel(CHANNEL_ID)
            if not channel:
                print(f"No se pudo encontrar el canal con ID {CHANNEL_ID}")
                return
            
            for user_id, username in user_map.items():
                is_live = user_id in live_streams
                username_lower = username.lower()
                
                if is_live and not self.streamers_status[username_lower]:
                    stream_data = live_streams[user_id]
                    stream_title = stream_data.title
                    stream_game = stream_data.game_name or 'Just Chatting'
                    stream_viewers = stream_data.viewer_count
                    stream_url = f"https://www.twitch.tv/{username}"
                    stream_thumbnail = stream_data.thumbnail_url.replace("{width}", "1280").replace("{height}", "720")
                    
                    embed = discord.Embed(
                        title=f"{username} is now live on Twitch!",
                        description=f"[{stream_title}]({stream_url})",
                        color=0x6441a5
                    )
                    embed.add_field(name="Game", value=stream_game, inline=True)
                    embed.add_field(name="Viewers", value=str(stream_viewers), inline=True)
                    embed.set_image(url=stream_thumbnail)
                    embed.set_thumbnail(url="https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png")
                    
                    button = Button(label="Watch Stream", url=stream_url, style=discord.ButtonStyle.link)
                    view = View()
                    view.add_item(button)
                    
                    await channel.send(content=f"@everyone ¡{username} ha iniciado stream!", embed=embed, view=view)
                    print(f"Notificación enviada para {username}")
                
                self.streamers_status[username_lower] = is_live
                
        except Exception as e:
            print(f"Error checking streams status: {e}")
            import traceback
            traceback.print_exc()

    @check_streams.before_loop
    async def before_check_streams(self):
        await self.bot.wait_until_ready()

# Configuración
TWITCH_CLIENT_ID = 'cplf97vljjq97hhjtwpqnru78f5up6'
TWITCH_CLIENT_SECRET = 'l4kf4uea2ghejo3t9tq50senp5hbth'
CHANNEL_ID = 1307882628665311245  # ID del canal de Discord
STREAMERS = ['pablitorelojero', 'selkie_', 'xtomiiii']
DISCORD_TOKEN = 'MTMxODEzOTg5OTQzMzQ1MTU4MQ.GgoCY3.rIZaSWxBU6vC-uEXtIKnIHt0n5sCTrZhkQdkqQ'

@bot.event
async def on_ready():
    print(f'Bot está listo como: {bot.user.name}')
    notifier = TwitchNotifier(bot)
    await notifier.initialize_twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, STREAMERS)
    await bot.add_cog(notifier)
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())

def main():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()

class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.access_token = None
        self.headers = None
        self.stream_live = False
        self.get_twitch_token.start()
        self.check_stream.start()

    @tasks.loop(hours=1)
    async def get_twitch_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=token_data) as resp:
                data = await resp.json()
                self.access_token = data["access_token"]
                self.headers = {
                    "Client-ID": TWITCH_CLIENT_ID,
                    "Authorization": f"Bearer {self.access_token}"
                }

    @tasks.loop(minutes=1)
    async def check_stream(self):
        if not self.access_token:
            return
        async with aiohttp.ClientSession() as session:
            async with session.get(stream_url, headers=self.headers) as resp:
                data = await resp.json()
                is_live = len(data["data"]) > 0
                if is_live and not self.stream_live:
                    self.stream_live = True
                    channel = self.bot.get_channel(DISCORD_CHANNEL_ID)
                    if channel:
                        await channel.send(f"🎥 {TWITCH_USER} está en vivo! Ve a verlo: https://www.twitch.tv/{TWITCH_USER}")
                elif not is_live:
                    self.stream_live = False

    @get_twitch_token.before_loop
    async def before_get_twitch_token(self):
        await self.bot.wait_until_ready()

    @check_stream.before_loop
    async def before_check_stream(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TwitchNotifier(bot))


def get_bot_instance(guild_id):
    if guild_id not in active_bots:
        active_bots[guild_id] = Bot()
        if str(guild_id) in server_settings:
            settings = server_settings[str(guild_id)]
            active_bots[guild_id].log_channel_id = settings.get('log_channel_id')
            active_bots[guild_id].transcript_channel_id = settings.get('transcript_channel_id')
            active_bots[guild_id].ticket_category_id = settings.get('ticket_category_id')
            active_bots[guild_id].mod_role_id = settings.get('mod_role_id')
            active_bots[guild_id].support_role_id = settings.get('support_role_id')
    return active_bots[guild_id]

isolated_users = {}


def save_data():
    data = {
        'warnings': warnings,
        'projects': projects,
        'server_settings': {},
        'isolated_users': isolated_users
    }
    for guild_id, bot_instance in active_bots.items():
        data['server_settings'][str(guild_id)] = {
            'log_channel_id': bot_instance.log_channel_id,
            'transcript_channel_id': bot_instance.transcript_channel_id,
            'ticket_category_id': bot_instance.ticket_category_id,
            'mod_role_id': bot_instance.mod_role_id,
            'support_role_id': bot_instance.support_role_id,
        }
    
    with open('bot_data.json', 'w') as f:
        json.dump(data, f)

def load_data():
    global warnings, projects, isolated_users
    try:
        with open('bot_data.json', 'r') as f:
            data = json.load(f)
            warnings = data.get('warnings', {})
            projects = data.get('projects', ["Proyecto 1: Squid Spyne games", "Ejemplo: Ejemplo", "Ejemplo 2: Ejemplo 2"])
            isolated_users = data.get('isolated_users', {})
            return data.get('server_settings', {})
    except FileNotFoundError:
        warnings = {}
        projects = ["Proyecto 1: Squid Spyne games", "Ejemplo: Ejemplo", "Ejemplo 2: Ejemplo 2"]
        isolated_users = {}
        return {}

load_data()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)
        self.log_channel_id = None
        self.transcript_channel_id = None
        self.ticket_category_id = None
        self.ticket_counter = 0
        self.tickets = {}
        self.mod_role_id = None
        self.support_role_id = None
        
        if not os.path.exists('transcripts'):
            os.makedirs('transcripts')

    async def setup_hook(self):
        await self.tree.sync()

bot = Bot()
warnings = {}
projects = ["Proyecto 1: Squid Spyne games", "Ejemplo: Ejemplo", "Ejemplo 2: Ejemplo 2"]
active_giveaways = {}
server_settings = load_data()
server_online = False
active_bots = {}

@tasks.loop(seconds=10)
async def check_news_update():
    global last_modified
    print("✓ Verificando actualizaciones...")
    
    try:
        if not os.path.exists(NEWS_FILE_PATH):
            print(f"❌ Archivo no encontrado: {NEWS_FILE_PATH}")
            return
        
        modified_time = os.path.getmtime(NEWS_FILE_PATH)
        print(f"📂 Última modificación: {datetime.fromtimestamp(modified_time)}")
        
        if last_modified is None or modified_time > last_modified:
            print("🔄 Detectada nueva actualización!")
            last_modified = modified_time
            await send_news_embed()
            
    except Exception as e:
        print(f"❌ Error en check_news_update: {str(e)}")

CANAL_HISTORIAS_ID = 1335291654579425371



@bot.event
async def on_message(message):
    # No procesar mensajes del bot
    if message.author.bot:
        return

    # Procesar comandos primero
    await bot.process_commands(message)
    
    # Verificar si el mensaje está en el canal de historias
    if message.channel.id == CANAL_HISTORIAS_ID:
        # Verificar permisos del bot
        if not message.channel.permissions_for(message.guild.me).manage_messages:
            print("¡Error! El bot no tiene permisos para eliminar mensajes")
            return
            
        # Esperar 3 segundos
        await asyncio.sleep(3)
        
        try:
            # Intentar eliminar el mensaje
            await message.delete()
            print(f"Mensaje eliminado: {message.content[:50]}...")
        except discord.errors.NotFound:
            print("El mensaje ya fue eliminado")
        except discord.errors.Forbidden:
            print("No tengo permisos para eliminar el mensaje")
        except Exception as e:
            print(f"Error al eliminar mensaje: {str(e)}")

@bot.command()
async def anecdota(ctx, *, contenido=None):
    if contenido is None:
        await ctx.author.send("❌ Debes escribir una historia después del comando. Ejemplo: !historia Mi anécdota aquí")
        return

    try:
        # Obtener el canal donde se enviarán las historias
        canal_historias = bot.get_channel(CANAL_HISTORIAS_ID)
        
        if canal_historias is None:
            await ctx.author.send("❌ Error: No se pudo encontrar el canal de historias.")
            return
        
        # Crear y enviar el embed
        embed = Embed(
            title="📖 Historia Anónima",
            description=contenido,
            color=0x2ECC71
        )
        embed.set_footer(text="Historia compartida anónimamente")
        
        await canal_historias.send(embed=embed)
        
        # Intentar eliminar el mensaje original
        try:
            await ctx.message.delete()
        except Exception as e:
            print(f"No se pudo eliminar el mensaje del comando: {str(e)}")
        
        # Confirmar al usuario
        await ctx.author.send(f"✅ Tu historia anónima ha sido compartida exitosamente en #{canal_historias.name}!")
        
    except Exception as e:
        await ctx.author.send(f"❌ Ocurrió un error: {str(e)}")

async def send_news_embed():
    try:
        print("📤 Intentando enviar embed...")
        
        with open(NEWS_FILE_PATH, "r", encoding="utf-8") as file:
            news_data = json.load(file)
            print(f"📋 Datos cargados: {news_data}")
            
            if not news_data:
                print("❌ Archivo JSON vacío")
                return
                
            latest_news = news_data[-1]
            print(f"📰 Última noticia: {latest_news}")
            
            embed = create_news_embed(latest_news)
            channel = bot.get_channel(CHANNEL_ID_UPDATES)
            print(f"📢 Canal encontrado: {channel}")
            
            if channel:
                await channel.send("@everyone", embed=embed)
                print("✅ Mensaje enviado exitosamente!")
            else:
                print(f"❌ Error: No se encontró el canal {CHANNEL_ID_UPDATES}")
                
    except Exception as e:
        print(f"❌ Error en send_news_embed: {str(e)}")

@bot.command()
async def noticia(ctx):
    try:
        if not os.path.exists(NEWS_FILE_PATH):
            await ctx.send("❌ No se encontró el archivo de noticias.")
            return
        
        with open(NEWS_FILE_PATH, "r", encoding="utf-8") as file:
            news_data = json.load(file)
            
            if not news_data:
                await ctx.send("❌ No hay noticias disponibles.")
                return
                
            latest_news = news_data[-1]
            embed = create_news_embed(latest_news)
            await ctx.send(embed=embed)
            print("✅ Noticia enviada con comando!")
            
    except Exception as e:
        print(f"❌ Error en noticia: {str(e)}")
        await ctx.send("❌ Ocurrió un error al obtener la noticia.")


def create_news_embed(news):
    embed = discord.Embed(
        title=news.get("title", "Nueva Actualización!"),
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.add_field(name="📰 Noticia", value=news.get("content", "Sin contenido"), inline=False)
    embed.add_field(name="✍ Autor", value=news.get("author", "Desconocido"), inline=True)
    embed.add_field(name="📅 Fecha", value=news.get("publish_date", "Fecha no especificada"), inline=True)
    return embed

@check_news_update.before_loop
async def before_check_news():
    print('🔄 Esperando a que el bot esté listo...')
    await bot.wait_until_ready()
    print('✅ Bot listo! Iniciando verificación de actualizaciones...')

def setup(bot):
    print('🔌 Configurando módulo de noticias...')
    check_news_update.start()
    bot.add_command(noticia)



@bot.tree.command(name="embed", description="Crea un mensaje embed personalizado")
@app_commands.describe(
    titulo="El título del embed",
    mensaje="El contenido del mensaje",
    channel_id="ID del canal donde enviar el mensaje (opcional)",
    color="Color del embed en formato hexadecimal (ejemplo: #FF0000)"
)
async def embed(
    interaction: discord.Interaction,
    titulo: str,
    mensaje: str,
    channel_id: str = None,
    color: str = None
):

    embed_color = discord.Color.blue()  
    if color:
        try:

            color = color.strip('#')
            embed_color = discord.Color.from_rgb(
                int(color[0:2], 16),
                int(color[2:4], 16),
                int(color[4:6], 16)
            )
        except:
            await interaction.response.send_message("Color inválido. Usando color por defecto.", ephemeral=True)
    

    embed = discord.Embed(
        title=titulo,
        description=mensaje,
        color=embed_color
    )
    
    if channel_id:
        try:
            channel = bot.get_channel(int(channel_id))
            if channel:
                await channel.send(embed=embed)
                await interaction.response.send_message(f"Embed enviado al canal {channel.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("No se encontró el canal especificado.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("ID de canal inválido.", ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)



class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Problemas Generales", emoji="😕", description="Problemas generales o consultas", value="general"),
            discord.SelectOption(label="Reportar a un usuario", emoji="👥", description="Si hay algun problema con un usuario abre ticket en esta categoria", value="Report"),
            discord.SelectOption(label="Problemas al sincronizar tu cuenta de Discord con Twitch", emoji="🖥️", description="Soporte para sincronizar cuentas", value="Sync"),
            discord.SelectOption(label="Servidor de minecraft", emoji="⛏️", description="Bugs o problemas con el servidor de minecraft de subs de Selkie", value="Minecraft")
        ]
        super().__init__(placeholder="Selecciona el motivo del ticket", options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        bot_instance = get_bot_instance(interaction.guild_id)
        
        if not bot_instance.ticket_category_id:
            await interaction.response.send_message("La categoría de tickets no está configurada", ephemeral=True)
            return

        category = interaction.guild.get_channel(bot_instance.ticket_category_id)
        if not category:
            await interaction.response.send_message("La categoría de tickets no existe", ephemeral=True)
            return

        bot_instance.ticket_counter += 1
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        if bot_instance.support_role_id:
            support_role = interaction.guild.get_role(bot_instance.support_role_id)
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        reason_text = next((opt.label for opt in self.options if opt.value == self.values[0]), "Desconocido")
        ticket_channel = await interaction.guild.create_text_channel(
            f"ticket-{bot_instance.ticket_counter}-{self.values[0]}",
            category=category,
            overwrites=overwrites
        )

        bot_instance.tickets[ticket_channel.id] = []

        embed = discord.Embed(
            title=f"Ticket Creado - {reason_text}",
            description="El staff te atenderá pronto.",
            color=discord.Color.green()
        )
        embed.add_field(name="Usuario", value=interaction.user.mention)
        embed.add_field(name="Motivo", value=reason_text)
        
        close_view = CloseTicketView()
        await ticket_channel.send(f"{interaction.user.mention}", embed=embed, view=close_view)
        await interaction.response.send_message(f"Ticket creado: {ticket_channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)



    @discord.ui.button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_instance = get_bot_instance(interaction.guild_id)
        
        if not bot_instance.transcript_channel_id:
            await interaction.response.send_message("El canal de transcripts no está configurado", ephemeral=True)
            return

        channel_id = interaction.channel.id
        if channel_id not in bot_instance.tickets:
            await interaction.response.send_message("Este canal no es un ticket válido", ephemeral=True)
            return

        await interaction.response.send_message("Cerrando ticket y generando transcript...")

        transcript_channel = interaction.guild.get_channel(bot_instance.transcript_channel_id)
        if not transcript_channel:
            await interaction.followup.send("Error: Canal de transcripts no encontrado")
            return

        messages = []
        async for message in interaction.channel.history(limit=None, oldest_first=True):
            if message.content:
                messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author}: {message.content}")
            for attachment in message.attachments:
                messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author}: [Archivo adjunto: {attachment.url}]")

        transcript_content = f"Transcript del ticket: {interaction.channel.name}\n\n" + "\n".join(messages)
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f"transcript-{interaction.channel.name}-{timestamp}.txt"
        filepath = os.path.join('transcripts', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(transcript_content)
        
        with open(filepath, 'rb') as f:
            file = discord.File(f, filename=filename)
            embed = discord.Embed(
                title=f"Transcript del Ticket: {interaction.channel.name}",
                description=f"Ticket cerrado por: {interaction.user.mention}",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            await transcript_channel.send(embed=embed, file=file)

        try:
            os.remove(filepath)
        except:
            pass
            
        await asyncio.sleep(5)
        await interaction.channel.delete()

async def send_log(guild, moderator, action, target, reason):
    bot_instance = get_bot_instance(guild.id)
    if bot_instance.log_channel_id:
        log_channel = guild.get_channel(bot_instance.log_channel_id)
        if log_channel:
            embed = discord.Embed(title=f"Acción de Moderación: {action}", color=discord.Color.red())
            embed.add_field(name="Moderador", value=moderator.mention)
            embed.add_field(name="Usuario Afectado", value=target.mention)
            embed.add_field(name="Razón", value=reason)
            embed.timestamp = datetime.now()
            await log_channel.send(embed=embed)







def has_mod_role():
    async def predicate(interaction: discord.Interaction):
        bot_instance = get_bot_instance(interaction.guild_id)
        if not bot_instance.mod_role_id:
            if interaction.user.guild_permissions.administrator:
                return True
            return False
        role = interaction.guild.get_role(bot_instance.mod_role_id)
        return role in interaction.user.roles or interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)

@bot.tree.command(name="setmodrole")
@app_commands.default_permissions(administrator=True)
async def setmodrole(interaction: discord.Interaction, role: discord.Role):
    bot_instance = get_bot_instance(interaction.guild_id)
    bot_instance.mod_role_id = role.id
    save_data()
    await interaction.response.send_message(f"Rol de moderación establecido en: {role.mention}")

@bot.tree.command(name="comandos")
@app_commands.default_permissions(administrator=True)
@has_mod_role()
async def comandos(interaction: discord.Interaction):
    """Muestra una lista de todos los comandos disponibles"""
    
    comandos_list = {
        "🛠️ Configuración": {
            "/setmodrole": "Establece el rol de moderación",
            "/setsupportrole": "Establece el rol de soporte",
            "/setticketcategory": "Establece la categoría para los tickets",
            "/setuptickets": "Configura el sistema de tickets en un canal",
            "/setlogchannel": "Establece el canal para logs de moderación",
            "/settranscriptchannel": "Establece el canal para transcripts de tickets"
        },
        "🚫 Moderación": {
            "/kick": "Expulsa a un usuario del servidor",
            "/ban": "Banea permanentemente a un usuario",
            "/tempban": "Aísla temporalmente a un usuario (timeout)",
            "/untimeout": "Remueve el aislamiento temporal de un usuario",
            "/warn": "Advierte a un usuario (3 advertencias = expulsión)"
        },
        "🎫 Tickets": {
            "Sistema de Tickets": "Los usuarios pueden crear tickets desde el panel configurado con /setuptickets"
        },
        "🎉 Sorteos": {
            "/giveaway": "Crea un nuevo sorteo con premio y duración específicos"
        },
        "📋 Proyectos": {
            "/proyectos": "Muestra la lista de proyectos actuales",
            "/addproject": "Añade un nuevo proyecto a la lista",
            "/removeproject": "Elimina un proyecto de la lista",
            "/editproject": "Edita un proyecto existente"
        },
        "ℹ️ Información": {
            "/comandos": "Muestra esta lista de comandos disponibles"
        }
    }

    embeds = []
    for categoria, comandos in comandos_list.items():
        embed = discord.Embed(
            title=f"{categoria}",
            color=discord.Color.blue()
        )
        
        for comando, descripcion in comandos.items():
            embed.add_field(
                name=comando,
                value=descripcion,
                inline=False
            )
        
        embeds.append(embed)

    await interaction.response.send_message(embeds=embeds)

@bot.tree.command(name="setsupportrole")
@app_commands.default_permissions(administrator=True)
async def setsupportrole(interaction: discord.Interaction, role: discord.Role):
    bot_instance = get_bot_instance(interaction.guild_id)
    bot_instance.support_role_id = role.id
    save_data()
    await interaction.response.send_message(f"Rol de soporte establecido en: {role.mention}")

@bot.tree.command(name="setticketcategory")
@app_commands.default_permissions(administrator=True)
async def setticketcategory(interaction: discord.Interaction, category: discord.CategoryChannel):
    bot_instance = get_bot_instance(interaction.guild_id)
    bot_instance.ticket_category_id = category.id
    save_data()
    await interaction.response.send_message(f"Categoría de tickets establecida en: {category.name}")

@bot.tree.command(name="setuptickets")
@app_commands.default_permissions(administrator=True)
async def setuptickets(interaction: discord.Interaction, channel: discord.TextChannel):
    embed = discord.Embed(
        title="Sistema de Tickets",
        description="Selecciona el motivo de tu ticket en el menú de abajo",
        color=discord.Color.blue()
    )
    await channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("Sistema de tickets configurado", ephemeral=True)

@bot.tree.command(name="setlogchannel")
@app_commands.default_permissions(administrator=True)
async def setlogchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    bot_instance = get_bot_instance(interaction.guild_id)
    bot_instance.log_channel_id = channel.id
    save_data()
    await interaction.response.send_message(f"Canal de logs establecido en {channel.mention}")

@bot.tree.command(name="settranscriptchannel")
@app_commands.default_permissions(administrator=True)
async def settranscriptchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    bot_instance = get_bot_instance(interaction.guild_id)
    bot_instance.transcript_channel_id = channel.id
    save_data()
    await interaction.response.send_message(f"Canal de transcripts establecido en {channel.mention}")

@bot.tree.command(name="kick")
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Usuario {member.mention} ha sido expulsado")
    await send_log(interaction.guild, interaction.user, "Kick", member, reason)


@bot.tree.command(name="ban")
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"Usuario {member.mention} ha sido baneado")
    await send_log(interaction.guild, interaction.user, "Ban", member, reason)




@bot.tree.command(name="tempban")
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def tempban(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str):
    if not interaction.guild.me.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ No tengo permisos para aislar miembros. Necesito el permiso 'Aislar miembros'.", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("❌ No puedo aislar a este usuario porque su rol es superior al mío.", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ No puedes aislar a este usuario porque su rol es superior al tuyo.", ephemeral=True)
        return

    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ No puedo aislar al dueño del servidor.", ephemeral=True)
        return

    try:
        timeout_duration = timedelta(minutes=duration)
        await member.timeout(timeout_duration, reason=reason)
        
        embed = discord.Embed(
            title="⏰ Usuario Aislado Temporalmente",
            description=f"**Usuario:** {member.mention}\n**Duración:** {duration} minutos\n**Razón:** {reason}",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Aislado por {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)
        await send_log(interaction.guild, interaction.user, "Timeout", member, f"{reason} (Duración: {duration} minutos)")

    except discord.Forbidden:
        await interaction.response.send_message("❌ No tengo los permisos necesarios para aislar a este usuario.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ocurrió un error al intentar aislar al usuario: {str(e)}", ephemeral=True)

@bot.tree.command(name="warn")
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    guild_id = str(interaction.guild.id)
    if guild_id not in warnings:
        warnings[guild_id] = {}
    
    if str(member.id) not in warnings[guild_id]:
        warnings[guild_id][str(member.id)] = []
    
    warnings[guild_id][str(member.id)].append({
        "reason": reason,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    save_data()
    
    warning_count = len(warnings[guild_id][str(member.id)])
    await interaction.response.send_message(f"Usuario {member.mention} ha sido advertido. Total: {warning_count}")
    await send_log(interaction.guild, interaction.user, "Warn", member, reason)
    
    if warning_count >= 3:
        await member.kick(reason="Acumulación de advertencias")
        await interaction.followup.send(f"{member.mention} ha sido expulsado por acumular 3 advertencias")
        await send_log(interaction.guild, interaction.user, "Auto-Kick", member, "Acumulación de 3 advertencias")

@bot.tree.command(name="untimeout")
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.timeout(None, reason="Timeout removido manualmente")
        
        embed = discord.Embed(
            title="✅ Timeout Removido",
            description=f"Se ha removido el aislamiento temporal de {member.mention}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Removido por {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)
        await send_log(interaction.guild, interaction.user, "Timeout Removed", member, "Timeout removido manualmente")

    except discord.Forbidden:
        await interaction.response.send_message("❌ No tengo los permisos necesarios para remover el timeout.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"❌ Ocurrió un error: {str(e)}", ephemeral=True)


@bot.tree.command(name="giveaway")
@app_commands.default_permissions(manage_messages=True)
async def giveaway(interaction: discord.Interaction, duration: int, prize: str, winners: int = 1):
    embed = discord.Embed(
        title="🎉 SORTEO 🎉", 
        description=f"Premio: {prize}\n"
                  f"Duración: {duration} minutos\n"
                  f"Ganadores: {winners}\n\n"
                  "Reacciona con 🎉 para participar!", 
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()
    await message.add_reaction("🎉")
    
    active_giveaways[message.id] = {
        "prize": prize, 
        "end_time": datetime.now() + timedelta(minutes=duration),
        "winners": winners
    }
    
    await asyncio.sleep(duration * 60)
    message = await interaction.channel.fetch_message(message.id)
    users = [user async for user in message.reactions[0].users() if not user.bot]
    
    if users:
        num_winners = min(winners, len(users))
        selected_winners = random.sample(users, num_winners)
        
        winners_text = ", ".join([winner.mention for winner in selected_winners])
        await interaction.channel.send(f"🎉 ¡Felicitaciones {winners_text}! Han ganado: {prize}")
    else:
        await interaction.channel.send("No hubo participantes en el sorteo")
    
    del active_giveaways[message.id]

@bot.tree.command(name="addproject")
@app_commands.default_permissions(administrator=True)
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def add_project(interaction: discord.Interaction, project: str):
    projects.append(project)
    save_data()
    await interaction.response.send_message(f"Proyecto añadido: {project}")

@bot.tree.command(name="removeproject")
@app_commands.default_permissions(administrator=True)
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def remove_project(interaction: discord.Interaction, index: int):
    if 1 <= index <= len(projects):
        removed_project = projects.pop(index - 1)
        save_data()
        await interaction.response.send_message(f"Proyecto eliminado: {removed_project}")
    else:
        await interaction.response.send_message("Índice de proyecto inválido")

@bot.tree.command(name="editproject")
@app_commands.default_permissions(administrator=True)
@has_mod_role()
@app_commands.default_permissions(administrator=True)
async def edit_project(interaction: discord.Interaction, index: int, new_name: str):
    if 1 <= index <= len(projects):
        old_project = projects[index - 1]
        projects[index - 1] = new_name
        save_data()
        await interaction.response.send_message(f"Proyecto editado:\nAntes: {old_project}\nAhora: {new_name}")
    else:
        await interaction.response.send_message("Índice de proyecto inválido")

@bot.tree.command(name="proyectos")
async def proyectos(interaction: discord.Interaction):
    project_list = "\n".join([f"{i+1}. {project}" for i, project in enumerate(projects)])
    embed = discord.Embed(
        title="📋 Proyectos Actuales", 
        description=project_list, 
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)


class PlayerView(discord.ui.View):
    def __init__(self, voice_client, music_player, interaction):
        super().__init__(timeout=None)
        self.voice_client = voice_client
        self.music_player = music_player
        self.interaction = interaction
        self.paused = False

    @discord.ui.button(label="⏸️ Pausar", style=discord.ButtonStyle.primary, row=0)
    async def pause_resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_interaction_author(interaction):
            return

        if self.voice_client.is_playing() and not self.paused:
            self.voice_client.pause()
            self.paused = True
            button.label = "▶️ Reanudar"
            button.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
        elif self.paused:
            self.voice_client.resume()
            self.paused = False
            button.label = "⏸️ Pausar"
            button.style = discord.ButtonStyle.primary
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("No hay nada reproduciéndose.", ephemeral=True)

    @discord.ui.button(label="⏭️ Siguiente", style=discord.ButtonStyle.success, row=0)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_interaction_author(interaction):
            return

        if self.voice_client.is_playing() or self.paused:
            self.voice_client.stop()
            await interaction.response.send_message("⏭️ Pasando a la siguiente canción...", ephemeral=True)
            await self.music_player.play_next(self.interaction)
        else:
            await interaction.response.send_message("No hay nada reproduciéndose.", ephemeral=True)

    async def check_interaction_author(self, interaction: discord.Interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message(
                "Solo quien solicitó la música puede usar los controles.", 
                ephemeral=True
            )
            return False
        return True
    


class MusicPlayer:
    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.queue = deque()
        self.history = deque(maxlen=10)
        self.currently_playing = None
        self.is_playing = False
        self.processing_playlist = False
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.loop_mode = "OFF"  # OFF, SINGLE, ALL
        self.volume = 1.0
        self.loading_task = None
        self.processing_playlist = False
        self.processing_task = None
        self.processing_progress = 0
        self.total_tracks = 0
        self.temp_queue = deque()
        self.shuffle_requested = False
        self.status_message = None  # Para rastrear el mensaje de estado
        self.loading_message = None # Para rastrear el mensaje de carga
        self.current_song_message = None  # Para rastrear el embed de la canción actual
        self.first_song_played = False  # Nueva variable para rastrear si la primera canción ya se reprodujo



        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }

        self.ytdl = yt_dlp.YoutubeDL(self.YTDL_OPTIONS)

        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id='e3c81e068f304cf995700605c333d69a',
            client_secret='63f95196aa7b4ed6bfbd55899c9db159'
        ))

    def shuffle_queue(self):
        random.shuffle(self.queue)

    async def get_song_info(self, url):
        if 'spotify.com' in url:
            tracks = await self.get_spotify_tracks(url)
            return tracks if 'playlist' in url else tracks[0]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.thread_pool, lambda: self.ytdl.extract_info(url, download=False))


    async def get_spotify_tracks(self, url):
        if 'playlist' in url:
            playlist_id = url.split('/')[-1].split('?')[0]
            results = self.sp.playlist_tracks(playlist_id)
            
            if not results['items']:
                return []
                
            # Si shuffle está activado, elegir una canción aleatoria como primera
            if self.shuffle_requested:
                first_track = random.choice(results['items'])['track']
            else:
                first_track = results['items'][0]['track']
                
            search_query = f"{first_track['name']} - {first_track['artists'][0]['name']}"
            youtube_url = await self.search_youtube(search_query)
            if youtube_url:
                return [await self.get_song_info(youtube_url)]
            return []
        elif 'track' in url:
            track_id = url.split('/')[-1].split('?')[0]
            track = self.sp.track(track_id)
            search_query = f"{track['name']} - {track['artists'][0]['name']}"
            youtube_url = await self.search_youtube(search_query)
            return [await self.get_song_info(youtube_url)]

    async def search_youtube(self, query):
        loop = asyncio.get_event_loop()
        search_url = f"ytsearch1:{query}"
        info = await loop.run_in_executor(self.thread_pool, lambda: self.ytdl.extract_info(search_url, download=False))
        if 'entries' in info and info['entries']:
            return f"https://youtube.com/watch?v={info['entries'][0]['id']}"
        return None
    


    async def process_playlist_async(self, url, interaction, shuffle=False):
        """Procesa una playlist de manera asíncrona mientras se reproduce música."""
        try:
            playlist_id = url.split('/')[-1].split('?')[0]
            results = self.sp.playlist_tracks(playlist_id)
            self.total_tracks = len(results['items'])
            self.processing_progress = 0
            self.shuffle_requested = shuffle
            
            # Crear o actualizar el mensaje de estado
            if not self.status_message:
                self.status_message = await interaction.followup.send(
                    "⏳ Cargando playlist: 0%"
                )
            else:
                await self.status_message.edit(content="⏳ Cargando playlist: 0%")

            # Comenzamos desde la segunda canción (índice 1)
            for i, item in enumerate(results['items'][1:], 1):
                if not self.processing_playlist:
                    break

                track = item['track']
                search_query = f"{track['name']} - {track['artists'][0]['name']}"
                try:
                    youtube_url = await self.search_youtube(search_query)
                    if youtube_url:
                        info = await self.get_song_info(youtube_url)
                        self.temp_queue.append(info)
                        
                        if self.shuffle_requested and len(self.temp_queue) > 1:
                            insert_position = random.randint(0, len(self.queue))
                            self.queue.insert(insert_position, self.temp_queue.popleft())
                        else:
                            self.queue.append(self.temp_queue.popleft())
                        
                        self.processing_progress = (i / (self.total_tracks - 1)) * 100

                        # Actualizar el mensaje de estado cada 5 canciones o cuando sea la última
                        if i % 5 == 0 or i == self.total_tracks - 1:
                            try:
                                await self.status_message.edit(
                                    content=f"⏳ Cargando playlist: {self.processing_progress:.1f}% ({i}/{self.total_tracks-1} canciones)"
                                )
                            except:
                                pass

                except Exception as e:
                    print(f"Error al procesar {search_query}: {e}")
                    continue

            # Manejar las canciones restantes en la cola temporal
            while self.temp_queue:
                if self.shuffle_requested:
                    insert_position = random.randint(0, len(self.queue))
                    self.queue.insert(insert_position, self.temp_queue.popleft())
                else:
                    self.queue.append(self.temp_queue.popleft())

            if self.processing_playlist:
                await self.status_message.edit(
                    content=f"✅ Playlist cargada completamente: {self.total_tracks - 1} canciones añadidas" + 
                    (" y mezcladas" if shuffle else "")
                )
            
            self.processing_playlist = False
            self.status_message = None

        except Exception as e:
            await interaction.followup.send(f"Error al procesar la playlist: {e}")
            self.processing_playlist = False
            self.status_message = None

    async def play_next(self, interaction):
        # Si es la primera reproducción y aún no hay nada reproduciéndose
        if not self.first_song_played and (self.queue or self.temp_queue):
            self.first_song_played = True
            if not self.queue and self.temp_queue:
                self.queue.append(self.temp_queue.popleft())

        if not self.queue and not self.temp_queue and not self.processing_playlist:
            self.is_playing = False
            self.first_song_played = False  # Resetear para futuras reproducciones
            if self.status_message:
                try:
                    await self.status_message.delete()
                except:
                    pass
            await interaction.followup.send("🎵 La cola de reproducción terminó.")
            return
        
        if not self.queue and (self.temp_queue or self.processing_playlist):
            await asyncio.sleep(1)
            if self.queue:
                await self.play_next(interaction)
            return

        # Asegurarnos de detener la reproducción actual
        try:
            if self.voice_client.is_playing():
                self.voice_client.stop()
        except:
            pass

        if self.loop_mode == "SINGLE" and self.currently_playing:
            next_song = self.currently_playing
        else:
            if not self.queue:
                if self.temp_queue:
                    self.queue.append(self.temp_queue.popleft())
                else:
                    return
            next_song = self.queue.popleft()
            if self.loop_mode == "ALL":
                self.queue.append(next_song)

        self.currently_playing = next_song
        self.is_playing = True
        await self.play_song(interaction, next_song)

    async def play_song(self, interaction, song_info):
        try:
            url = song_info.get('url') or song_info.get('formats', [{}])[0].get('url')
            if not url:
                url = await self.get_stream_url(song_info['webpage_url'])

            source = await discord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)
            
            # Crear el embed para la canción actual
            embed = discord.Embed(
                title="🎵 Ahora reproduciendo",
                description=f"**{song_info['title']}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Duración", value=str(timedelta(seconds=song_info.get('duration', 0))))
            embed.add_field(name="Canal", value=song_info.get('uploader', 'Desconocido'))

            # Si ya existe un mensaje con el embed, actualizarlo
            if self.current_song_message:
                try:
                    await self.current_song_message.edit(embed=embed)
                except discord.NotFound:
                    # Si el mensaje no se encuentra, crear uno nuevo
                    self.current_song_message = await interaction.followup.send(embed=embed)
            else:
                # Si es la primera canción, crear el mensaje
                self.current_song_message = await interaction.followup.send(embed=embed)

            # Reproducir la canción después de actualizar el embed
            self.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(interaction), 
                bot.loop
            ))

        except Exception as e:
            # Solo enviar mensaje de error si no es "Already playing audio"
            if str(e) != "Already playing audio.":
                await interaction.followup.send(f"Error al reproducir la canción: {e}")

@bot.tree.command(name="play", description="Reproduce una canción o playlist desde YouTube o Spotify.")
@app_commands.describe(url="URL de la canción o playlist", shuffle="Mezclar la playlist si es aplicable")
async def play(interaction: discord.Interaction, url: str, shuffle: bool = False):
    try:
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("Debes estar en un canal de voz para usar este comando.", ephemeral=True)
            return

        await interaction.response.defer()

        if not interaction.guild.voice_client:
            vc = await interaction.user.voice.channel.connect()
        else:
            vc = interaction.guild.voice_client

        if not hasattr(bot, 'music_player'):
            bot.music_player = MusicPlayer(vc)

        music_player = bot.music_player

        if 'spotify.com' in url and 'playlist' in url:
            music_player.shuffle_requested = shuffle  # Establecer antes de get_spotify_tracks
            first_song = await music_player.get_spotify_tracks(url)
            
            if first_song and first_song[0]:
                music_player.queue.append(first_song[0])  # Siempre añadir a la cola principal
                
                loading_msg = await interaction.followup.send(
                    "🎶 Reproduciendo la primera canción mientras se carga el resto de la playlist..."
                )
                music_player.loading_message = loading_msg
                music_player.first_song_played = False  # Resetear el estado
                
                # Iniciar el procesamiento asíncrono de la playlist
                music_player.processing_playlist = True
                music_player.processing_task = asyncio.create_task(
                    music_player.process_playlist_async(url, interaction, shuffle=shuffle)
                )
                
                # Asegurarnos de que la reproducción comience
                if not music_player.is_playing:
                    await music_player.play_next(interaction)
        else:
            info = await music_player.get_song_info(url)
            if isinstance(info, list):
                for track in info:
                    music_player.queue.append(track)
                if shuffle:
                    music_player.shuffle_queue()
                    await interaction.followup.send(f"Playlist añadida con {len(info)} canciones y mezclada.")
                else:
                    await interaction.followup.send(f"Playlist añadida con {len(info)} canciones.")
            else:
                music_player.queue.append(info)
                await interaction.followup.send(f"🎶 Canción añadida: **{info['title']}**")

        if not music_player.is_playing:
            await music_player.play_next(interaction)

        view = PlayerView(vc, music_player, interaction)
        await interaction.followup.send("🎵 Controles del reproductor:", view=view)

    except Exception as e:
        if interaction.response.is_done():
            await interaction.followup.send(f"Error al procesar la solicitud: {e}")
        else:
            await interaction.response.send_message(f"Error crítico al procesar la solicitud: {e}", ephemeral=True)







@bot.command()
async def clear(ctx):
    if not hasattr(bot, 'music_player'):
        await ctx.send("No hay un reproductor de música inicializado.")
        return

    bot.music_player.queue.clear()
    await ctx.send("🗑️ Cola de reproducción limpiada.")

ytdl_format_options = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "noplaylist": False,
    "extract_flat": "in_playlist"
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)



@bot.command(name='leave')
async def leave(ctx):
    player = ctx.voice_client
    if not player:
        await ctx.send("El bot no está conectado a un canal de voz.")
        return
    await player.disconnect()
    await ctx.send("Me he desconectado del canal de voz.")


@bot.command()
async def announce(ctx, *, message: str):
    await ctx.message.delete()
    embed = discord.Embed(
        title="ANUNCIO MUY IMPORTANTE",
        description=message,
        color=discord.Color.green()
    )
    spoiler_mention = "||@everyone||"
    await ctx.send(content=spoiler_mention, embed=embed)



@bot.tree.command(name="comandos-admin", description="Muestra una lista de comandos disponibles para moderacion.")
async def comandos(interaction: discord.Interaction):
    comandos_lista = {
        "/anti-mogolicos": "Mutea a los roles que vos elijas",
        "/mandar": "el bot manda exactamente todo lo que vos mandes despues del comando",
        "/unmuteall": "desmutea a los roles",
        "servers": "Te dice los servers en los que esta el usuario",
        "/announce": "anuncia con un embed y un ping a todos los usuarios lo que vos quieras",

    }

    mensaje = "**Comandos de moderacion disponibles**\n"
    for comando, descripcion in comandos_lista.items():
        mensaje += f"{comando}: {descripcion}\n"

    await interaction.response.send_message(mensaje, ephemeral=True)


@bot.command(name="mandar", help="Envía un mensaje personalizado (solo para el admin).")
async def mandar(ctx, *, mensaje: str):
    if ctx.author.id == ADMIN_USER_ID:
        await ctx.send(mensaje)
        await ctx.message.delete()
    else:
        await ctx.send("No tienes permisos para usar este comando.")

@bot.command(name="reglas", help="Muestra las reglas del servidor.")
async def reglas(ctx):

    embed = discord.Embed(
        title="₊˚๑ ꒰**REGLAS DEL SERVIDOR** ✧ ˚ ｡⊹\n・・ ︶︶︶︶꒷꒦︶︶︶︶꒦꒷︶︶︶︶꒷ ๑ .",
        description="",
        color=discord.Color.purple()  # Barra lateral de color violeta
    )

    # Añadir las reglas con formato de negrita y emojis
    embed.add_field(
        name="**🫧・RESPETO A TODOS Y A LOS MODS**",
        value=(
            "Sean respetuosos entre miembros del servidor y a su vez con los moderadores (tanto en twitch como en discord), "
            "no se va a tolerar comentarios ofensivos a posta, amenazas, faltas de respeto y la fomentación de odio, nada de toxicidad dentro o fuera del servidor."
        ),
        inline=False
    )

    embed.add_field(
        name="**🍒・SIN ACOSO NI SUPLANTAR IDENTIDAD**",
        value=(
            "Está completamente prohibido acosar a cualquier persona del servidor, si llega a suceder alguna forma de acoso "
            "se va a tomar cartas del asunto inmediatamente y la consecuencia va a ser un ban permanente."
        ),
        inline=False
    )

    embed.add_field(
        name="**⚠️ ・CERO CONTENIDO EXPLÍCITO**",
        value=(
            "Está totalmente prohibido el contenido NSFW/+18, violencia, gore y relacionados. Al igual que chistes de mal gustos "
            "referidos a abusos sexuales u homicidios/femicidios. No se va a tolerar, serán advertidos o baneados del servidor."
        ),
        inline=False
    )

    embed.add_field(
        name="**🚨・NO SEAS RARO/A**",
        value=(
            "Se les pide una cosa nada más y es **SENTIDO COMÚN.** Por favor, si son nuevos en el servidor dense a conocer y socialicen "
            "de manera normal, no flasheen confianza al toque porque el server tiene su propio ritmo y no queremos problemas dentro del mismo."
        ),
        inline=False
    )

    embed.add_field(
        name="**🍡・PROHIBIDO EL SPAM**",
        value=(
            "El spam de mensajes está completamente **PROHIBIDO** ya que es molesto. Esto incluye links de otros servidores, links de dudosa "
            "procedencia y cadenas de mensajes, será motivo de baneo."
        ),
        inline=False
    )

    embed.add_field(
        name="**🫡・RESPETAR EL CONTENIDO DE LOS CANALES**",
        value=(
            "Como se puede ver hay varios canales, hasta de jueguitos, cada uno tiene su propio tema de charla, por favor respeten la temática "
            "de cada canal y eviten ser sancionados. **NO UTILIZAR @/everyone**"
        ),
        inline=False
    )

    embed.add_field(
        name="**💌・ANTE CUALQUIER PROBLEMA HABLAR CON LOS MODS**",
        value=(
            "Los mods están divididos entre twitch y discord, si tienes algún problema o inconveniente acudan directamente con el staff mediante un ticket, "
            "para abrir un ticket pueden ir a <#1329355260833169499> y contar la situación. **NO MANDAR MENSAJES PRIVADOS A LOS MODERADORES**."
        ),
        inline=False
    )

    # Enviar el embed
    await ctx.send(embed=embed)




@bot.tree.command(name="anti-mogolicos", description="Silencia ciertos roles para que no puedan hablar.")
@app_commands.describe(
    razon="Razón para activar el anti-mogolicos",
    rol1="Selecciona el primer rol a silenciar",
    rol2="Selecciona el segundo rol a silenciar (opcional)"
)
async def anti_mogolicos(
    interaction: discord.Interaction, 
    razon: str, 
    rol1: discord.Role, 
    rol2: discord.Role = None
):
    if interaction.user.id not in autorizados:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return

    roles = [rol1]
    if rol2:
        roles.append(rol2)

    for role in roles:
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(role, send_messages=False)

    # Alerta en el canal
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerta = (
        f"🚨 **Anti-Mogolicos activado** 🚨\n"
        f"Ejecutado por: {interaction.user.mention}\n"
        f"Fecha y hora: {ahora}\n"
        f"Roles silenciados: {', '.join([role.name for role in roles])}\n"
        f"Razón: {razon}"
    )
    await interaction.response.send_message(alerta)


@bot.tree.command(name="unmuteall", description="Restaura el permiso para hablar a los roles silenciados.")
async def unmuteall(interaction: discord.Interaction):
    if interaction.user.id not in autorizados:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return

    for channel in interaction.guild.text_channels:
        for role_or_member, perms in channel.overwrites.items():  # Iterar sobre las sobrescrituras
            if isinstance(role_or_member, discord.Role):  # Verificar si es un rol
                if perms.send_messages is False:  # Si el permiso está denegado
                    await channel.set_permissions(role_or_member, send_messages=None)

    await interaction.response.send_message("Todos los roles silenciados ahora tienen permiso para hablar.")



@bot.tree.command(name="autorizar", description="Autoriza a un usuario a usar el comando anti-mogolicos.")
@app_commands.describe(usuario="Usuario al que deseas autorizar")
async def autorizar(interaction: discord.Interaction, usuario: discord.Member):
    if interaction.user.id != autorizados[0]:  # Solo el administrador inicial puede autorizar
        await interaction.response.send_message("No tienes permisos para autorizar a otros usuarios.", ephemeral=True)
        return

    if usuario.id in autorizados:
        await interaction.response.send_message(f"{usuario.mention} ya está autorizado.", ephemeral=True)
        return

    autorizados.append(usuario.id)
    await interaction.response.send_message(f"{usuario.mention} ahora está autorizado para usar `/anti-mogolicos`.")

    # Notificar al usuario por privado
    try:
        await usuario.send(
            f"Has sido autorizado para usar el comando `/anti-mogolicos` en el servidor {interaction.guild.name}."
        )
    except discord.Forbidden:
        await interaction.followup.send(
            f"No pude enviar un mensaje privado a {usuario.mention}, pero ya está autorizado."
        )


@bot.tree.command(name="desautorizar", description="Revoca el permiso de un usuario para usar el anti-mogolicos.")
@app_commands.describe(usuario="Usuario al que deseas desautorizar")
async def desautorizar(interaction: discord.Interaction, usuario: discord.Member):
    if interaction.user.id != autorizados[0]:  # Solo el administrador inicial puede desautorizar
        await interaction.response.send_message("No tienes permisos para desautorizar a otros usuarios.", ephemeral=True)
        return

    if usuario.id not in autorizados:
        await interaction.response.send_message(f"{usuario.mention} no está autorizado.", ephemeral=True)
        return

    autorizados.remove(usuario.id)
    await interaction.response.send_message(f"{usuario.mention} ya no está autorizado para usar `/anti-mogolicos`.")

    # Notificar al usuario por privado
    try:
        await usuario.send(
            f"Se te ha revocado el permiso para usar el comando `/anti-mogolicos` en el servidor {interaction.guild.name}."
        )
    except discord.Forbidden:
        await interaction.followup.send(
            f"No pude enviar un mensaje privado a {usuario.mention}, pero ya no está autorizado."
        )


@bot.tree.command(name="servers", description="Ver en qué servidores está un usuario")
async def servers(interaction: discord.Interaction, user: discord.User):
    servers_list = []
    for guild in bot.guilds:
        if user in guild.members:
            servers_list.append(guild.name)

    if servers_list:
        await interaction.response.send_message(f"{user.name} está en los siguientes servidores:\n" + "\n".join(servers_list))
    else:
        await interaction.response.send_message(f"{user.name} no está en ningún servidor que sea parte del bot.")




horoscopos = {
    "aries": "Hoy, Aries, sentirás que tienes toda la energía del universo. ¡Aprovecha para conquistar tus metas! 💪",
    "tauro": "Tauro, es un buen día para relajarte y disfrutar de las pequeñas cosas de la vida. 🌻",
    "geminis": "Géminis, tu mente está clara hoy, perfecto para resolver problemas complicados. 🧠",
    "cancer": "Cáncer, la familia y los amigos estarán cerca para apoyarte. No dudes en pedir ayuda. ❤️",
    "leo": "Leo, hoy es el día para brillar. Deja que tu luz ilumine el camino. 🌟",
    "virgo": "Virgo, es momento de organizar tus ideas y empezar nuevos proyectos. 📝",
    "libra": "Libra, las relaciones sociales serán tu fortaleza hoy. Conecta con los demás. 🤝",
    "escorpio": "Escorpio, las emociones estarán a flor de piel. Mantén la calma y escucha a tu corazón. 💖",
    "sagitario": "Sagitario, es un buen día para explorar nuevas ideas. Abre tu mente. 🌍",
    "capricornio": "Capricornio, hoy es un buen día para centrarte en tus objetivos. ¡No pierdas el enfoque! 🎯",
    "acuario": "Acuario, estarás lleno de ideas innovadoras. Comparte tus pensamientos. 💡",
    "piscis": "Piscis, es un buen momento para cuidar de ti mismo y reflexionar. 🌸"
}

# Lista de Canciones
canciones = [
    {"titulo": "Despacito", "clip": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"},
    {"titulo": "Shape of You", "clip": "https://www.youtube.com/watch?v=JGwWNGJdvx8"},
    {"titulo": "Blinding Lights", "clip": "https://www.youtube.com/watch?v=4NRXx6U8ABQ"},
]

# Lista de Pokémon
pokemones = [
    {"nombre": "Pikachu", "tipo": "Eléctrico", "ataque": 300, "defensa": 250, "velocidad": 400},
    {"nombre": "Bulbasaur", "tipo": "Planta/Veneno", "ataque": 250, "defensa": 300, "velocidad": 250},
    {"nombre": "Charmander", "tipo": "Fuego", "ataque": 350, "defensa": 200, "velocidad": 300},
    {"nombre": "Squirtle", "tipo": "Agua", "ataque": 200, "defensa": 350, "velocidad": 200},
]

RAPIDAPI_KEY = "deefe32036mshfccbe128e5850b2p1e1654jsnd0259abd7a68"
RAPIDAPI_HOST = "vedicrishi-horoscope-matching-v1.p.rapidapi.com"
URL = "rapidapi.com"

# Comando para obtener el horóscopo
@bot.command()
async def horoscopo(ctx, signo: str):
    signo = signo.lower()
    
    signos_validos = ["aries", "tauro", "geminis", "cancer", "leo", "virgo", "libra", "escorpio", "sagitario", "capricornio", "acuario", "piscis"]
    
    if signo not in signos_validos:
        await ctx.send("Lo siento, no reconozco ese signo. Intenta con uno de los 12 signos del zodiaco.")
        return
    
    # Preparar la solicitud con parámetros
    querystring = {"date": "today", "sign": signo}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        # Realizamos la solicitud GET a la API
        response = requests.get(URL, headers=headers, params=querystring)

        # Verificar si la respuesta es exitosa (código 200)
        if response.status_code == 200:
            data = response.json()
            
            # Revisar la estructura de la respuesta
            print(f"Respuesta de la API: {data}")  # Imprimir la respuesta para depurar

            # Extraer el horóscopo
            horoscopo = data.get("horoscope", "No se pudo obtener el horóscopo.")
            
            # Enviar el horóscopo al canal
            await ctx.send(f"**Horóscopo de {signo.capitalize()} para hoy:**\n{horoscopo}")
        else:
            await ctx.send(f"Error al obtener el horóscopo. Código de respuesta: {response.status_code}")
    
    except Exception as e:
        await ctx.send("Lo siento, ocurrió un error al obtener el horóscopo. Intenta más tarde.")
        print(f"Error al obtener el horóscopo: {e}")

# Comando para adivinar la canción
@bot.command()
async def adivina(ctx):
    canción = random.choice(canciones)
    pregunta = f"🎶 ¡Adivina la canción! 🎶\nAquí está el link para escuchar: {canción['clip']}\n¿Cuál es el título de la canción?"
    await ctx.send(pregunta)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        respuesta = await bot.wait_for('message', check=check, timeout=30.0)
        if respuesta.content.lower() == canción["titulo"].lower():
            await ctx.send("¡Correcto! 🎉")
        else:
            await ctx.send(f"¡Incorrecto! La respuesta correcta era: {canción['titulo']}")
    except asyncio.TimeoutError:
        await ctx.send("¡Se acabó el tiempo! La respuesta correcta era: {canción['titulo']}")

# Comando para obtener un Pokémon
@bot.command()
async def pokemon(ctx):
    pokemon = random.choice(pokemones)
    await ctx.send(f"Tu Pokémon es {pokemon['nombre']}:\nTipo: {pokemon['tipo']}\nAtaque: {pokemon['ataque']}\nDefensa: {pokemon['defensa']}\nVelocidad: {pokemon['velocidad']}")


# Diccionario para guardar puntuaciones de usuarios
puntuaciones = {}

translator = googletrans.Translator()

@bot.command(name="trivia", help="¡Juega una trivia con preguntas generales!")
async def trivia(ctx):
    # Lista de categorías en español
    categorias = {
        "1": "Conocimiento general",
        "2": "Entretenimiento: libros",
        "3": "Entretenimiento: película",
        "4": "Entretenimiento: música",
        "5": "Entretenimiento: musicales y teatros",
        "6": "Entretenimiento: televisión",
        "7": "Entretenimiento: videojuegos",
        "8": "Entretenimiento: juegos de mesa",
        "9": "Ciencia y naturaleza",
        "10": "Ciencia: computadoras",
        "11": "Ciencia: matemáticas",
        "12": "Mitología",
        "13": "Deportes",
        "14": "Geografía",
        "15": "Historia",
        "16": "Política",
        "17": "Arte",
        "18": "Celebridades",
        "19": "Animales",
        "20": "Vehículos",
        "21": "Entretenimiento: cómics",
        "22": "Ciencia: gadgets",
        "23": "Entretenimiento: anime y manga japonés",
        "24": "Entretenimiento: dibujos animados y animaciones"
    }

    # Diccionario de categorías en inglés para las solicitudes a la API
    categorias_en_ingles = {
        "1": 9,  # General Knowledge
        "2": 10, # Books
        "3": 11, # Film
        "4": 12, # Music
        "5": 13, # Musicals & Theatres
        "6": 14, # Television
        "7": 15, # Video Games
        "8": 16, # Board Games
        "9": 17, # Science & Nature
        "10": 18, # Computers
        "11": 19, # Gadgets
        "12": 20, # Mythology
        "13": 21, # Sports
        "14": 22, # Geography
        "15": 23, # History
        "16": 24, # Politics
        "17": 25, # Art
        "18": 26, # Celebrities
        "19": 27, # Animals
        "20": 28, # Vehicles
        "21": 29, # Comics
        "22": 30, # Science: Gadgets
        "23": 31, # Anime & Manga
        "24": 32  # Cartoons & Animations
    }

    categorias_texto = "\n".join([f"{i}. {cat}" for i, cat in categorias.items()])
    
    # Enviar mensaje con la lista de categorías
    await ctx.send(f"🎮 **¡Bienvenido a la trivia!**\nSelecciona una categoría respondiendo con el número:\n{categorias_texto}")
    
    # Validar categoría seleccionada
    def check_categoria(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content in categorias

    try:
        respuesta_categoria = await bot.wait_for("message", check=check_categoria, timeout=15)
        categoria_id = categorias_en_ingles[respuesta_categoria.content]
    except asyncio.TimeoutError:
        await ctx.send("⏰ **Tiempo agotado para seleccionar una categoría. Inténtalo de nuevo.**")
        return

    # Obtener pregunta
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://opentdb.com/api.php?amount=1&category={categoria_id}&type=multiple") as response:
            if response.status == 200:
                data = await response.json()
                if not data['results']:
                    await ctx.send("❌ **No se encontraron preguntas en esta categoría. Intenta otra.**")
                    return
                pregunta_data = data['results'][0]
                
                # Traducir pregunta y respuestas de forma secuencial
                pregunta = translator.translate(pregunta_data['question'], src="en", dest="es")
                respuestas = [
                    translator.translate(resp, src="en", dest="es").text for resp in pregunta_data['incorrect_answers']
                ]
                correcta = translator.translate(pregunta_data['correct_answer'], src="en", dest="es").text
                
                respuestas.append(correcta)
                random.shuffle(respuestas)

                # Opciones de respuesta
                opciones_mapeadas = {chr(97 + i): respuestas[i] for i in range(len(respuestas))}
                opciones_texto = "\n".join([f"{letra}) {opcion}" for letra, opcion in opciones_mapeadas.items()])
                await ctx.send(f"📚 **Categoría seleccionada**\n🧠 {pregunta.text}\n{opciones_texto}\n\nResponde con la letra de tu elección (a, b, c, ...):")
            else:
                await ctx.send("❌ **Error al obtener una pregunta. Inténtalo más tarde.**")
                return

    # Validar respuesta del usuario
    def check_respuesta(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in opciones_mapeadas.keys()

    try:
        respuesta_usuario = await bot.wait_for("message", check=check_respuesta, timeout=15)
        respuesta_elegida = opciones_mapeadas[respuesta_usuario.content.lower()]
        if respuesta_elegida == correcta:
            await ctx.send(f"🎉 **¡Correcto, {ctx.author.name}!** La respuesta era: **{correcta}**.")
        else:
            await ctx.send(f"❌ **Incorrecto, {ctx.author.name}.** La respuesta correcta era: **{correcta}**.")
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ **Tiempo agotado, {ctx.author.name}.** Sé más rápido la próxima vez.")




@bot.tree.command(name="batalladedados", description="Desafía a otro usuario a una batalla de dados.")
@app_commands.describe(oponente="El usuario al que desafiarás")
async def batalla_dados(interaction: discord.Interaction, oponente: discord.Member):
    if oponente == interaction.user:
        await interaction.response.send_message("¡No puedes desafiarte a ti mismo!", ephemeral=True)
        return

    dado_tuyo = random.randint(1, 6)
    dado_oponente = random.randint(1, 6)
    resultado = f"🎲 **{interaction.user.display_name}** tiró un {dado_tuyo}.\n🎲 **{oponente.display_name}** tiró un {dado_oponente}.\n"

    if dado_tuyo > dado_oponente:
        resultado += f"¡**{interaction.user.display_name}** gana! 🎉"
    elif dado_tuyo < dado_oponente:
        resultado += f"¡**{oponente.display_name}** gana! 🎉"
    else:
        resultado += "¡Es un empate! 🤝"

    await interaction.response.send_message(resultado)



@bot.event
async def on_guild_join(guild):
    """
    Este evento se ejecuta cuando el bot se une a un nuevo servidor.
    Intenta enviar el mensaje "llegó el prime" en el primer canal donde tiene permisos para escribir.
    """
    message = "Llegó el prime"
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            try:
                await channel.send(message)
                print(f"Mensaje enviado en el servidor '{guild.name}' (ID: {guild.id}) en el canal '{channel.name}'.")
                break
            except Exception as e:
                print(f"No se pudo enviar el mensaje en el canal '{channel.name}' del servidor '{guild.name}'. Error: {e}")





def send_command_via_rcon(command):
    """Envía un comando al servidor de Minecraft a través de RCON."""
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            print(f"Conexión al RCON establecida. Enviando comando: {command}")
            response = mcr.command(command)
            print(f"Respuesta del servidor: {response}")
            return response
    except Exception as e:
        print(f"Error al enviar comando vía RCON: {e}")
        return None


async def has_whitelist_permission(user: discord.Member):
    role = discord.utils.get(user.roles, name="subs")
    permission_role = discord.utils.get(user.roles, name="PermisoWhitelist")
    return role is not None or permission_role is not None or user.id == ADMIN_USER_ID


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == WHITELIST_CHANNEL_ID:
        if not await has_whitelist_permission(message.author):
            await message.reply("No tienes permisos para usar el comando /whitelist.")
            return

        username = message.content.strip()
        if not username.replace('_', '').isalnum() or len(username) > 16:
            await message.reply("Por favor, proporciona un nombre de usuario de Minecraft válido (solo letras, números y guiones bajos, máx. 16 caracteres).")
            return

        try:
            response = send_command_via_rcon(f"whitelist add {username}")
            if response and "added to the whitelist" in response:
                await message.reply(f"¡{username} se ha agregado correctamente a la whitelist! 🎉")
            else:
                await message.reply(f"¡{username} se ha agregado correctamente a la whitelist! 🎉")
        except Exception as e:
            print(f"Error al procesar el mensaje: {e}")
            await message.reply("Ocurrió un error al procesar tu solicitud.")
    await bot.process_commands(message)


@bot.tree.command(name="darpermisowhitelist", description="Otorga permisos a un usuario para usar el comando /whitelist.")
@app_commands.describe(user="El usuario al que se le otorgarán permisos para la whitelist")
async def dar_permisos_whitelist(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != ADMIN_USER_ID:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return

    role = discord.utils.get(interaction.guild.roles, name="PermisoWhitelist")
    if role is None:
        role = await interaction.guild.create_role(name="PermisoWhitelist", reason="Rol que da el permiso para usar /whitelist")

    await user.add_roles(role, reason="Se le ha otorgado permiso para ejecutar el comando /whitelist")
    await interaction.response.send_message(f"{user.mention} ahora tiene permiso para usar el comando /whitelist.", ephemeral=True)


@bot.tree.command(name="quitarpermiso", description="Quita el permiso para usar comandos especiales.")
@app_commands.describe(user="El usuario al que se le quitarán los permisos.")
async def quitar_permiso(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != ADMIN_USER_ID:
        await interaction.response.send_message("No tienes permisos para usar este comando.", ephemeral=True)
        return

    role = discord.utils.get(interaction.guild.roles, name="PermisoWhitelist")
    if role in user.roles:
        await user.remove_roles(role, reason="Permiso retirado por el administrador")
        await interaction.response.send_message(f"{user.mention} ya no tiene permisos para usar comandos especiales.", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user.mention} no tiene permisos asignados que puedan retirarse.", ephemeral=True)


async def check_instagram_new_reel():
    """Verifica si hay un nuevo reel en Instagram."""
    try:
        response = requests.get(INSTAGRAM_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        for script in scripts:
            data = json.loads(script.string)
            if '@type' in data and data['@type'] == 'VideoObject':
                print(f"Nuevo reel encontrado: {data['url']}")
                return data['url']
    except Exception as e:
        print(f"Error al verificar reels: {e}")
    return None


@bot.tree.command(name="serverfeliz", description="Mutea a un usuario por un tiempo específico.")
@app_commands.describe(user="El usuario que será muteado", duration="Duración del muteo en minutos")
async def serverfeliz(interaction: discord.Interaction, user: discord.Member, duration: int):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muteado")
    if muted_role is None:
        muted_role = await interaction.guild.create_role(name="Muteado", reason="Rol para mutear usuarios")
        for channel in interaction.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await user.add_roles(muted_role, reason=f"Muteado por {duration} minutos")
    await interaction.response.send_message(f"{user.mention} ha sido muteado por {duration} minutos.", ephemeral=True)

    await asyncio.sleep(duration * 60)
    await user.remove_roles(muted_role, reason="Fin del tiempo de muteo")



