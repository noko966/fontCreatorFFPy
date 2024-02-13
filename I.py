import subprocess

# Define the commands
download_command = ["python", "scripts/download_sprite.py"]
sprite_command = ["python", "scripts/create_image.py"]

# Run the download script
subprocess.run(download_command)
subprocess.run(sprite_command)

# Then run the FontForge script
# subprocess.run(fontforge_command)