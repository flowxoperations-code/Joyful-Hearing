import glob
import re

desktop_link = '''                <a href="best-hearing-aid-lucknow.html" class="flex gap-4 p-4 rounded-xl hover:bg-slate-50 transition-colors group">
                  <div class="text-joy-blue mt-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.45 1-1 1H7"/><path d="M14 14.66V17c0 .55.45 1 1 1h2"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
                  </div>
                  <div>
                    <p class="font-bold text-joy-ink text-sm mb-1 group-hover:text-joy-blue transition-colors">Best Hearing Aid in Lucknow</p>
                    <p class="text-xs text-slate-500 leading-relaxed">Compare top brands, trial procedures, and clinical warranties in Lucknow.</p>
                  </div>
                </a>'''

mobile_link = '''              <a href="best-hearing-aid-lucknow.html" class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-50">Best Hearing Aid in Lucknow</a>'''

footer_service_link = '''              <li><a href="best-hearing-aid-lucknow.html" class="transition-colors hover:text-joy-red">Best Hearing Aid in Lucknow</a></li>'''

html_files = sorted(glob.glob("*.html"))
updated_count = 0

for filepath in html_files:
    if filepath == "best-hearing-aid-lucknow.html":
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Desktop navigation: insert under brands.html link if not present
    if 'href="best-hearing-aid-lucknow.html"' not in content:
        # Look for the brands.html link in desktop dropdown
        pattern_desktop = re.compile(
            r'(<a href="brands\.html"[^>]*>.*?</a>\s*</div>)',
            re.DOTALL
        )
        if pattern_desktop.search(content):
            content = pattern_desktop.sub(
                lambda m: m.group(1)[:-6] + "\n" + desktop_link + "\n              </div>",
                content,
                count=1
            )
            modified = True

    # 2. Mobile navigation: insert under brands.html link if not present in mobile menu
    if 'best-hearing-aid-lucknow.html' not in content or content.count('best-hearing-aid-lucknow.html') < 2:
        # Check if mobile link is missing
        pattern_mobile = re.compile(
            r'(<a href="brands\.html" class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-50">Hearing Aid Brands</a>)',
            re.DOTALL
        )
        if pattern_mobile.search(content) and 'class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-50">Best Hearing Aid in Lucknow</a>' not in content:
            content = pattern_mobile.sub(
                r'\1\n              <a href="best-hearing-aid-lucknow.html" class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-50">Best Hearing Aid in Lucknow</a>',
                content,
                count=1
            )
            modified = True

    # 3. Footer Services list: check if footer has services list
    pattern_footer = re.compile(
        r'(<h3 class="mb-4 font-semibold text-white">Services</h3>\s*<ul class="space-y-3 text-sm text-slate-400">)',
        re.DOTALL
    )
    if pattern_footer.search(content) and 'best-hearing-aid-lucknow.html' not in content[content.find('Services</h3>'):]:
        content = pattern_footer.sub(
            r'\1\n' + footer_service_link,
            content,
            count=1
        )
        modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated_count += 1
        print(f"Updated navigation and footer in: {filepath}")

print(f"Total files updated: {updated_count}")
