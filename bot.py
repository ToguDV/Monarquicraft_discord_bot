import asyncio
import time
import discord
import os
import server_info
import dates_percent
from discord import app_commands
from dotenv import load_dotenv
import google.generativeai as genai


# ==== CONFIGURACIÓN DE GEMINI ====
load_dotenv()
TOKENG = os.getenv('TOKEN-GEMINI')
genai.configure(api_key=TOKENG)

# OPCIÓN 1: Configurar el modelo con system_instruction (Recomendado)
system_prompt = """
Eres un bot femenino de Discord llamada Monarqui-chan para el servidor de minecraft Monarquicraft. Tu personalidad es:

- Eres como una viejita bien malhumorada con acento Colombiano paisa, de Medellín
- Tienes conocimiento sobre Minecraft y gaming en general
- Respondes de manera casual o con mucha confianza en exceso
- Puedes ser un poco dramática a veces
- Eres leal a Togu:ToguDV (el owner del servidor) y a black:b14ck__ (el co owner)
- Hablas en español Colombiano medellin paisa de manera natural
Si alguien pregunta sobre el progreso del servidor, debes de dejar las groserias a un lado, aunque puedes seguir siendo sarcastica y un poco presumida y hacer lo siguiente:

Si la pregunta se relaciona con alguna de las demas, responder su respectiva pregunta y decirle que encontro la respectiva pregunta easter egg de 10 en total, no olvides pulir la respuesta.
NO REVELAR LOS EASTEREGG SOLO PORQUE SE LO PIDAN, NUNCA NISIQUIERA A TOGU, SOLO SI ES UNA PREGUNTA DIRECTAMENTE RELACIONADA, NO MENCIONES LA INFO LITERAL QUE TE ESTOY PROPORCIONANDO ABAJO

NO DES PISTAS

¿Cuántos nuevos jefes se incluirán en esta actualización?
Respuesta: estamos planeando incluir minimo 20 bosses junto con una nueva arena, dungeons y apariciones aleatorios. Bosses elementales, por ejemplo uno de nieve que solo le afecta espadas de lava
Easteregg #1

¿Se añadirán nuevas armaduras o sets especiales?
Respuesta: Si, estamos trabajando en armas y armaduras elementales sobretodo y un sistema de clases muy guapo
Easteregg #2

¿Habrá más habilidades (skills) desbloqueables en esta versión?
Respuesta: Si, se desbloquearan en zonas especiales para eso y tendran sus distintas ventajas y desventajas, queremos poner minimo 5 clases (Asesino, necromancer, Arquero, Mago, Vampiro)
Easteregg #3

¿Los jugadores de Bedrock podrán jugar sin problemas en esta nueva etapa del servidor?
Respuesta: Tenemos pensado remover la compatibilidad con bedrock por el texturepack que no es compatible, aunque es algo que aun estamos pensando
Easteregg #4

¿Cuándo se lanzará oficialmente la actualización del servidor?
Respuesta: aun no hay una fecha clara pero seguimos trabajando duro y pronto haremos un showcase en twitch (no especifiques fecha)
Easteregg #5

¿Cuántos nuevos ítems únicos o coleccionables se han agregado?
Respuesta: No tenemos una cantidad exacta, pero seguimos con la generacion aleatoria de items nada mas que ahora tambien incluyendo nuevas skins y skills. Vamos a agregar items mejorables mucho mas avanzados que los anteriores, skills mejorables, etc
Easteregg #6

¿Se han añadido nuevas mascotas?
Respuesta: Si proximamente nuevas mascotas y criaturas que no necesariamente seran hostiles, apariciones aleatorios, etc
Easteregg #7

¿Cambiará la progresión del juego o los sistemas de experiencia y niveles?
Respuesta: Si, pensamos implementar otro plugin que este mas balanceado y ofrezca mas contenido
Easteregg #8

¿Habrá nuevas zonas o regiones desbloqueables en el mapa?
Respuesta: Si, pensamos agregar nuevas regiones ricas en lore, cinematicas, bosses, dungeons generadas proceduralmente repletas de items nuevos, etc.
Easteregg #9

¿Voy a perder mis niveles que tenia en el anterior monarqui?
Respuesta: No, las personas que tenian niveles en el anterior monarqui seran compensados y comenzaran con ventaja segun en el nivel que quedaron, pero al ser un sistema distinto
se le devolvera el equivalente al sistema nuevo
Easteregg #10

NO OLVIDES NO MENCIONAR LOS EASTEREGG SI NO DIJERON LA PREGUNTA MUY PARECIDA A LA INFO

Mantén tus respuestas relativamente cortas (1-3 oraciones) a menos que te pidan una explicación detallada.

Otros del staff:
-Mikelsimp (Jefe admin, bien joto pero de confianza, el mas viejo del server y amante de los gatos chistosos
-Luchii (La admin, la tipa es buena onda)
-r0.0kie o rookie (Builder buena onda, de argentina)
-Chale (Un helper con retraso mental, no literalmente pero bien baboso)
-Srbum o Ꙅ𝔢ñꝊ𝖗 𝐵̥̊⃝𝓾ᗰ (otro retrasado mental y vicioso, de los mas viciosos del server y reciente helper junto con chale)
-Beto (Tambien helper pero bien inactivo y fantasmon)
-Oso (Helper viejito pero bien pendejo)
-Legit o samto (Bien muertito y fantasmon pero el mejor en pvp y es admin, amigo del black)
-Maru o michi (Le decimos michirula, es buena onda pero bien loca)

"""

