import mock
from scrapy.http import HtmlResponse

from farascraper.spiders.foreign_principals_scraper import (
    ActiveForeignPrincipalsScraper,
)
from farascraper.spiders.utils import (
    format_date,
    get_ajax_identifier,
)
from farascraper.tests.mock_html import html


class TestActiveForeignPrincipalsScraper(object):
    def test_parse_active_foreign_principals_page(self):
        url = "https://efile.fara.gov/ords/f?p=1381:1:5921812400951:::::"
        mock_response = HtmlResponse(url=url)
        return_value = "return_value"

        with mock.patch.object(
            ActiveForeignPrincipalsScraper,
            "parse_active_foreign_principals_page",
            return_value=return_value,
        ) as scraper_method:
            scraper = ActiveForeignPrincipalsScraper()
            result = scraper.parse_active_foreign_principals_page(
                mock_response
            )

        scraper_method.assert_called_once_with(mock_response)
        assert result == return_value

    def test_parse_active_foreign_principals_data(self):
        url = "https://efile.fara.gov/ords/f?p=1381:130:13852610166285::NO:RP,130:P130_DATERANGE:N"
        mock_response = HtmlResponse(url=url)
        return_value = "return_value"

        with mock.patch.object(
            ActiveForeignPrincipalsScraper,
            "parse_active_foreign_principals_data",
            return_value=return_value,
        ) as scraper_method:
            scraper = ActiveForeignPrincipalsScraper()
            result = scraper.parse_active_foreign_principals_data(
                mock_response
            )

        scraper_method.assert_called_once_with(mock_response)
        assert result == return_value

    def test_extract_data(self):
        url = "https://efile.fara.gov/ords/wwv_flow.ajax"
        mock_response = HtmlResponse(url=url)
        return_value = "return_value"

        with mock.patch.object(
            ActiveForeignPrincipalsScraper,
            "extract_data",
            return_value=return_value,
        ) as scraper_method:
            scraper = ActiveForeignPrincipalsScraper()
            result = scraper.extract_data(mock_response)

        scraper_method.assert_called_once_with(mock_response)
        assert result == return_value

    def test_extract_exhibit_url(self):
        url = "https://efile.fara.gov/ords/f?p=1381:200:13852610166285::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6399,Exhibit%20AB,AUSTRALIA"
        mock_response = HtmlResponse(url=url)
        return_value = "return_value"

        with mock.patch.object(
            ActiveForeignPrincipalsScraper,
            "extract_exhibit_url",
            return_value=return_value,
        ) as scraper_method:
            scraper = ActiveForeignPrincipalsScraper()
            result = scraper.extract_exhibit_url(mock_response)

        scraper_method.assert_called_once_with(mock_response)
        assert result == return_value


class TestActiveForeignPrincipalsScraperUtils:
    def test_format_date(self):
        date1 = "03/25/1999"
        date2 = "05/16/2008"
        assert format_date(date1) == "1999-03-25T00:00:00"
        assert format_date(date2) == "2008-05-16T00:00:00"

    def test_get_ajax_identifier(self):
        assert get_ajax_identifier(html) == "5EXplKSaR7JiG5np0CApU6LVznt5zWzSiIfVJMPinvVM59SqAvNzajHT7_d_wJzk"
