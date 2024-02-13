import subprocess

# Define the commands
download_command = ["python", "scripts/download_file.py"]
fontforge_command = ["ffpython", "scripts/create_font.py", "E078"]

# Run the download script
subprocess.run(download_command)

# Then run the FontForge script
subprocess.run(fontforge_command)