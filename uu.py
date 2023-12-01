import fontforge
import os
import re

# Config for Paths and Names
source_folder = "src"
icons_folder = "icons"
source_blank_font = "source_empty_font.ttf"

src_icons_path = os.path.join(source_folder, icons_folder)
font = fontforge.open(os.path.join(source_folder, source_blank_font))
css_class_prefix = "es_glyph_"
font_file_name = "eSportsIcons"
font_family_name = "{}Font".format(font_file_name)

files = os.listdir(src_icons_path)

filesArray = []

html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="styles.css" />
    <style>
  .icons_container {
        display: flex;
      flex-direction: row;
      gap: 8px;
      flex-wrap: wrap;
  }
  </style>
  </head>
  <body>
    <div class="icons_container">
  
"""

# Generate CSS content
css_content = f"""
@font-face {{
  font-family: "{font_family_name}";
  src: url("esportIcons.eot");
  src: url("esportIcons.eot?#iefix") format("embedded-opentype"),
    url("esportIcons.woff2") format("woff2"),
    url("esportIcons.woff") format("woff"),
    url("esportIcons.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}}

.ico_font-L {{
  width: 36px !important;
  height: 36px !important;
  line-height: 36px !important;
  font-size: 36px !important;
}}

[class^="{css_class_prefix}"],
[class*=" {css_class_prefix}"] {{
  font-family: "{font_family_name}";
  display: inline-block;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  line-height: 24px;
  font-size: 24px;
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

for idx, files in enumerate(filesArray):
    uv = "uniE006"
    hexToInt = int("E000", 16) + idx
    intToHex = hex(hexToInt)[2:].upper()
    # print(hexToInt, intToHex)
    glyph = font.createMappedChar("uni" + intToHex)
    glyph.importOutlines(os.path.join(src_icons_path, files))

    result = files.replace(" ", "")
    result = result.replace(".svg", "")
    result = result.replace("a__", "")

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

# font.save("dist/output-font.sfd")

font.generate("dist/esportIcons.ttf")
font.generate("dist/esportIcons.eot")
font.generate("dist/esportIcons.woff")
font.generate("dist/esportIcons.woff2")

# Save HTML file
html_file_path = "dist/index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "dist/styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)
