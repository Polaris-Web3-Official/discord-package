import os
from rich.console import Console

console = Console()
def create_project(project_name):
    try:
      console.log("project created")
    except Exception as e:
        print(f"Error al crear el proyecto: {e}")
