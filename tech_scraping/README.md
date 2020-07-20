This program can scrape prices on products from Komplett.dk, Proshop.dk and Computersalg.dk

In the terminal, run:
1.     pip install -r requirements.txt
2.     python scraping.py

Before scraping a new product, run:

     python add_product.py
and follow instructions.

Then add this line in the last if-statement in scraping.py:

    {site}('{category}', '{link}')
e.g.

    Komplett('gpu', 'https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio')
OBS: make sure the category and product name has been created with add_product.py
