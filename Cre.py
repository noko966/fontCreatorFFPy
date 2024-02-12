import subprocess

# Define the commands
download_command = ["python", "download_file.py"]
fontforge_command = ["ffpython", "create_font.py", "E003"]

# Run the download script
subprocess.run(download_command)

# Then run the FontForge script
subprocess.run(fontforge_command)