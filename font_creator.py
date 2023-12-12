import os
import fontforge

# config for Paths and Names
source_folder = "src"
dest_folder = "dist"
icons_folder = "icons"
source_blank_font = "source_empty_font.ttf"

# config for font names
font_file_name = "eSportsIcons"
font_family_name = "{}Font".format(font_file_name)
# config for glyph class names
css_class_prefix = "es_glyph_"
css_class_additional = "dg_glyph"
# configs for glyph sizes
glyph_sizes = {"sm": "16", "md": "20", "lg": "28", "xl": "32"}
glyph_default_size = "24"
# config for demo html
demo_html_file_name = "index.html"
icons_marker = "<!-- icons -->"

# init needed variables
src_icons_path = os.path.join(source_folder, icons_folder)
font = fontforge.open(os.path.join(source_folder, source_blank_font))
filesArray = os.listdir(src_icons_path)

html_content = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="{font_file_name}.css" />
    <style>
    *, *:before, *:after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      outline: 0;
      border: 0;
      font-size: 100%;
      font: inherit;
      vertical-align: baseline;
      }}
      
    :root{{
    --iconSize: {glyph_default_size}px;
      
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
    html {{
      background: var(--bodyBg);
      color: var(--bodyTxt);
    }}
    
    .icons_container {{
      display: flex;
      flex-direction: row;
      justify-content: center;
      gap: calc(var(--iconSize) * 0.6);
      flex-wrap: wrap;
      padding-left: calc(var(--iconSize) * 0.5);
      padding-right: calc(var(--iconSize) * 0.5);
      background: var(--bodyBg);
      border: 1px solid var(--151A1E);
      padding: calc(var(--iconSize) * 1.6);
    }}
    
    .icons_container .{css_class_additional} {{
      border-radius: 2px;
      background: var(--dominantBg);
      color: var(--dominantTxt);
      cursor: pointer;
      transition: all 0.3s;
    }}

  </style>
  </head>
  <body>
    <div class="icons_container">
    {icons_marker}
    </div>
  </body>
</html>
"""

# Generate CSS content
css_content = f"""
@font-face {{
  font-family: "{font_family_name}";
  src: url("{font_file_name}.eot");
  src: url("{font_file_name}.eot?#iefix") format("embedded-opentype"),
    url("{font_file_name}.woff2") format("woff2"),
    url("{font_file_name}.woff") format("woff"),
    url("{font_file_name}.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}}



[class^="{css_class_prefix}"],
[class*=" {css_class_prefix}"] {{
  --iconSize: 24px;
  font-family: "{font_family_name}";
  display: inline-block;
  flex-shrink: 0;
  width: var(--iconSize);
  height: var(--iconSize);
  line-height: var(--iconSize);
  font-size: var(--iconSize);
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

for key, value in glyph_sizes.items():
    css_content += f"""
    .{css_class_additional}.{key} {{
        --iconSize: {value}px;
    }}
    """


def process_string(s):
    result = ""
    for i, char in enumerate(s):
        if char.isupper():
            # If it's the start of the string or follows a space, convert to lowercase
            if i == 0 or s[i - 1] == " ":
                result += char.lower()
            else:
                # Otherwise, add an underscore before it and convert to lowercase
                result += "_" + char.lower()
        else:
            result += char
    return result


icons_from_index = html_content.index(icons_marker) + len(icons_marker)

for idx, files in enumerate(filesArray):
    uv = "uniE006"
    hexToInt = int("E000", 16) + idx
    intToHex = hex(hexToInt)[2:].upper()
    # print(hexToInt, intToHex)
    glyph = font.createMappedChar("uni" + intToHex)
    glyph.importOutlines(os.path.join(src_icons_path, files))

    # print(dir(glyph))
    # print(glyph.width)
    # print(glyph.vwidth)
    # print(glyph.boundingBox())

    result = files.replace(" ", "")
    result = result.replace(".svg", "")
    result = process_string(result)

    for key, value in glyph_sizes.items():
        html_content = (
            html_content[:icons_from_index]
            + f"""
      <i class="{css_class_prefix}{result} {css_class_additional} {key}" title="{result} | {"uni" + intToHex}"></i>
      """
            + html_content[icons_from_index:]
        )

    css_content += f"""
    .{css_class_prefix}{result}::before {{
        content: "\\{intToHex}";
    }}
    """


font.save("{}/{}.sfd".format(dest_folder, font_file_name))

output_formats = ["ttf", "eot", "woff", "woff2"]

for output_format in output_formats:
    font.generate("{}/{}.{}".format(dest_folder, font_file_name, output_format))

# Save HTML file
with open(("{}/{}".format(dest_folder, demo_html_file_name)), "w") as html_file:
    html_file.write(html_content)
# Save CSS file
with open(("{}/{}.css".format(dest_folder, font_file_name)), "w") as css_file:
    css_file.write(css_content)
