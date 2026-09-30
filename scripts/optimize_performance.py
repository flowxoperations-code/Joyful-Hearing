import os
import re
import glob

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def optimize_html_files():
    html_files = glob.glob(os.path.join(WORKSPACE_DIR, "*.html"))
    print(f"Found {len(html_files)} HTML files to optimize.")

    # 1. Regex for Tailwind CDN -> Static CSS
    tailwind_pattern = re.compile(
        r'<script\s+src=[\"\']https://cdn\.tailwindcss\.com[\"\']></script>\s*(?:<script\s+src=[\"\']assets/tailwind-config\.js[^>]*></script>)?',
        re.DOTALL
    )
    tailwind_replacement = '<link rel="stylesheet" href="assets/tailwind.min.css?v=20260920" />'

    # 2. Regex for Google Fonts non-blocking
    fonts_pattern = re.compile(
        r'<link\s+href=[\"\']https://fonts\.googleapis\.com/css2\?family=Manrope[^\"]+[\"\']\s+rel=[\"\']stylesheet[\"\']\s*/>',
        re.DOTALL
    )
    fonts_replacement = (
        '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700&display=swap" />\n'
        '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700&display=swap" media="print" onload="this.media=\'all\'" />\n'
        '    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@500;600;700&display=swap" /></noscript>'
    )

    # 3. Google Translate optimized loader
    old_translate_pattern = re.compile(
        r'<script\s+type=[\"\']text/javascript[\"\']\s+src=[\"\']https://translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit[\"\']></script>',
        re.DOTALL
    )

    new_translate_snippet = (
        '  <script type="text/javascript">\n'
        '    function loadGoogleTranslate() {\n'
        '      if (!document.getElementById("google-translate-script")) {\n'
        '        var s = document.createElement("script");\n'
        '        s.id = "google-translate-script";\n'
        '        s.type = "text/javascript";\n'
        '        s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";\n'
        '        document.body.appendChild(s);\n'
        '      }\n'
        '    }\n'
        '    if ("requestIdleCallback" in window) {\n'
        '      requestIdleCallback(loadGoogleTranslate, { timeout: 3500 });\n'
        '    } else {\n'
        '      window.addEventListener("load", function() { setTimeout(loadGoogleTranslate, 1500); });\n'
        '    }\n'
        '  </script>'
    )

    updated_count = 0
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        # Replace Tailwind
        if tailwind_pattern.search(new_content):
            new_content = tailwind_pattern.sub(tailwind_replacement, new_content)

        # Replace Google Fonts
        if fonts_pattern.search(new_content):
            new_content = fonts_pattern.sub(fonts_replacement, new_content)

        # Replace Google Translate blocking script
        if old_translate_pattern.search(new_content):
            new_content = old_translate_pattern.sub(new_translate_snippet, new_content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_count += 1

    print(f"Successfully updated Tailwind, Fonts, and Translate in {updated_count} files.")

if __name__ == "__main__":
    optimize_html_files()
