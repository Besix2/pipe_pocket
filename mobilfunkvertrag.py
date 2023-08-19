from operator import add
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import re 
import json
from tqdm import tqdm

# Cache expires after 1 hour

def scrape_with_selenium():
    url = "https://www.sparhandy.de/handy-vertrag/"
    driver = webdriver.Chrome("C:\Web_driver\chromedriver.exe")
    driver.get(url)

    wdwait = WebDriverWait(driver, 10)
    wdwait.until(EC.presence_of_element_located((By.ID, "usercentrics-root")))
    consentButton = driver.execute_script("function sleep(ms) { return new Promise(resolve => setTimeout(resolve, "
                                                "ms));} async function waitForConsent() {let consent;let tries = 20; "
                                                "while (!consent && tries > 0) {consent = document.querySelector("
                                                "'#usercentrics-root').shadowRoot.querySelector('[role=dialog] "
                                                "button');tries--;await sleep(500);} return consent;} return await waitForConsent()")
    consentButton.click()
    wdwait.until(EC.invisibility_of_element(consentButton))

    def wait_for_button():
        return WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Die nächsten 12 laden")]'))
        )

    while True:
        try:
            button = wait_for_button()
            button.click()
            # Add a pause to allow time for the new content to load
            time.sleep(3)
        except:
            print("abgebrochen")
            # If the button is no longer present or clickable, break the loop
            break

    page_source = driver.page_source
    driver.quit()
    return page_source



def soup_loader():
    soup = BeautifulSoup(scrape_with_selenium(), "html.parser")

    elements = soup.find("ul", class_="product-boxes product-boxes--device-with-tariff")
    link_list = []
    for i in elements:
        if i == "\n":
            continue

        name = i.find("a", class_="product-box-link")
        
        try: 
            link = name["href"]
            link_list.append(str(link))
            
        except Exception:
            pass
    return link_list
