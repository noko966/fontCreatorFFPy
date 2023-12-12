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
css_class_additional = "es_glyph_large"
ico_preview_size = "16"
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
          justify-content: center;
          gap: calc(var(--icoSize) * 0.3);
          flex-wrap: wrap;
          padding-left: calc(var(--icoSize) * 0.5);
          padding-right: calc(var(--icoSize) * 0.5);
          background: var(--bodyBg);
          border: 1px solid var(--151A1E);
      }

  html {
  background: var(--bodyBg);
  color: var(--bodyTxt);
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
  width: var(--icoSize);
  height: var(--icoSize);
  line-height: var(--icoSize);
  font-size: var(--icoSize);
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
    uv = "uniE006"
    hexToInt = int("E000", 16) + idx
    intToHex = hex(hexToInt)[2:].upper()
    # print(hexToInt, intToHex)
    glyph = font.createMappedChar("uni" + intToHex)
    glyph.importOutlines(os.path.join(src_icons_path, files))


    print(dir(glyph))
    print(glyph.width)
    print(glyph.vwidth)
    print(glyph.boundingBox())

    result = files.replace(" ", "")
    result = result.replace(".svg", "")
    result = process_string(result)

    html_content += f"""
    <i class="{css_class_prefix}{result} {css_class_additional}"></i>
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

font.save("dist/output-font.sfd")

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
