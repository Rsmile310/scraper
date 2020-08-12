**The tech scraper can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk and Elgiganten.dk**
**The Fakta scraper can scrape discounts from this week discounts.**

# Table of contents
- [First setup](#first-setup)
- [Tech scraper](#tech-scraper)
    - [Scrape products](#scrape-products)
    - [Adding products](#adding-products)
        - [Optional arguments](#optional-arguments)
- [Fakta scraper](#fakta-scraper)
    - [Scrape discounts](#scrape-discounts)

<br/>

## First setup <a name="first-setup"></a>
First make sure you have the modules, run this in the terminal:

    pip install -r requirements.txt

Then cd into the tech_scraping directory:

    cd tech_scraping

<br/>

# Tech scraper <a name="tech-scraper"></a>
The tech scraper can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk and Elgiganten.dk

## Scrape products <a name="scrape-products"></a>
To scrape prices of products run this in the terminal:

    python3 scraping.py

## Adding products <a name="adding-products"></a>
Before scraping a new product, run a similar line to this:

    python3 add_product.py <category> <url>
e.g.

    python3 add_product.py gpu https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio
**OBS: the category can only be one word, so add a underscore instead of a space if needed.**

<br/>Then add a line in this form in the last if-statement in scraping.py:

    <site>('<category>', '<link>')
e.g.

    Komplett('gpu', 'https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio')
**OBS: make sure the category and product name has been created with add_product.py**

### Optional arguments <a name="optional-arguments"></a>
There is some optional arguments you can use when running add_product.py, these are:

-     --komplett

-     --proshop

-     --computersalg

-     --elgiganten

When using one or more of "domain" arguments, only the chosen domains gets added to records.json under the product name. 

<br/>

# Fakta scraper <a name="fakta-scraper"></a>
The Fakta scraper can scrape discounts from this week discounts. <br/>
**OBS: Fakta scraper can not run in Linux as it uses the Firefox webdriver which is a .exe file.**

## Scrape discounts <a name="scrape-discounts"></a>
For now you can only search for keywords and get the discounts that match the keywords.
To scrape for discounts about for example Kellogg products, you only have to add the keyword "Kellogg" as a argument when running the fakta_scraper.py script:

    python3 fakta_scraper.py kellogg

You can search for multiple keyword by just adding them as arguments, as such:

    python fakta_scraper.py <keyword_1> <keyword_2> <keyword_3>

The discounts is printed in the terminal.