def phone_comparator():
    link_list = soup_loader()
    link_list = link_list[31:]
    for link in link_list:
        print(link)
        url = f"https://www.sparhandy.de{link}"
        driver = webdriver.Chrome("C:\Web_driver\chromedriver.exe")
        driver.get(url)
        wdwait = WebDriverWait(driver, 10)
        wdwait.until(EC.presence_of_element_located((By.ID, "usercentrics-root")))
        consentButton = driver.execute_script("function sleep(ms) { return new Promise(resolve => setTimeout(resolve, "
                                                "ms));} async function waitForConsent() {let consent;let tries = 20; "
                                                "while (!consent && tries > 0) {consent = document.querySelector("
                                                "'#usercentrics-root').shadowRoot.querySelector('[role=dialog] "
                                                "button');tries--;await sleep(500);} return consent;} return await waitForConsent()")

        consentButton.click()
        wdwait.until(EC.invisibility_of_element(consentButton))
        
        
        
    
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Die nächsten 6 laden")]')))
        while True:
            try:
                button.click()
                time.sleep(3)
            except:
                print("abgebrochen")
                break
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        phone_name = soup.find("span",itemprop="name", class_="device-name-text").string
        phone_name = phone_name.strip()
        print(phone_name)
        
        html_name = os.path.join("handys", f"{phone_name}.html")
        with open(html_name, "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))
        
def price_check():
    price_list = {}
    for root, dirs, files in os.walk("handys"):
        for file in files:
            file = file.replace(".html", "")
            file = re.sub(' +', ' ', file).strip()
            phone_name = file.replace("Refurbished", "")
            file = phone_name.replace(" ", "%20")
            base_url = f"https://www.zoxs.de/ankauf_suche.html?q={file}"
            driver = webdriver.Chrome("C:\Web_driver\chromedriver.exe")
            driver.get(base_url)
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAccept"]')))
            button.click()
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                elements_grid = soup.find("div", class_="row category-overview pt-4")
                
                for i in elements_grid:
                    if i == "\n":
                        continue
                    try:
                        name = i.find("div", class_="bottom")
                        name_string = name.find("span").text
                        if phone_name in name_string:
                            if phone_name in price_list:
                                break
                            sub_link_parent = i.find("a", class_="text-dark nav-link p-0 rounded offer-tile-klickarea")
                            sub_link = sub_link_parent["href"]
                            complete_link = f"https://www.zoxs.de/verkaufen/{sub_link}"
                            driver = webdriver.Chrome("C:\Web_driver\chromedriver.exe")
                            driver.get(complete_link)
                            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAccept"]')))
                            button.click()
                            page = driver.page_source
                            soup = BeautifulSoup(page, "html.parser")
                            price = soup.find("span", class_="hideinput").string
                            price_list[phone_name] = price
                    except Exception as error:
                        pass
                
            except Exception as error: 
                print(error)
        print(price_list)
        with open("preise.json", "w") as price_list_file:
            for key, value in price_list.items():
                value = value.replace("\xa0", "").replace("\u20ac", "€")
                price_list[key] = value
            json.dump(price_list, price_list_file)
            
            
def compare():
    last_volume = 0
    last_price = 100
    best_contract = ""
    directory_path = "handys"
    for filename in tqdm(os.listdir(directory_path), desc="Processing files"):
        if filename.endswith(".html"):  # Check if the file is an HTML file
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as html_file:
                html_content = html_file.read()
                soup = BeautifulSoup(html_content, "html.parser")
                contracts = soup.find_all("li", class_="product-list-item")
                phone_name = soup.find("span", {"class": "device-name-text", "data-acceptance-test": "device-name"}).text.strip()
                with open("preise.json", "r") as price_list_file:
                    resell_price_list = json.load(price_list_file)
                phone_resell_price = resell_price_list[phone_name]
                phone_resell_price = str(phone_resell_price).replace("€", "")
                phone_resell_price = str(phone_resell_price).replace(".", "")
                phone_resell_price = phone_resell_price.replace(",", ".")
                phone_resell_price = float(phone_resell_price)
                for contract in contracts:
                    if "magenta" in contract.find("span", class_="product-box-headline").text or "Congstar" in contract.find("span", class_="product-box-headline").text:
                        continue
                    
                    volume = contract.find("div", class_="product-usp-list-item-title").text
                    
                    element = contract.select_one("span.price-euro:not([data-behavior])")
                    if element is not None:
                        euro_monthly = element.get_text(strip=True)
                    else:
                        print("Element not found")

                    element_cent = contract.select_one("span.price-cent:not([data-behavior])")
                    if element_cent is not None:
                        cent_monthly = element_cent.get_text(strip=True)
                    else:
                        print("Element not found")

                    price_monthly = f"{euro_monthly},{cent_monthly}"
                    euro_onetime = contract.find("span", itemprop="price")
                    euro_onetime = euro_onetime.text.strip()
                    euro_onetime = re.sub(r'[^\d,.]', '', euro_onetime).replace(',', '.')
                    euro_onetime = float(euro_onetime)
                    additional_fees_element = contract.find("div", class_="price-item-additional").text
                    match = re.findall(r'\d+', additional_fees_element)
                    if match:
                        match.pop(0)
                        additional_fees = ','.join(match)
                    else:
                        print("Anschlusspreis not found")

                    price_monthly = price_monthly.replace("*", "")
                    price_monthly = price_monthly.replace(",", ".")
                    price_monthly = float(price_monthly)
                    # additional_fees = additional_fees.replace(",", ".")
                    # additional_fees = float(additional_fees)
                    # additional_fees =+ 10
                    additional_fees = 50
                    one_time_payment = euro_onetime + additional_fees
                    monthly_payment = 24 * price_monthly
                    Final_price = (one_time_payment + monthly_payment) - phone_resell_price
                    Final_price = Final_price / 24
                    if "Unlimitierte" in volume:
                        volume = 999
                    elif not re.search(r'\d+', volume):                                 #
                        continue
                    else:
                        volume_numbers = re.findall(r'\d+', volume)
                        volume = int(volume_numbers[0])
                        
                    if last_price > Final_price:
                        last_volume = volume
                        last_price = Final_price
                        best_contract = contract.find("a", class_="button button--call-to-action")["href"]
                        print(one_time_payment)
                        print(monthly_payment)
                        print(phone_resell_price)
                    # if volume > last_volume and Final_price < last_price:
                    #     last_volume = volume
                    #     last_price = Final_price
                    #     best_contract = contract.find("a", class_="button button--call-to-action")["href"]
    print(best_contract)
    print(last_price)
    


    
compare()
        
