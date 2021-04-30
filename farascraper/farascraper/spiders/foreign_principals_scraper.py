import scrapy

from farascraper.items import ActiveForeignPrincipalItem

from .utils import (
    format_date,
    get_ajax_identifier,
)


class ActiveForeignPrincipalsScraper(scrapy.Spider):
    """
    Class responsible for scraping all Active Foreign Principals data
    from US Department of Justice website
    """

    name = "active_foreign_principals_scraper"

    custom_settings = {
        "FEEDS": {
            "results/items.json": {"format": "json", "overwrite": True},
        },
        "SPIDER_MIDDLEWARES": {
            "farascraper.middlewares.FarascraperSpiderMiddleware": 543,
            "scrapy_autounit.AutounitMiddleware": 950,
        },
        "AUTOUNIT_ENABLED": False,
        "ITEM_PIPELINES": {
            "farascraper.pipelines.FarascraperPipeline": 300,
        },
    }

    base_url = "https://efile.fara.gov/ords"

    def start_requests(self):
        yield scrapy.Request(
            url="https://efile.fara.gov/ords/f?p=171:1",
            callback=self.parse_active_foreign_principals_page,
        )

    def parse_active_foreign_principals_page(self, response):
        foreign_principals_path = response.css(
            "ul#L80330217189774968 li a::attr(href)"
        ).get()
        yield scrapy.Request(
            f"{self.base_url}/{foreign_principals_path}",
            callback=self.parse_active_foreign_principals_data,
        )

    def parse_active_foreign_principals_data(self, response):
        """Send a POST request to get all the results in the page"""

        # dynamic POST payload fields
        p_flow_id = response.css("input[name=p_flow_id]::attr(value)").get()
        p_flow_step_id = response.css("input[name=p_flow_step_id]::attr(value)").get()
        p_instance = response.css("input[name=p_instance]::attr(value)").get()
        ajax_identifier = get_ajax_identifier(response.text)

        # Number of foreign principals to be extracted
        # It can be number passed in a "count" argument in the command-line
        # Or the total count of the foreign principals on the page
        active_foreign_principals_count = ""
        count = getattr(self, "count", None)
        if count is not None:
            active_foreign_principals_count = count
        else:
            active_foreign_principals_count = (
                response.css("span.display_only[id=P130_FP_NBR]::text").get().strip()
            )

        # POST request payload
        formdata = {
            "p_flow_id": p_flow_id,
            "p_flow_step_id": p_flow_step_id,
            "p_instance": p_instance,
            "p_request": f"PLUGIN={ajax_identifier}",
            "p_widget_name": "worksheet",
            "p_widget_mod": "ACTION",
            "p_widget_action": "BREAK",
            "p_widget_num_return": active_foreign_principals_count,
            "x01": "80340213897823017",
            "x02": "80341508791823021",
            "x03": "COUNTRY_NAME",
        }

        yield scrapy.FormRequest(
            "https://efile.fara.gov/ords/wwv_flow.ajax",
            callback=self.extract_data,
            formdata=formdata,
        )

    def extract_data(self, response):
        """
        Extract all data from CSS and save it to an Item
        Calls the next GET request to extract all the exhibits URLs
        """

        table_rows = response.css("table#80340213897823017 tr")[1:]

        for row in table_rows:
            path = row.css("td[headers=LINK] a::attr(href)").get()
            url = f"{self.base_url}/{path}"
            foreign_principal = row.css("td[headers=FP_NAME]::text").get()
            fp_reg_date = row.css("td[headers=FP_REG_DATE]::text").get()
            address = row.css("td[headers=ADDRESS_1]::text").get()
            state = row.css("td[headers=STATE]::text").get()
            country = row.css("td[headers=COUNTRY_NAME]::text").get()
            registrant = row.css("td[headers=REGISTRANT_NAME]::text").get()
            reg_num = row.css("td[headers=REG_NUMBER]::text").get()
            reg_date = row.css("td[headers=REG_DATE]::text").get()

            foreign_principal_item = ActiveForeignPrincipalItem(
                url=url,
                foreign_principal=foreign_principal,
                fp_reg_date=format_date(fp_reg_date),
                address=address.strip(),
                state=state,
                country=country,
                registrant=registrant,
                reg_num=reg_num,
                reg_date=format_date(reg_date),
            )

            yield scrapy.Request(
                url,
                callback=self.extract_exhibit_url,
                cb_kwargs={"foreign_principal_item": foreign_principal_item},
                dont_filter=True,
            )

    def extract_exhibit_url(self, response, foreign_principal_item):
        """Extract the PDF document URL of the Foreign Principal page"""

        exhibit_rows = response.css("div.a-IRR-tableContainer tr")[1:]
        exhibit_urls = []
        for row in exhibit_rows:
            exhibit_url = row.css(
                "td.u-tL[headers=DOCLINK] a::attr(href)"
            ).get()
            exhibit_date = format_date(
                row.css("td.u-tL[headers=DATE_STAMPED]::text").get()
            )
            exhibit_urls.append({"url": exhibit_url, "date": exhibit_date})
        foreign_principal_item["exhibits"] = exhibit_urls
        yield foreign_principal_item
