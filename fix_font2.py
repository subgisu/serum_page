import json
import sys

def main():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # find the json string
        import re
        match = re.search(r'(<script type="__bundler/template">\s*)(["\'].*?["\'])(\s*</script>)', content, re.DOTALL)
        if not match:
            print("Template not found")
            return
            
        json_str = match.group(2)
        try:
            template_html = json.loads(json_str)
        except:
            print("Failed to parse JSON")
            return
            
        # replace the style in the decoded HTML
        old_style1 = ".s-st-headline { font-family: 'Nanum Myeongjo', 'Batang', serif; font-size: 24px; font-weight: 400; color: var(--black); margin-bottom: 20px; letter-spacing: -0.02em; }"
        new_style = ".s-st-headline { font-size: 24px; font-weight: 500; color: var(--black); margin-bottom: 20px; letter-spacing: -0.02em; }"
        
        # It might have newlines in the decoded html
        old_style_re = r'\.s-st-headline\s*\{\s*font-family:\s*\'Nanum Myeongjo\',\s*\'Batang\',\s*serif;\s*font-size:\s*24px;\s*font-weight:\s*400;\s*color:\s*var\(--black\);\s*margin-bottom:\s*20px;\s*letter-spacing:\s*-0\.02em;\s*\}'
        
        new_style_formatted = '''.s-st-headline {
      font-size: 24px;
      font-weight: 500;
      color: var(--black);
      margin-bottom: 20px;
      letter-spacing: -0.02em;
    }'''
        
        template_html, count = re.subn(old_style_re, new_style_formatted, template_html)
        print(f"Replaced {count} times")
        
        if count == 0:
            print("Could not find the style block in decoded HTML. Trying to find anything with Nanum Myeongjo...")
            print(re.findall(r'.{0,50}Nanum Myeongjo.{0,50}', template_html))
            return
            
        # re-encode to json
        new_json_str = json.dumps(template_html, ensure_ascii=False)
        
        new_content = content[:match.start(2)] + new_json_str + content[match.end(2):]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