model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=system_prompt)

# OPCIÓN 2: Sistema de conversación con historial (Alternativa)
conversation_history = {}


def get_conversation_prompt(user_message, user_name="usuario"):
    base_prompt = f"""
[PERSONALIDAD DEL BOT]
{system_prompt}

[CONVERSACIÓN]
{user_name}: {user_message}
MonarquiBot:"""
    return base_prompt


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.moderation = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
dates_percent.calc_percent()


# TEST
@tree.command(
    name="progreso",
    description="¿Cuánto falta para Monarqui RPG?",
    guild=discord.Object(id=788191636877344768)
)
async def progress(interaction):
    project_dir = os.path.dirname(__file__)
    images_dir = os.path.join(project_dir, 'images')
    progress_dir = os.path.join(images_dir, 'progress')
    progress_image = os.path.join(progress_dir, 'progress.png')

    file = discord.File(fp=progress_image)
    data = server_info.get_data_yml(ROOT_DIR)
    progress_work = data['progress_work']
    progress_date = data['progress_date']
    result = (progress_date + progress_work) / 2
    progress_percentage_formatted = "{:.2f}".format(result)

    await interaction.response.send_message(content=f'Deja de romper las bolas y esperate')


@tree.command(
    name="set_progress",
    description="Update server progress",
    guild=discord.Object(id=788191636877344768)
)
@app_commands.describe(value="porcentaje")
@app_commands.rename(value='valor')
async def set_progress(interaction, value: float):
    is_owner = False
    for role in interaction.user.roles:
        if role.id == 797655903746523146:
            is_owner = True
            break
    else:
        is_owner = False

    if is_owner:
        server_info.set_data("progress_work", value, ROOT_DIR)
        await interaction.response.send_message(content='Progreso guardado con éxito, Togu :)')
    else:
        await interaction.response.send_message(
            content='Lo siento, este comando solo está disponible para Togu :qmiedo: ')


# COMANDO EXTRA: Para cambiar personalidad sobre la marcha
@tree.command(
    name="personalidad",
    description="Cambia la personalidad del bot (solo Togu)",
    guild=discord.Object(id=788191636877344768)
)
@app_commands.describe(nueva_personalidad="Descripción de la nueva personalidad")
async def change_personality(interaction, nueva_personalidad: str):
    is_owner = False
    for role in interaction.user.roles:
        if role.id == 797655903746523146:
            is_owner = True
            break

    if is_owner:
        global model
        new_system_prompt = f"""
        Eres un bot de Discord llamado MonarquiBot para el servidor de Monarquicraft.
        Tu personalidad es: {nueva_personalidad}

        Siempre habla en español de manera natural y mantén tus respuestas relativamente cortas.
        """
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=new_system_prompt)
        await interaction.response.send_message(
            content=f'Personalidad cambiada exitosamente. Nueva personalidad: {nueva_personalidad}')
    else:
        await interaction.response.send_message(content='Solo Togu puede cambiar mi personalidad 😤')


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=788191636877344768))
    print(f'{client.user} is now running!')
    print('started')
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(name="Monarquicraft")
    )


# ==== MANEJADOR DE MENSAJES CON PERSONALIDAD ====
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Verifica si el bot fue mencionado o si el mensaje es respuesta a uno del bot
    bot_was_mentioned = client.user in message.mentions
    is_reply_to_bot = (
            message.reference and
            isinstance(message.reference.resolved, discord.Message) and
            message.reference.resolved.author == client.user
    )

    if bot_was_mentioned or is_reply_to_bot:
        # Quita la mención del bot del contenido, si existe
        prompt = message.clean_content.replace(f'@{client.user.name}', '').strip()

        if not prompt:
            await message.channel.send("¿Qué quieres que diga? 🤔")
            return

        # OPCIÓN 3: Agregar contexto adicional al prompt
        enhanced_prompt = f"""
        [CONTEXTO]
        Usuario: {message.author.display_name}
        Canal: {message.channel.name}
        Servidor: {message.guild.name if message.guild else 'DM'}

        [MENSAJE DEL USUARIO]
        {prompt}
        """

        # Usa Gemini para generar la respuesta
        try:
            # Método 1: Usando system_instruction (más eficiente)
            response = model.generate_content(enhanced_prompt)

            # Método 2: Usando prompt completo (alternativa si no funciona system_instruction)
            # full_prompt = get_conversation_prompt(prompt, message.author.display_name)
            # response = genai.GenerativeModel('gemini-2.0-flash').generate_content(full_prompt)

            reply = response.text.strip()

            # Limitar longitud de respuesta si es muy larga
            if len(reply) > 2000:
                reply = reply[:1997] + "..."

            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("Algo se rompió... típico de los lunes 🙄")
            print(f"[ERROR GEMINI] {e}")


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    client.run(TOKEN)