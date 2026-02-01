import discord
from discord.ext import commands
import os

# ================= Keep-alive сервер =================
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=3000)

Thread(target=run).start()
# =====================================================

# Токен берём из переменной окружения
TOKEN = os.environ['MTQ2NzU4MTY1MjA2NTg0OTQzNg.GqoQod.1EbLU0hAw04vCJyuzw2a_bk_Jt7jqHB1bKrVnk']

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ==================== Твои команды ===================
@bot.tree.command(name="track", description="Показать текущий трек станции")
async def current_track(interaction: discord.Interaction):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    state = player_state.get(guild_id)
    if not state:
        await interaction.followup.send("Сейчас ничего не играет.", ephemeral=True)
        return
    name = STATION_NAMES[state["station_idx"]]
    title = state.get("track")
    if not title and not state.get("paused", False):
        try:
            _, url = RADIO_STATIONS[state["station_idx"]]
            title = await fetch_icy_title(url)
            if title:
                state["track"] = title
                try:
                    await update_presence_for_guild(guild_id)
                except Exception:
                    pass
        except Exception:
            title = None
    if title:
        await interaction.followup.send(f"🎧 Трек: {title}** (станция: {name})", ephemeral=False)
    else:
        await interaction.followup.send(f"Текущий трек недоступен. Станция: {name}", ephemeral=True)

@bot.tree.command(name="history", description="Показать историю треков текущей станции")
async def track_history(interaction: discord.Interaction):
    await interaction.response.defer()
    guild_id = interaction.guild.id
    state = player_state.get(guild_id)
    if not state:
        await interaction.followup.send("Сейчас ничего не играет.", ephemeral=True)
        return
    station_name = STATION_NAMES[state["station_idx"]]
    history = state.get("history") or []
    if not history:
        await interaction.followup.send(f"История пуста для станции {station_name}.", ephemeral=True)
        return
    last_items = history[-10:]
    lines = [f"{idx+1}. {title}" for idx, title in enumerate(last_items)]
    msg = f"История треков для {station_name} (последние {len(last_items)}):\n" + "\n".join(lines)
    await interaction.followup.send(msg, ephemeral=False)
# =====================================================

bot.run('MTQ2NzU4MTY1MjA2NTg0OTQzNg.GqoQod.1EbLU0hAw04vCJyuzw2a_bk_Jt7jqHB1bKrVnk')
