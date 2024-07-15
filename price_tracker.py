from bs4 import BeautifulSoup
import requests
import smtplib
import os

EMAIL = os.environ.get("EMAIL")
PASSWORD =  os.environ.get("EMAIL_PASSWORD")
SMTP_ADDRESS = os.environ.get("SMTP_ADDRESS")

# Headers to add the to Request
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", 
    "Accept-Language":"en-US",
    "Cookie":"PHPSESSID=079647f315e0f8ebad4dbaa9c867eb1b; _ga=GA1.2.1166026948.1721076667; _gid=GA1.2.129755154.1721076667; _ga_VL41109FEB=GS1.2.1721076668.1.0.1721076668.0.0.0",
}

# Site Link
book_url = "https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1098125975/ref=pd_bxgy_d_sccl_1"
response = requests.get(book_url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
# Check you are getting the actual Amazon page back and not something else
print(soup.prettify())

# Find the HTML element that contains the price
price_element = soup.find(class_="aok-offscreen").get_text()
price = price_element.split()[0]
print(price)

# Remove the dollar sign using split
price_without_currency = price.split("$")[1]

# Convert string to floating point number
price_as_float = float(price_without_currency)
print(price_as_float)


# Get the product title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Set the price below which you would like to get a notification
BUY_PRICE = 50.00

# ====================== Send an Email ===========================
if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"
    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            result = connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:Amazon Book Price Alert!\n\n{message}\n{book_url}".encode("utf-8")
            )
    except Exception as e:
        print(f"Error: {e}")