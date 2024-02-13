from PIL import Image
import os
import random
# Constants for the sprite dimensions and the spacing between sprites
SPRITE_WIDTH = 80  # Assuming each sprite is 16px wide
SPRITE_HEIGHT = 80  # Assuming each sprite is 24px tall
SPRITE_SPACING = 0  # Assuming 24px of spacing between each sprite
css_class_prefix = "imgSpr"
# Function to get the Y position for the sprite index
def get_sprite_y_position(index):
    return index * SPRITE_SPACING

# Function to update or append a sprite
def update_sprite(image_path, index, sprite_sheet):
    new_sprite = Image.open(image_path)
    if new_sprite.size != (SPRITE_WIDTH, SPRITE_HEIGHT):
        raise ValueError(f"New sprite size does not match. Expected {(SPRITE_WIDTH, SPRITE_HEIGHT)}, got {new_sprite.size}")
    y_position = get_sprite_y_position(index)
    sprite_sheet.paste(new_sprite, (0, y_position))
    return sprite_sheet

# Load the original sprite sheet
# Config for Paths and Names
source_folder = "src"
images_folder = "images"
sprite_sheet_path = 'sport_icons_start.png'

new_images_folder = os.path.join(source_folder, images_folder)
sprite_sheet = Image.open(os.path.join(source_folder, sprite_sheet_path))

new_images = sorted([
    (int(os.path.splitext(filename)[0]), os.path.join(new_images_folder, filename))
    for filename in os.listdir(new_images_folder)
    if filename.endswith('.png') and filename.replace('.png', '').isdigit()
], key=lambda x: x[0])

# Adjust get_sprite_y_position to correctly calculate the Y position based on index
def get_sprite_y_position(index):
    # Assuming each sprite's height is SPRITE_HEIGHT and there's SPRITE_SPACING between each sprite
    return index * (SPRITE_HEIGHT + SPRITE_SPACING)

# Calculate the required height for the sprite sheet after adding new sprites
# This part remains largely the same but uses the updated get_sprite_y_position for calculation
max_index = max(new_images[-1][0], sprite_sheet.height // (SPRITE_HEIGHT + SPRITE_SPACING) - 1)
required_height = get_sprite_y_position(max_index + 1) + SPRITE_HEIGHT  # Ensure there's room for the last sprite

# Create a new sprite sheet if necessary
if sprite_sheet.height < required_height:
    new_sprite_sheet = Image.new('RGBA', (SPRITE_WIDTH, required_height))
    new_sprite_sheet.paste(sprite_sheet, (0, 0))
else:
    new_sprite_sheet = sprite_sheet

# Update or append each new sprite
for index, image_path in new_images:
    new_sprite_sheet = update_sprite(image_path, index, new_sprite_sheet)

# Save the updated sprite sheet
new_sprite_sheet.save('dist/imageSprite/sportIcons.png')


html_content = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="styles.css?{random.randint(0, 100)}" />
    <style>
  .icons_container {{
          display: flex;
          flex-direction: row;
          justify-content: center;
          gap: calc(var(--icoSize) * 0.3);
          flex-wrap: wrap;
          padding-left: calc(var(--icoSize) * 0.5);
          padding-right: calc(var(--icoSize) * 0.5);
          background: var(--bodyBg);
          border: 1px solid var(--151A1E);
      }}

  html {{
  background: var(--bodyBg);
  color: var(--bodyTxt);
}}
  </style>
  </head>
  <body>
    <div class="icons_container">
  
"""


# Generate CSS content
css_content = f"""
:root{{
  --bodyBg: #121212;
  --bodyBg2: #151A1E;
  --bodyTxt: #ccc;
  --dominantBg: #0b293d;
  --dominantBg2: #14496d;
  --dominantTxt: #fefefe;
  --accentBg: #00b6ff;
  --accentBg2: #33454d;
  --accentTxt: rgba(0, 0, 0, 0.97);
}}


[class^="{css_class_prefix}"],
[class*=" {css_class_prefix}"] {{
  background-image: url(sportIcons.png);
  background-size: 100%;
  width: 24px;
  height: 24px;
}}
"""

# Generate and save the new CSS
css_filename = 'dist/imageSprite/sprite.css'
with open(css_filename, 'w') as css_file:
    for index in range(max_index + 1):
        y_position = -(index * 24)  # 24px step for each sprite index

        html_content += f"""
        <i class="{css_class_prefix}{index}"></i>
        """

        css_content += f"""
        .{css_class_prefix}{index} {{
            background-position: 0px {y_position}px;
        }}
        """

# Save HTML file
html_file_path = "dist/imageSprite/index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "dist/imageSprite/styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)


print("Sprite sheet updated and CSS generated.")