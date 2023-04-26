import os
import subprocess
import glob
from pathlib import Path
from pick import pick
from rich import print, box
from rich.panel import Panel
from rich.table import Table
import time


def main():
    desktop_path = os.path.join(Path.home(), r'OneDrive\Desktop')
    # workspace_files = glob.glob(f"{desktop_path}/**/*.code-workspace", recursive=True)
    workspace_files = glob.glob(f"{desktop_path}/**/*.code-workspace", recursive=False)
    workspace_files += glob.glob(f"{desktop_path}/*.code-workspace", recursive=False)

    # Sort workspaces by timestamp (last modified time) in descending order
    workspace_files = sorted(workspace_files, key=os.path.getmtime, reverse=True)

    workspaces = {Path(workspace).stem: workspace for workspace in workspace_files}

    if not workspaces:
        print("[bold red]No workspaces found on your Desktop.[/bold red]")
        return

    workspace_names = ['None'] + list(workspaces.keys())
    selected_workspace, _ = pick(workspace_names, "Select a workspace:")

    if selected_workspace == 'None':
        print("[bold yellow]Exiting without opening a workspace.[/bold yellow]")
        return None

    workspace_path = workspaces[selected_workspace]
    print(f"[bold green]Opening {selected_workspace}...[/bold green]")
    open_workspace(workspace_path)


def open_workspace(path):
    if os.name == 'nt':  # For Windows
        cmd = r"C:\Users\acer\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"
    else:  # For macOS and Linux
        cmd = 'code-insiders' if os.path.exists('/usr/local/bin/code-insiders') else 'code'

    subprocess.run([cmd, path], check=True)

def render_title(title):
    title_table = Table(box=box.SQUARE)
    title_table.add_column()
    title_table.add_row(f"[bold blue]{title}[/bold blue]")
    print(Panel.fit(title_table))

if __name__ == "__main__":
    # render_title("Visual Studio Code Workspace Selector")
    start_time = time.time()
    main()
    print("Time taken: {:.2f} seconds".format(time.time() - start_time))

