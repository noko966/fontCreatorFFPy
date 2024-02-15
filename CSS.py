import os
import glob
import cssutils
import logging
from colour import Color

cssutils.log.setLevel(logging.ERROR)

def generate_css_variables(prefix, keys):
    # Generate the dictionary with full variable names
    return {key: f"--{prefix}{key}" for key in keys}

def correct_case(css_text, essences, keys):
    # Dynamically generate the case corrections based on essences and keys
    case_corrections = {}
    for essence in essences:
        for key in keys:
            wrong_case = f"--{essence.lower()}{key.lower()}"
            correct_case = f"--{essence}{key}"
            case_corrections[wrong_case] = correct_case

    # Apply the case corrections
    for wrong, correct in case_corrections.items():
        css_text = css_text.replace(wrong, correct)
    
    return css_text

def add_missing_variables_to_css(css_file_path, essences, keys, output_dir):
    # Read the CSS file
    with open(css_file_path, 'r') as file:
        css_text = file.read()

    # Parse the CSS
    sheet = cssutils.parseString(css_text)

    # Initialize a dictionary to hold all variables for all essences
    all_variables = {}
    for essence in essences:
        all_variables.update(generate_css_variables(essence, keys))

    # Create a new :root rule to add missing variables
    root_rule = cssutils.css.CSSStyleRule()
    root_rule.selectorText = ':root'
    variables_added = False

    # Iterate over the essences and keys in the specified order
    for essence in essences:
        for key in keys:
            var_name = f"--{essence}{key}"
            # Check if this variable is already defined in the sheet
            # if not any(rule.style.getPropertyValue(var_name) for rule in sheet if rule.type == cssutils.css.CSSRule.STYLE_RULE):
                # Add the variable with a placeholder value if it's missing
            bg = "#000"
            for rule in sheet:
                print(var_name)
                
                if(rule.style.getPropertyValue(var_name)):
                    bg = rule.style.getPropertyValue(var_name)
                    root_rule.style.setProperty(var_name, rule.style.getPropertyValue(var_name))
                else:
                    print(Color(bg).lighten(0.2))
                    root_rule.style.setProperty(var_name, "#000")
            
            variables_added = True

    # If any variables were added, append the new :root rule to the sheet
    if variables_added:
        sheet.add(rule=root_rule)

    # Generate the new CSS text
    new_css_text = sheet.cssText.decode('utf-8')

    # Correct the case of essence names in variables
    new_css_text = correct_case(new_css_text, essences, keys)

    # Define the output file path and write the modified CSS
    output_file_path = os.path.join(output_dir, os.path.basename(css_file_path))
    with open(output_file_path, 'w') as file:
        file.write(new_css_text)

def process_all_css_files(input_dir, output_dir, essences, keys):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .css files in the input directory
    css_files = glob.glob(os.path.join(input_dir, '*.css'))
    
    # Process each file
    for css_file in css_files:
        add_missing_variables_to_css(css_file, essences, keys, output_dir)

# Define the order of keys
keys = [
    'G', 'Bg', 'Bg2', 'Bg3', 'Bghover', 'Bg2hover', 'Bg3hover',
    'Txt', 'Txt2', 'Txt3', 'Accent', 'AccentTxt', 'RGBA', 'RGBA2', 'RGBA3',
    'Radius', 'Border',
]

# Example usage
input_dir = "css_manipulator/input_css_files"
output_dir = "css_manipulator/output_css_files"
essences = ["body", "accent"]
process_all_css_files(input_dir, output_dir, essences, keys)