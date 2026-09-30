import os
import re
import json
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestJoyfulHearingIntegration(unittest.TestCase):

    def setUp(self):
        self.new_page_path = os.path.join(WORKSPACE_DIR, "best-hearing-aid-lucknow.html")
        self.index_path = os.path.join(WORKSPACE_DIR, "index.html")
        self.hearing_aids_path = os.path.join(WORKSPACE_DIR, "hearing-aids.html")
        self.brands_path = os.path.join(WORKSPACE_DIR, "brands.html")
        self.sitemap_path = os.path.join(WORKSPACE_DIR, "sitemap.xml")
        self.robots_path = os.path.join(WORKSPACE_DIR, "robots.txt")

        with open(self.new_page_path, "r", encoding="utf-8") as f:
            self.new_page_content = f.read()

        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index_content = f.read()

    def test_file_exists(self):
        """1. Verify new page file exists on disk."""
        self.assertTrue(os.path.exists(self.new_page_path), "best-hearing-aid-lucknow.html must exist.")

    def test_keyword_count_in_intro(self):
        """2. Content should open with an intro naturally using 'best hearing aid in Lucknow' 4-6 times."""
        # Find the editorial intro section
        intro_match = re.search(
            r'<!-- Editorial Intro Section.*?<div class="prose[^>]*>(.*?)</div>',
            self.new_page_content,
            re.DOTALL | re.IGNORECASE
        )
        self.assertIsNotNone(intro_match, "Editorial intro section must be present.")
        intro_text = intro_match.group(1)
        
        # Remove HTML tags for clean text matching
        clean_intro = re.sub(r'<[^>]+>', ' ', intro_text)
        pattern = re.compile(r'\bbest hearing aid in lucknow\b', re.IGNORECASE)
        matches = pattern.findall(clean_intro)
        count = len(matches)
        
        print(f"\n[Test] 'best hearing aid in Lucknow' occurrences in intro: {count}")
        self.assertGreaterEqual(count, 4, f"Expected at least 4 occurrences, found {count}")
        self.assertLessEqual(count, 6, f"Expected at most 6 occurrences, found {count}")

    def test_brands_and_trial_warranty_details(self):
        """3. List the brands from brands.html with trial/warranty details."""
        brands = ["ReSound", "Signia", "Widex", "Phonak", "Starkey"]
        for brand in brands:
            self.assertIn(brand, self.new_page_content, f"Brand {brand} must be mentioned.")

        # Verify Trial Details are present
        trial_mentions = re.findall(r'trial details', self.new_page_content, re.IGNORECASE)
        self.assertGreaterEqual(len(trial_mentions), 5, "Every brand should have trial details.")

        # Verify Warranty Details are present
        warranty_mentions = re.findall(r'warranty', self.new_page_content, re.IGNORECASE)
        self.assertGreaterEqual(len(warranty_mentions), 5, "Every brand should have warranty details.")

    def test_testimonials_pulled_from_homepage(self):
        """4. Pull in 2-3 existing testimonials from homepage that mention 'hearing aid'."""
        # Testimonial 1: Namrata Rajghar
        self.assertIn("Namrata Rajghar", self.new_page_content)
        self.assertIn("father is very happy with his new hearing aids", self.new_page_content)

        # Testimonial 2: Ramesh Verma
        self.assertIn("Ramesh Verma", self.new_page_content)
        self.assertIn("helped me choose the right hearing aid", self.new_page_content)

        # Testimonial 3: Manoj Tripathi
        self.assertIn("Manoj Tripathi", self.new_page_content)
        self.assertIn("hearing aid trial support", self.new_page_content)

    def test_faq_section_and_jsonld_schema(self):
        """5. Add FAQ section near bottom wrapped in FAQPage JSON-LD schema in <head>."""
        # Check FAQ content on the page
        target_question = "Which is the best hearing aid clinic in Lucknow?"
        self.assertIn(target_question, self.new_page_content, "FAQ question must be in page content.")

        # Extract JSON-LD scripts
        json_ld_matches = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            self.new_page_content,
            re.DOTALL
        )
        self.assertGreater(len(json_ld_matches), 0, "At least one JSON-LD block must exist.")

        faq_schema_found = False
        question_in_schema = False

        for json_str in json_ld_matches:
            try:
                data = json.loads(json_str.strip())
                if data.get("@type") == "FAQPage":
                    faq_schema_found = True
                    entities = data.get("mainEntity", [])
                    for entity in entities:
                        if entity.get("name") == target_question:
                            question_in_schema = True
                            self.assertTrue(len(entity.get("acceptedAnswer", {}).get("text", "")) > 10)
            except json.JSONDecodeError:
                self.fail("Malformed JSON-LD in <head>")

        self.assertTrue(faq_schema_found, "FAQPage JSON-LD schema must be in <head>")
        self.assertTrue(question_in_schema, f"'{target_question}' must be in the FAQPage JSON-LD schema.")

    def test_homepage_hero_and_footer_links(self):
        """6. Link to it from homepage hero section and footer 'Services' list."""
        # Hero section check
        hero_section = re.search(r'<main>.*?</section>', self.index_content, re.DOTALL)
        self.assertIsNotNone(hero_section, "Hero section must exist on homepage.")
        self.assertIn(
            'href="best-hearing-aid-lucknow.html"',
            hero_section.group(0),
            "Homepage hero section must link to best-hearing-aid-lucknow.html"
        )

        # Footer Services list check
        footer_section = re.search(r'<footer.*?</footer>', self.index_content, re.DOTALL)
        self.assertIsNotNone(footer_section, "Footer must exist on homepage.")
        footer_services = re.search(r'Services</h3>\s*<ul[^>]*>(.*?)</ul>', footer_section.group(0), re.DOTALL)
        self.assertIsNotNone(footer_services, "Footer Services list must exist on homepage.")
        self.assertIn(
            'href="best-hearing-aid-lucknow.html"',
            footer_services.group(1),
            "Footer Services list must link to best-hearing-aid-lucknow.html"
        )

    def test_navigation_dropdowns(self):
        """7. Add it as a link under 'Hearing Aids' nav dropdown alongside 'Types of Hearing Aids' and 'Hearing Aid Brands'."""
        pages_to_test = [self.new_page_path, self.index_path, self.hearing_aids_path, self.brands_path]
        for page_path in pages_to_test:
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
            basename = os.path.basename(page_path)
            
            # Check desktop dropdown
            self.assertIn('Types of Hearing Aids', content, f"{basename} must contain Types of Hearing Aids")
            self.assertIn('Hearing Aid Brands', content, f"{basename} must contain Hearing Aid Brands")
            self.assertIn('best-hearing-aid-lucknow.html', content, f"{basename} must link to best-hearing-aid-lucknow.html")

    def test_sitemap_and_robots(self):
        """8. Sitemap and robots.txt include the new URL."""
        self.assertTrue(os.path.exists(self.sitemap_path), "sitemap.xml must exist.")
        self.assertTrue(os.path.exists(self.robots_path), "robots.txt must exist.")
        
        with open(self.sitemap_path, "r", encoding="utf-8") as f:
            sitemap_content = f.read()
        self.assertIn("best-hearing-aid-lucknow.html", sitemap_content)

    def test_meta_description_length(self):
        """10. Meta description must be trimmed to about 155-160 characters."""
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', self.new_page_content)
        self.assertIsNotNone(desc_match, "Meta description tag must be present.")
        desc = desc_match.group(1)
        length = len(desc)
        print(f"\n[Test] Meta description length: {length} chars ('{desc}')")
        self.assertGreaterEqual(length, 150, f"Meta description is too short ({length} chars).")
        self.assertLessEqual(length, 160, f"Meta description is too long ({length} chars). Target: ~155-160.")

    def test_emi_financing_support(self):
        """11. Verify EMI and financing options are included on page and in FAQ schema."""
        # On-page check
        self.assertIn("0% EMI", self.new_page_content, "0% EMI badge/text should be present.")
        self.assertTrue(
            "Flexible EMI &amp; 0% Interest Financing" in self.new_page_content or "Flexible EMI & 0% Interest Financing" in self.new_page_content,
            "Flexible EMI & 0% Interest Financing heading must be present."
        )
        self.assertIn("Do you offer EMI or financing options for hearing aids in Lucknow?", self.new_page_content)

        # JSON-LD FAQ Schema check for EMI
        json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.new_page_content, re.DOTALL)
        emi_in_schema = False
        for json_str in json_ld_matches:
            data = json.loads(json_str.strip())
            if data.get("@type") == "FAQPage":
                for item in data.get("mainEntity", []):
                    if "EMI" in item.get("name", ""):
                        emi_in_schema = True
                        self.assertIn("0% interest financing", item.get("acceptedAnswer", {}).get("text", ""))
        self.assertTrue(emi_in_schema, "EMI question must be included in FAQPage JSON-LD schema.")

    def test_asset_links_integrity(self):
        """12. All local images referenced in the new page exist on disk."""
        img_srcs = re.findall(r'<img[^>]+src=["\'](.*?)["\']', self.new_page_content)
        for src in img_srcs:
            if not src.startswith("http") and not src.startswith("data:"):
                clean_src = src.split("?")[0]
                img_path = os.path.join(WORKSPACE_DIR, clean_src)
                self.assertTrue(os.path.exists(img_path), f"Referenced image {src} must exist at {img_path}")

    def test_performance_optimizations(self):
        """13. Verify elimination of Tailwind CDN, presence of static CSS, htaccess, and image dimensions."""
        # 1. No cdn.tailwindcss.com in index or best-hearing-aid-lucknow
        self.assertNotIn("cdn.tailwindcss.com", self.index_content, "Tailwind Play CDN must be removed from index.html.")
        self.assertNotIn("cdn.tailwindcss.com", self.new_page_content, "Tailwind Play CDN must be removed from best-hearing-aid-lucknow.html.")

        # 2. Static CSS referenced and exists
        self.assertIn("assets/tailwind.min.css", self.index_content)
        self.assertIn("assets/tailwind.min.css", self.new_page_content)
        tailwind_css_path = os.path.join(WORKSPACE_DIR, "assets", "tailwind.min.css")
        self.assertTrue(os.path.exists(tailwind_css_path), "assets/tailwind.min.css must exist.")
        css_size = os.path.getsize(tailwind_css_path)
        self.assertGreater(css_size, 5000, f"Tailwind CSS file is suspiciously small: {css_size} bytes")

        # 3. .htaccess exists with compression & caching
        htaccess_path = os.path.join(WORKSPACE_DIR, ".htaccess")
        self.assertTrue(os.path.exists(htaccess_path), ".htaccess must exist.")
        with open(htaccess_path, "r", encoding="utf-8") as f:
            htaccess_content = f.read()
        self.assertIn("mod_deflate.c", htaccess_content)
        self.assertIn("mod_expires.c", htaccess_content)

        # 4. 100% of images in index.html have width and height
        index_imgs = re.findall(r'<img[^>]+>', self.index_content)
        for img in index_imgs:
            self.assertTrue("width=" in img and "height=" in img, f"Image missing dimensions in index.html: {img}")

        # 5. 100% of images in best-hearing-aid-lucknow.html have width and height
        page_imgs = re.findall(r'<img[^>]+>', self.new_page_content)
        for img in page_imgs:
            self.assertTrue("width=" in img and "height=" in img, f"Image missing dimensions in best-hearing-aid-lucknow.html: {img}")

        # 6. Hero image preload present
        self.assertIn('rel="preload" as="image"', self.index_content)
        self.assertIn('rel="preload" as="image"', self.new_page_content)

if __name__ == "__main__":
    unittest.main()
