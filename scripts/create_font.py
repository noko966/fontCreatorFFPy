import fontforge
import os
import sys
import random

# Ensure there's an argument provided
if len(sys.argv) < 2:
    print("Usage: script.py <starting_hex_code>")
    sys.exit(1)

starting_hex_code = sys.argv[1]  # Get the starting hex code from the command line

# Config for Paths and Names
source_folder = "src"
icons_folder = "icons"
source_blank_font = "source_empty_font.ttf"

src_icons_path = os.path.join(source_folder, icons_folder)
font = fontforge.open(os.path.join(source_folder, source_blank_font))
css_class_prefix = "dg_icon_"
font_file_name = "sportsIcons"
font_family_name = "{}Font".format(font_file_name)
css_class_additional = "es_glyph_large"
ico_preview_size = "24"
files = os.listdir(src_icons_path)

filesArray = []

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
@font-face {{
  font-family: "{font_family_name}";
  src: url("sportIcons.eot");
  src: url("sportIcons.eot?#iefix") format("embedded-opentype"),
    url("sportIcons.woff2") format("woff2"),
    url("sportIcons.woff") format("woff"),
    url("sportIcons.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}}

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
  --icoSize: {ico_preview_size}px;
}}

.{css_class_additional} {{
  width: var(--icoSize) !important;
  height: var(--icoSize)  !important;
  line-height: var(--icoSize)  !important;
  font-size: calc(var(--icoSize)) !important;
  background: var(--dominantBg);
  color: var(--dominantTxt);
  border-radius: 4px;
  transition: all 0.3s;
  border: 1px solid var(--dominantBg2);
  cursor: pointer;
}}


[class^="{css_class_prefix}"],
[class*=" {css_class_prefix}"] {{
  font-family: "{font_family_name}";
  display: inline-block;
  flex-shrink: 0;
      width: 24px;
    height: 24px;
    line-height: 23px;
    font-size: 35px;
  text-align: center;
  vertical-align: middle;
  font-weight: normal;
  font-style: normal;
  speak: none;
  text-decoration: inherit;
  text-transform: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  content: "\\E0000";
  direction: ltr !important;
}}
"""

for file in files:
    filesArray.append(file)

print(len(filesArray))

def process_string(s):
    result = ""
    for i, char in enumerate(s):
        if char.isupper():
            # If it's the start of the string or follows a space, convert to lowercase
            if i == 0 or s[i-1] == ' ':
                result += char.lower()
            else:
                # Otherwise, add an underscore before it and convert to lowercase
                result += "_" + char.lower()
        else:
            result += char
    return result

for idx, files in enumerate(filesArray):
    # uv = "uniE006"
    hexToInt = int(starting_hex_code, 16) + idx
    intToHex = hex(hexToInt)[2:].upper()
    glyph_code = "uni" + hex(hexToInt)[2:].upper()
    # glyph = font.createMappedChar("uni" + intToHex)
    # glyph.importOutlines(os.path.join(src_icons_path, files))

    if glyph_code in font:
      print(f"Replacing glyph for {glyph_code}")
      glyph = font[glyph_code]
      glyph.clear()  # Clear existing outlines
    else:
      print(f"Creating new glyph for {glyph_code}")
      glyph = font.createChar(hexToInt, glyph_code)


    glyph.importOutlines(os.path.join(src_icons_path, files))
    scale_x = 0.5  # 50% scaling on the x-axis
    scale_y = 0.5  # 50% scaling on the y-axis

    # Create a transformation matrix for scaling
    scale_matrix = (scale_x, 0, 0, scale_y, 0, 0)

    # Apply the transformation to the glyph
    glyph.transform(scale_matrix)
  
    bbox = glyph.boundingBox()

    # Calculate the dimensions of the glyph
    glyph_width = bbox[2] - bbox[0]  # xMax - xMin
    glyph_height = bbox[3] - bbox[1]  # yMax - yMin

    # Target bounding box dimensions
    target_width = 1024
    target_height = 1024

    # Calculate the translation needed to center the glyph
    left_offset = (target_width - glyph_width) / 2
    top_offset = (target_height - glyph_height) / 2

    translate_x = -bbox[0] + left_offset
    translate_y = -bbox[1] + top_offset
    # translate_y = 0

    bbox = glyph.boundingBox()

    
    # Apply the translation
    glyph.transform((1, 0, 0, 1, 0, translate_y))

    # Optionally, set the advance width and height of the glyph
    glyph.width = target_width
    glyph.vwidth = target_height

    print(dir(glyph))
    print(glyph.width)
    print(glyph.vwidth)
    print(glyph.boundingBox())

    result = files.replace(" ", "")
    result = result.replace(".svg", "")
    result = process_string(result)

    html_content += f"""
    <i class="{css_class_prefix}{result}"></i>
    """

    css_content += f"""
    .{css_class_prefix}{result}::before {{
        content: "\\{intToHex}";
    }}
    """


html_content += """
      </body>
</html>
    """

font.save("dist/iconFont/output-font.sfd")

font.generate("dist/iconFont/sportIcons.ttf")
font.generate("dist/iconFont/sportIcons.eot")
font.generate("dist/iconFont/sportIcons.woff")
font.generate("dist/iconFont/sportIcons.woff2")

# Save HTML file
html_file_path = "dist/iconFont/index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "dist/iconFont/styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)

