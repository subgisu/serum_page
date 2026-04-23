import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The script tag has <script type="__bundler/template">\n"<!DOCTYPE html>...
# We will just do a string replacement on the raw file content.
old_style = "  .s-st-headline { font-family: 'Nanum Myeongjo', 'Batang', serif; font-size: 24px; font-weight: 400; color: var(--black); margin-bottom: 20px; letter-spacing: -0.02em; }"

new_style = "  .s-st-headline { font-size: 24px; font-weight: 500; color: var(--black); margin-bottom: 20px; letter-spacing: -0.02em; }"

if old_style in content:
    content = content.replace(old_style, new_style)
    print("Replaced successfully (single line format)")
else:
    # Let's try JSON encoded format if it was formatted
    # Actually, let's just use regex to replace it
    import re
    # Match `.s-st-headline { ... }` in the json string which has `\\n`
    pattern = r'\.s-st-headline\s*\\n\s*\{\\n\s*font-family:\s*\'Nanum Myeongjo\',\s*\'Batang\',\s*serif;\\n\s*font-size:\s*24px;\\n\s*font-weight:\s*400;\\n\s*color:\s*var\(--black\);\\n\s*margin-bottom:\s*20px;\\n\s*letter-spacing:\s*-0\.02em;\\n\s*\}'
    
    replacement = '.s-st-headline \\n      {\\n      font-size: 24px;\\n      font-weight: 500;\\n      color: var(--black);\\n      margin-bottom: 20px;\\n      letter-spacing: -0.02em;\\n    }'
    
    new_content, count = re.subn(pattern, replacement, content)
    if count > 0:
        content = new_content
        print(f"Replaced {count} times (regex format 1)")
    else:
        # Try another regex
        pattern2 = r'\\n\s*\.s-st-headline\s*\{\\n\s*font-family:\s*\'Nanum Myeongjo\',\s*\'Batang\',\s*serif;\\n\s*font-size:\s*24px;\\n\s*font-weight:\s*400;\\n\s*color:\s*var\(--black\);\\n\s*margin-bottom:\s*20px;\\n\s*letter-spacing:\s*-0\.02em;\\n\s*\}'
        replacement2 = '\\n    .s-st-headline {\\n      font-size: 24px;\\n      font-weight: 500;\\n      color: var(--black);\\n      margin-bottom: 20px;\\n      letter-spacing: -0.02em;\\n    }'
        new_content, count = re.subn(pattern2, replacement2, content)
        if count > 0:
            content = new_content
            print(f"Replaced {count} times (regex format 2)")
        else:
            # Let's try matching just the font-family line inside .s-st-headline
            print("Trying to find the block...")
            match = re.search(r'\.s-st-headline.*?\}', content, re.DOTALL)
            if match:
                print("Found block:")
                print(match.group(0))
            else:
                print("Could not find .s-st-headline at all!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
