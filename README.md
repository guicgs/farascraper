# __Active Foreign Principals Scraper__
Scraping Foreign Principals Take-home Test

## __Documentation__
- [Overview](#overview)
- [Setup](#setup)
- [Running the scraper](#running-the-scraper)
- [Settings](#settings)
- [Running tests](#running-tests)
- [Take-home Test Biggest Challenges](#take-home-test-biggest-challenges)
- [Possible Enhancements](#possible-enhancements)
- [Final Observations](#final-observations)

## __Overview__
Application to extract Active Foreign Principals data from [Foreign Agents Registration Act section](https://www.fara.gov/quick-search.html) on the US Department of Justice website.

It was built using Python and Scrapy, a framework used for web scraping and web crawling. 

## __Setup__
To run the application, it is necessary to activate the virtual environment and install the project dependencies.

- First, open the `scraper` folder and run the following command to create the virtual environment and activate it:
  ```
  python3 -m venv .venv && source .venv/bin/activate
  ```

- Then, run the following command to install the application's dependencies:
  ```
  pip install -r requirements.txt 
  ``` 
  *(If you have any problems during installation related to `pip`, just follow the instructions on the terminal to update it.)*

## __Running the scraper__
- After the installation is complete, enter the `farascraper` folder:
  ```
  cd farascraper/
  ``` 
- ### __To start the application, simply run the following command:__
  ```
  scrapy crawl active_foreign_principals_scraper
  ```
  This command will extract all the Active Foreign Principals data. 

- All the data will be saved in a `items.json` file inside a `results` folder. This file will always be overwritten every time the web scraping is run (this can be changed, see [Settings](#settings)).
  
  Each extracted item will look like this:
  ```
  {
    "url": "https://efile.fara.gov/ords/f?p=171:200:::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:6630,Exhibit%20AB,BELGIUM",
    "foreign_principal": "European People's Party",
    "fp_reg_date": "2019-01-28T00:00:00",
    "address": "10 Rue de Commerce",
    "state": null,
    "country": "BELGIUM",
    "registrant": "Shepura, Nathan",
    "reg_num": "6630",
    "reg_date": "2019-01-28T00:00:00",
    "exhibits": [
      {
        "url": "https://efile.fara.gov/docs/6630-Exhibit-AB-20200226-2.pdf",
        "date": "2020-02-26T00:00:00"
      },
      {
        "url": "https://efile.fara.gov/docs/6630-Exhibit-AB-20190128-1.pdf",
        "date": "2019-01-28T00:00:00"
      }
    ]
  }
  ```

## __Settings__
- ### Save the data to a MongoDB collection
  There's a Scrapy Pipeline to connect and save all the data collected to a MongoDB collection. 
  
  To run this pipeline, just pass a `db=mongo` as a command-line argument:
  ```
  scrapy crawl active_foreign_principals_scraper -a db=mongo
  ``` 
  Make sure you have MongoDB installed and started to run it.

- ### Limit the number of results
  To limit the number of the items collected, pass a "count" argument with the desired number of items to be extracted:
  ```
  scrapy crawl active_foreign_principals_scraper -a count=3
  ```
- ### Disable `json` file overwrite
  To disable `json` file overwriting every time the scraper is run, just change the respective `FEEDS` item in the `custom_settings` object of the class `ActiveForeignPrincipalsScraper`:
  ```
  class ActiveForeignPrincipalsScraper(scrapy.Spider):
      ...
      custom_settings = {
            "FEEDS": {
                "results/items.json": {
                  "format": "json", 
                  "overwrite": False
                },
            },
            ...
      }
  ```

## __Running tests__
There are two "test suites" in the application. The first one was written by me and has some few unit tests, including tests for utils functions. The other one is from an external library called [Scrapy Autounit](https://github.com/scrapinghub/scrapy-autounit) and creates fixtures and tests for each item and request. In the [Take-home Test Biggest Challenges](#testing-the-application) section I talk more about my choice.
- To run the unit tests I created:
  ```
  pytest farascraper/tests/tests.py
  ```
- To run the unit tests generated by Scrapy Autounit:
  ```
  python -m unittest discover autounit/tests/
  ```

## __Take-home Test Biggest Challenges__
- ### First time with Scrapy
  This was the first time I used Scrapy. So it was an interesting challenge to learn a new framework and still be able to explore its functionalities in the best possible way, considering the time I had. I liked it very much.
  
  I had already done web scraping, but with the HTTP library called requests. At first, I tried to do the test with it, but I couldn't make it works. 
  
  After I found the static addresses of the pages (I talk more about this in my [Final Observations](#final-observations)), it is possible that it would be easier to make requests using the requests lib, but I didn't have time to try. 

- ### Ajax Identifier
  The POST request to get all the foreign principals' data requires a `p_instance` in the request's body. You can find the other dynamic parameters in the URL itself, but that specific Ajax parameter is contained within a `<script>` tag that can be found in the RAW HTML. It took me a while to realize it. 

- ### Testing the application
  I am aware that I could have tested the application more satisfactorily. I've already tested other Python applications with pytest and mock, but I couldn't understand as well as I could how to instantiate the web scraping Class and mock the results of the requests, and finally, test the final results. Unfortunately, I couldn't find much about web scraping testing on the internet. I kept the tests I wrote just to show how far I got, in the time I had, and I decided to use an external library that, as far as I was able to evaluate, works very well.

## __Possible Enhancements__
- ### Architecture
  - I don't know if it's a good practice when we make scrapers, but a possibility of improving the architecture would be to make a more generic Class to support other searches on the same website.

- ### Functionalities
  - With more time, I would have built functions to apply multiple filters to the results saved in the Mongo database (as I did in another web scraping project). And maybe build an API to do it;
  - Other option for the filters I mentioned above, would be do it by arguments via command-line (but personally, in that case, I prefer the API);
  - Declare the type (using typing) of the variables, function's arguments and returns, and Item's fields;
  - Explore more possible pipelines;
  - Assess if it is necessary to deal with Exceptions that may not be covered by Scrapy.

- ### Tests
  - Understand in more depth the operation of Scrapy to write more and better unit and integration tests, without any external dependency. 

## __Final Observations__
At first, I used the dynamic URLs generated by the FARA website, and the scraper worked very well, exactly the way it is structured now (changing only a few CSS selectors), saving all the information as required. 

Scrapy handles the flow of cookies, headers, etc., very well between requests. However, the URL extracted from each foreigner was also dynamic, which meant that the URL saved in the final file did not lead directly to the foreigner principal's page, as it requires all this previous communication between requests. 

Looking at the Take-home Test instructions, I realized that in the object used as a model of the result there was a small difference in the URL parameters (the number "171" instead of "1381"). With this "flow_id" 171 I would be able to navigate between pages without needing to pass additional information in addition to the information already contained in the URL. In practice, it didn't make any difference to the written code (as I said, just a few CSS selectors), but it made it possible for me to save each foreigner's static URL. 
