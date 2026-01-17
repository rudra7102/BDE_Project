import scrapy


class FacultySpider(scrapy.Spider):
    name = "faculty"
    allowed_domains = ["daiict.ac.in"]
    start_urls = [
        "https://www.daiict.ac.in/faculty"
    ]

    # ----------------------------------------
    # STAGE 1: FACULTY DIRECTORY PAGE
    # ----------------------------------------
    def parse(self, response):

        profile_links = response.css(
            "a[href*='/faculty/']::attr(href)"
        ).getall()

        # DEBUG (optional)
        self.logger.info(f"Found {len(profile_links)} profile links")

        for link in profile_links:
            yield response.follow(link, self.parse_faculty)

    # ----------------------------------------
    # STAGE 2: INDIVIDUAL FACULTY PAGE
    # ----------------------------------------
    def parse_faculty(self, response):

        name = response.css(
            "div.field--name-field-faculty-names::text"
        ).get(default="").strip()

        bio_parts = response.xpath(
            "//h2[normalize-space()='Biography']"
            "/following::div[contains(@class,'about')][1]//text()"
        ).getall()
        bio = " ".join(b.strip() for b in bio_parts if b.strip())

        specialization_parts = response.xpath(
            "//h2[normalize-space()='Specialization']"
            "/following::div[contains(@class,'work-exp')][1]//text()"
        ).getall()
        specialization = ", ".join(
            s.strip() for s in specialization_parts if s.strip()
        )

        teaching = response.xpath(
            "//h2[normalize-space()='Teaching']"
            "/following::div[contains(@class,'work-exp')][1]//li/text()"
        ).getall()
        teaching = [t.strip() for t in teaching if t.strip()]

        phone = response.css(
            "div.mobileIcon div.field--name-field-contact-no::text"
        ).get(default="").strip()

        email = response.css(
            "div.emailIcon div.field_item::text"
        ).get(default="").strip()

        yield {
            "name": name,
            "bio": bio,
            "specialization": specialization,
            "teaching": teaching,
            "phone": phone,
            "email": email,
            "profile_url": response.url
        }
