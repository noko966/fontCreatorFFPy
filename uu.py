import fontforge
import os
import re

folder_path = 'icons'
font = fontforge.open('aa.ttf')

files = os.listdir(folder_path)

# Remove the '-01.svg' suffix using regular expression
filesArray = []

html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
"""

# Generate CSS content
css_content = """
@font-face {
  font-family: "esportIconsFont";
  src: url("esportIcons.eot");
  src: url("esportIcons.eot?#iefix") format("embedded-opentype"),
    url("esportIcons.woff2") format("woff2"),
    url("esportIcons.woff") format("woff"),
    url("esportIcons.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.ico_font-L {
  width: 36px !important;
  height: 36px !important;
  line-height: 36px !important;
  font-size: 36px !important;
}

[class^="ico_font-"],
[class*=" ico_font-"] {
  font-family: "esportIconsFont";
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
  content: "\\e051";
  direction: ltr !important;
  background: #41487d;
  color: #fff;
  border-radius: 8px;
}
"""

for file in files:
    filesArray.append(file)

print(len(filesArray))

for idx, files in enumerate(filesArray):
    uv = 'uniE006'
    hexToInt = int("E000", 16) + idx
    intToHex = hex(hexToInt)[2:].upper()
    # print(hexToInt, intToHex)
    glyph = font.createMappedChar('uni' + intToHex)
    glyph.importOutlines('icons/' + files)

    result = re.sub(r'-\d+\.svg$', '', files)
    result = result.replace(" ", "")

    html_content += f"""
    <i class="ico_font-{result} ico_font-L"></i>
    """

    css_content += f"""
    .ico_font-{result}::before {{
        content: "\\{intToHex}";
    }}
    """


html_content += f"""
      </body>
</html>
    """

font.save('output-font.sfd')

font.generate("esportIcons.ttf")
font.generate("esportIcons.eot")
font.generate("esportIcons.woff")
font.generate("esportIcons.woff2")

# Save HTML file
html_file_path = "index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)
