import os
from rich.console import Console

console = Console()

def bot():
  try:
     # Crear directorios principales y archivos
        os.makedirs(project_directory)
        print(f"Proyecto '{project_name}' creado en {project_directory}")

        # Estructura de directorios y archivos
        directories = [
            'commands',
            'utils',
            'functions',
            'buttons',
            'logs',
            'config',
            'assets',
            'monitor',
        ]
        
        files = [
            # Assets
            ('assets', '__init__.py', ''),
            
            # Monitor
            ('monitor', '__init__.py', ''),
            ('monitor', 'index.html', """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Monitor de Logs</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <h1>Monitor (ALPHA)</h1>

    <!-- Filters -->
    <div class="filters">
      <input
        type="text"
        id="filterGuild"
        placeholder="Filter by server name"
      />
      <input
        type="text"
        id="filterGuildId"
        placeholder="Filter by Server ID"
      />
      <input
        type="text"
        id="filterUser"
        placeholder="Filter by user name"
      />
      <input type="date" id="filterDate" placeholder="Filter by date" />
      <button onclick="applyFilters()">Apply Filters</button>
      <button onclick="resetFilters()">Reset Filters</button>
    </div>

    <!-- Logs -->
    <table id="logsTable">
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>User</th>
          <th>Server</th>
          <th>ID - Server</th>
          <th>Channel</th>
          <th>ID - Channel</th>
          <th>Message</th>
        </tr>
      </thead>
      <tbody id="logsBody">
        <!-- Logs will be inserted here -->
      </tbody>
    </table>

    <script src="script.js"></script>
  </body>
</html>

"""),
            ('monitor', 'style.css', """
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  padding: 20px;
}

h1 {
  text-align: center;
}

.filters {
  margin-bottom: 20px;
  text-align: center;
}

.filters input,
.filters button {
  padding: 10px;
  margin: 5px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #4caf50;
  color: white;
}

tr:hover {
  background-color: #cae496;
  cursor: pointer;
}

"""),
            ('monitor', 'script.js', """
// Variables globales para los logs filtrados
let allLogs = []; // Guardar todos los logs cargados

// Función para cargar los logs del archivo y actualizar la tabla
async function loadLogs() {
  try {
    const response = await fetch("../logs/logs.txt"); // Ruta al archivo de logs
    const data = await response.text();

    // Actualiza todos los logs cargados
    allLogs = data.split("|").filter((log) => log.trim() !== "");

    // Aplicar los filtros iniciales
    applyFilters();
  } catch (error) {
    console.error("Error al cargar los logs:", error);
    console.log(error);
  }
}

// Función para aplicar filtros a los logs
function applyFilters() {
  const filterGuild = document
    .getElementById("filterGuild")
    .value.toLowerCase();
  const filterGuildId = document
    .getElementById("filterGuildId")
    .value.toLowerCase();
  const filterUser = document.getElementById("filterUser").value.toLowerCase();
  const filterDate = document.getElementById("filterDate").value;

  const filteredLogs = allLogs.filter((log) => {
    const [timestamp, userInfo, guild, guildData, channel, channelData, msg] =
      log.split(";").map((item) => item.trim());

    const logDate = timestamp.split(" ")[0]; // Asume que timestamp tiene el formato "YYYY-MM-DD HH:MM:SS"
    return (
      (!filterGuild || guild.toLowerCase().includes(filterGuild)) &&
      (!filterGuildId || guildData.toLowerCase().includes(filterGuildId)) &&
      (!filterUser || userInfo.toLowerCase().includes(filterUser)) &&
      (!filterDate || logDate === filterDate)
    );
  });

  updateTable(filteredLogs);
}

// Función para restablecer filtros
function resetFilters() {
  document.getElementById("filterGuild").value = "";
  document.getElementById("filterGuildId").value = "";
  document.getElementById("filterUser").value = "";
  document.getElementById("filterDate").value = "";
  applyFilters();
}

// Función para actualizar la tabla de logs
function updateTable(logs) {
  const logsBody = document.getElementById("logsBody");
  logsBody.innerHTML = ""; // Limpiar la tabla antes de actualizar

  logs.forEach((log) => {
    const [timestamp, userInfo, guild, guildData, channel, channelData, msg] =
      log.split(";").map((item) => item.trim());

    const row = document.createElement("tr");
    row.innerHTML = `
              <td>${timestamp}</td>
              <td>${userInfo}</td>
              <td>${guild}</td>
              <td>${guildData}</td>
              <td>${channel}</td>
              <td>${channelData}</td>
              <td>${msg}</td>
          `;
    logsBody.insertBefore(row, logsBody.firstChild); // Insertar en la parte superior de la tabla
  });
}

// Cargar los logs cada 5 segundos
setInterval(loadLogs, 5000);
loadLogs(); // Cargar los logs inicialmente

"""),
            ('monitor', 'monitor.py', """
# comming
"""),
            
            # Comandos
            ('commands', '__init__.py', ''),
            ('commands', 'ping.py', """
import discord
from discord.ext import commands
from buttons.buttons_help import ButtonsHelp

async def ping_layout(interaction, latency):
    try:
        embed = discord.Embed(title="🏓 Pong", description=f"{interaction.user.mention} {latency} ms / Pong!", color=0x00ff00)
        embed.set_image(url="https://cusoft.tech/wp-content/uploads/2024/07/image-24.jpg")  # -> images can be attached by external url
        embed.set_footer(text="💻 Polaris", icon_url="https://cusoft.tech/wp-content/uploads/2024/05/working.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True, view=ButtonsHelp()) # -> view=ButtonsHelp() to display the buttons
    except Exception as e:
        return e
"""),
            
            # Utils
            ('utils', '__init__.py', ''),
            ('utils', 'error_message.py', """

import discord
from buttons.buttons_help import ButtonsHelp
from datetime import datetime
from functions.print_logs import logguer

async def error_message(e, interaction, msg):
    try: 
        embed = discord.Embed(
            title="We had a problem ⚠️",
            description=f"An error occurred while executing the 😢 command. Don't worry, it's not your fault, we are working to fix the problem as soon as possible ⚒️."
        )
        
        embed.add_field(
            name=" ",
            value="●▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬●",
            inline=False)
        
        embed.add_field(
            name="Error description: ",
            value=f"{msg}",
            inline=False)
        
        embed.add_field(
            name=" ",
            value="●▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬●",
            inline=False)
        
        embed.set_image(
                url="https://nftplazas.com/wp-content/uploads/2024/06/lumittera-gameplay.png"
            )
        
        embed.color = 0x0fffff
        await interaction.response.send_message(embed=embed, ephemeral=True, view=ButtonsHelp())
        
        # Record the error in the log file
        await logguer(interaction, "logs.txt", f"Error: -> Command: {msg}")

    except Exception as e:
        print(f"Ocurrio un error al enviar el mensaje de error: {str(e)}")
        await logguer(interaction, "logs.txt", f"Error: -> Command: {msg}, Error: {str(e)}")

"""),
            
            # Funciones
            ('functions', '__init__.py', ''),
            ('functions', 'print_logs.py', """


from datetime import datetime

async def logguer(interaction, file_name, msg):
    log_file = f'logs/{file_name}'
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = interaction.user
            user_info = {
                "name": user.name,
                "discriminator": user.discriminator,
                "id": user.id,
                "user_roles": ", ".join([role.name for role in user.roles]) if interaction.guild else "No Roles"
            }
            guild = interaction.guild.name if interaction.guild else "Direct Message"
            guild_data = None
            if guild == "Direct Message":
                guild_data = None
            else:
                guild_data = {
                    "name": interaction.guild.name,
                    "id": interaction.guild.id
                }
            channel = interaction.channel.name if interaction.guild else "DM"
            channel_data = None
            if channel == "DM":
                channel_data = None
            else:
                channel_data = {
                    "name": interaction.channel.name,
                    "id": interaction.channel.id
                }
            
            
            log_entry = f''' time: {timestamp}; user: {user_info}; guild: {guild}; guild_data: {guild_data}; channel: {channel}; channel_data: {channel_data}; msg: {msg} |'''
            f.write(log_entry)

    except Exception as e:
        print(f"Error al registrar el comando en el log: {e}")

"""),
            ('functions', 'file_manager.py', """
# In the process of being updated 
# 
# 
# import os
# import discord
# 
# # Devuelve un objeto discord.File si el archivo existe, de lo contrario, devuelve None.
# def get_discord_file(filename):
#     
#     # Construye la ruta completa al archivo
#     file_path = os.path.join('assets', filename) # es modificable
# 
#     # Verifica si el archivo existe
#     if os.path.isfile(file_path):
#         # Crea y devuelve el objeto discord.File
#         try:
#             discord_file = discord.File(file_path, filename=filename)
#             return discord_file
#         except Exception as e:
#             # Si ocurre algún error, devuelve None
#             print(f"Error al crear el objeto discord.File en la función get_discord_file: {e}")
#             return None
#     else:
#         # Retorna None si el archivo no existe
#         return None

"""),
            
            # Botones
            ('buttons', '__init__.py', ''),
            ('buttons', 'buttons_help.py', """
import discord

website_url = "https://polarisweb3.org"

class ButtonsHelp(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(label="Oficial Web",
                              url=website_url,
                              style=discord.ButtonStyle.url))
      
"""),
            
            # Logs
            ('logs', '__init__.py', ''),
            ('logs', 'logs.txt', ''),
            
            # Config
            ('config', '__init__.py', ''),
            ('config', 'bot_config.py', """
# Configuración del bot

TOKEN = 'YOUR_TOKEN_HERE'
"""),
            
            # Gitignore
            ('', '.gitignore', """
config
config.py    
bot_config.py
"""),
            
            # requirements.txt
            ('', 'requirements.txt', """
discord.py
watchdog
asyncio
datetime
requests
rich
"""),
           
           
            # dev.py     
            ('', 'dev.py', """
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.progress import Progress
from rich import print
import subprocess
import time
import os
import threading
import hashlib
import sys

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command, root_path):
        self.command = command
        self.process = None
        self.console = Console()
        self.debounce_timer = None
        self.root_path = root_path
        self.last_hash = None

    def calculate_directory_hash(self):
        #Calcula un hash para todos los archivos `.py` en el proyecto.
        hasher = hashlib.md5()
        try:
            for subdir, _, files in os.walk(self.root_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(subdir, file)
                        with open(file_path, 'rb') as f:
                            buf = f.read()
                            hasher.update(buf)
            return hasher.hexdigest()
        except Exception as e:
            self.console.print(f"[bold red]Error calculating directory hash: {e}[/bold red]")
            return None

    def on_modified(self, event):
        # Se llama cuando se detecta un cambio en un archivo.
        # Solo monitorear archivos Python
        if event.is_directory or not event.src_path.endswith('.py'):
            return

        # Reiniciar el temporizador de debounce
        if self.debounce_timer:
            self.debounce_timer.cancel()

        # Usar debounce para reiniciar el proceso después de un corto periodo de inactividad
        self.debounce_timer = threading.Timer(1, self.restart_if_needed)
        self.debounce_timer.start()

    def restart_if_needed(self):
        # Reinicia el proceso si el hash del proyecto ha cambiado.
        current_hash = self.calculate_directory_hash()
        if current_hash != self.last_hash:
            self.last_hash = current_hash
            self.restart_process()

    def start_process(self):
        #Iniciar el proceso del bot.
        if not self.process or self.process.poll() is not None:
            self.console.print(f"[bold green]Running command:[/bold green] [italic yellow]{self.command}[/italic yellow]")
            with Progress() as progress:
                task = progress.add_task("[cyan]Starting process...", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.1)  # Simular carga

            try:
                # Ajustar para Windows y Unix
                if os.name == 'nt':  # Windows
                    self.process = subprocess.Popen(self.command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:  # Unix (Linux/macOS)
                    self.process = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)
                self.console.print("[bold green]Process started successfully![/bold green]")
            except Exception as e:
                self.console.print(f"[bold red]Error starting process: {e}[/bold red]")
        else:
            self.console.print("[bold yellow]Process is already running.[/bold yellow]")

    def stop_process(self):
        # Detener el proceso enviando `SIGINT` (Ctrl+C).
        if self.process:
            self.console.print("[bold red]Stopping the current process with Ctrl+C...[/bold red]")
            try:
                # Enviar SIGINT (Ctrl+C) al grupo de procesos
                if os.name == 'nt':  # Windows
                    self.process.send_signal(signal.CTRL_BREAK_EVENT)
                else:  # Unix (Linux/macOS)
                    os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
                self.process.wait()  # Esperar a que el proceso termine
                self.console.print("[bold red]Process stopped.[/bold red]")
            except Exception as e:
                self.console.print(f"[bold red]Error stopping process: {e}[/bold red]")

    def restart_process(self):
        # Reiniciar el proceso.
        self.stop_process()  # Detener el proceso de manera controlada
        self.start_process()  # Iniciar un nuevo proceso

    def stop(self):
        # Detener el proceso y cualquier temporizador.
        if self.debounce_timer:
            self.debounce_timer.cancel()
        if self.process:
            self.console.print("[bold red]Terminating process before exit...[/bold red]")
            self.stop_process()

if __name__ == "__main__":
    root_path = os.getcwd()  # Monitorear toda la carpeta raíz del proyecto
    command = "python bot.py"  # Comando para ejecutar el bot

    event_handler = ChangeHandler(command, root_path)

    # Inicializar hash del proyecto
    event_handler.last_hash = event_handler.calculate_directory_hash()

    # Iniciar el bot
    event_handler.start_process()

    observer = Observer()
    observer.schedule(event_handler, root_path, recursive=True)  # Monitorear recursivamente todo el directorio
    observer.start()

    console = Console()
    try:
        console.print(f"[bold green]Monitoring for changes in: {root_path}...[/bold green]")
        while True:
            time.sleep(1)  # Mantener el programa corriendo
    except KeyboardInterrupt:
        observer.stop()
        event_handler.stop()
        console.print("[bold red]Monitoring stopped by user.[/bold red]")

    observer.join()


"""),
           
            
            # bot.py
            ('', 'bot.py', """

# Import required modules
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from config.bot_config import TOKEN
from utils.error_message import error_message
from commands.ping import ping_layout
from functions.print_logs import logguer

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Bot startup event
@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f'{bot.user} has connected to Discord!')
    except Exception as e:
        print(e)
        

# Ping command
@bot.tree.command(name="ping", 
                  description="Ping the bot")
async def ping_command(interaction: discord.Interaction):
    try:
        await logguer(interaction, "logs.txt", f"Execution: -> Command: Ping")
        
        # after registration, send the response
        await ping_layout(interaction, round(bot.latency * 1000))
    except Exception as e:
        await error_message(e,
                            interaction,
                            f"Command ping [{e}]")

bot.run(TOKEN)

""")
        ]

        # Crear directorios
        for directory in directories:
            dir_path = os.path.join(project_directory, directory)
            os.makedirs(dir_path)
            print(f"Directorio '{dir_path}' creado.")

        # Crear archivos y añadir contenido
        for file_dir, file_name, content in files:
            file_path = os.path.join(project_directory, file_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)  # Añade contenido al archivo
            print(f"Archivo '{file_path}' creado con contenido.")

  except Exception as e:
    console.print("Error")