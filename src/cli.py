import sys
from rich import print
from rich.console import Console
console = Console()

#commands
from src.commands.create_project import create_project
from src.commands.delete_project import delete_project
from src.commands.list_projects import list_projects
from src.commands.run_project import run_project
from src.commands.build_project import build_project

#utils
from src.utils.show_error import show_error

def display_help(command):
  console.print(f"\033[92m[\033[0m\033[94m{command}\033[0m\033[92m]: \033[0m\033[93mEsta es la ayuda para el comando {command}\033[0m")
  console.print("\033[0m")

def display_help_command():
  console.print(f"\033[96m----------------------------------------\033[0m")
  console.print(f"\033[96m|                  Ayuda                 |\033[0m")
  console.print(f"\033[96m----------------------------------------\033[0m")
  console.print(f"Usos:")
  display_help("create")
  display_help("delete")
  display_help("list")
  display_help("run")

def deploy_command(argv):
  try:
    command = argv[1]
    argument = argv[2]

    if command in ["help", "-h"]:
      display_help_command()
        
    elif command == "create" and isinstance(argument, str):
      create_project(argument)
      console.print(f"\033[92mProyecto creado con éxito!\033[0m")
        
    elif command == "delete" and isinstance(argument, str):
      delete_project(argument)
      console.print(f"\033[92mProyecto eliminado con éxito!\033[0m")
      
    elif command == "list":
      list_projects()
      console.print(f"\033[92mLista de proyectos actualizada.\033[0m")
      
    elif command == "run" and isinstance(argument, str):
      run_project(argument)
      console.print(f"\033[92mProyecto ejecutado con éxito!\033[0m")
      
    elif command == "build":
      build_project()
      console.print(f"\033[92mProyecto construido con éxito!\033[0m")
    
    else:
        if len(argv) > 3 and argv[3] in ["-h", "--help"]:
          display_help(command)
          return
        show_error()
        print(f"\033[91mQuizás quisiste decir: dcp {command} -h\033[0m")

  except Exception as e:
    console.print(f"\033[91mError crítico en deploy, no te preocupes: {e}\033[0m")
    console.print(f"\033[96m------------------------------------------------\033[0m")

def main():
    deploy_command(sys.argv)

if __name__ == "__main__":
    main()
