import glob
import os
from datetime import datetime

domain = "https://joyfulhearingandspeech.com"
html_files = sorted(glob.glob("*.html"))
today = datetime.now().strftime("%Y-%m-%d")

# High priority pages
priority_map = {
    "index.html": ("1.0", "daily"),
    "best-hearing-aid-lucknow.html": ("0.9", "weekly"),
    "hearing-aids.html": ("0.9", "weekly"),
    "hearing-test.html": ("0.8", "weekly"),
    "speech-therapy.html": ("0.8", "weekly"),
    "brands.html": ("0.8", "weekly"),
    "contact.html": ("0.8", "monthly"),
    "about.html": ("0.7", "monthly"),
    "services.html": ("0.8", "weekly"),
    "blog.html": ("0.8", "weekly"),
}

xml_entries = []
for file in html_files:
    priority, freq = priority_map.get(file, ("0.6", "monthly"))
    url_path = "" if file == "index.html" else file
    loc = f"{domain}/{url_path}" if url_path else f"{domain}/"
    xml_entries.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_entries)}
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)
print(f"sitemap.xml generated with {len(html_files)} URLs.")

robots_content = f"""User-agent: *
Allow: /

Sitemap: {domain}/sitemap.xml
"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)
print("robots.txt generated successfully.")
