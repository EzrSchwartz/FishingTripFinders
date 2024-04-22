#https://www.aveloair.com/flight-search/deeplink/searchflights/roundtrip/HVN/TPA/leaving year-leaving month-leaving day/returning year-returning month-returning day/2/0/0/0/?calendar=false
#Strucutre link to find flights
#element id is fare-price



from timestamp import timestamps
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
from dateutil.relativedelta import relativedelta
import smtplib
import pandas as pd
import numpy as np


nametext = []
departingflightstext = []
returningflightstext = []
pricetext = []

# Set the number of days for the stay
days = int(input("How long will you stay: "))  # Convert the input to an integer

# Get the current date
now = datetime.now()

# Calculate the check-in date (2 days after the current date)
checkin_date = now + relativedelta(days=2)

# Calculate the check-out date
checkout_date = checkin_date + relativedelta(days=days)

# Setup
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))


driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Navigate to the website
driver.get(f'https://www.satorealestate.com/vacation-rentals/results/?searchform=1&arrive_date={checkin_date.month}%2F{checkin_date.day}%2F{checkin_date.year}&depart_date={checkout_date.month}%2F{checkout_date.day}%2F{checkout_date.year}&cwrsearch=1&Bedrooms=2')



links = []
# Wait for the JavaScript to load
driver.implicitly_wait(2)



# Find the elements with the class 'boxprice'
prices = driver.find_elements(By.CSS_SELECTOR, '.boxprice')

names = driver.find_elements(By.CSS_SELECTOR, '.title')
names.pop(0)

print(len(names))


for price in prices:
    pricetext.append(price.text)

for name in names:
    nametext.append(name.text)


for name in nametext:
    links.append(f'https://www.satorealestate.com/vacation-rentals/rental/{name.replace(" ","-")}')

for link in links:
    print(link)
d = {'Names': nametext,'Prices': pricetext, 'Link': links}


df = pd.DataFrame(columns=[ 'Arrival Date', 'Departure Date', 'ID','Names','Rental Price','Link','Plane Price'])

df["Names"] = nametext
df["Price"] = pricetext
df["Links"] = links

# Print the text of each element
print(df)



# Close the driver
driver.quit()
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))


driver.get(f'https://www.aveloair.com/flight-search/deeplink/searchflights/roundtrip/HVN/TPA/{checkin_date}/{checkout_date}/2/0/0/0/?calendar=false')


driver.implicitly_wait(2)

flightselector = driver.find_elements(By.CSS_SELECTOR, '.flight-selector')
for outer_div in flightselector:
    print((outer_div.find_element(By.CSS_SELECTOR, '.route-label')).text)
    if(  "Depart:" == (outer_div.find_element(By.CSS_SELECTOR, '.route-label').text)):
        departingflights = outer_div.find_elements(By.CSS_SELECTOR, '.btn-fare-wheel')



        for flight in departingflights:
            if (str(checkout_date).replace("-","/") == flight.find_element(By.CSS_SELECTOR, '.id').text):
                if((flight.find_element(By.CSS_SELECTOR, '.fare-price').text).find("Sold")):
                    departingflightstext.append(flight.find_element(By.CSS_SELECTOR, '.fare-price').text)

        print(departingflightstext)
df["Plane Price"] = min(departingflights)

df = df.assign(industry='yyy')

# Set up the SMTP server and log into your account
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login("fishingtripfinder@outlook.com", "PWD!23")


sendingemail = "fishingtripfinder@outlook.com"

recievingemails = ["ezra.n.schwartz@gmail.com"]

dfstring = df.to_string(index=False)

# Create the message
msg = """\
Subject: Hello, here are the bookings avalible


"""+dfstring



server.sendmail(sendingemail, recievingemails, msg)

# Close the connection to the server
server.quit()

