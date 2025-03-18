"""Utils."""

import csv
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
from exceptions import SaveCSVFileException
from extract import extract_year, extract_about



def get_results(query, start_year=2021, results_per_page=10, max_results=400):
    """Get all possible results from Google Scholar."""
    results = []
    base_url = "https://scholar.google.com.br"
    start = 0
    total_fetched = 0

    service = Service()
    driver = webdriver.Firefox(service=service)
    # driver.get(BASE_URL)

    # search_box = driver.find_element(By.NAME, "q")
    # time.sleep(2)
    # search_box.send_keys("demência and idosos and aplicativo movel")
    # time.sleep(3)
    # search_box.submit()
    # time.sleep(40)
    flag = True

    while total_fetched < max_results:
        url = base_url
        url += f"/scholar?hl=pt-BR&as_sdt=0%2C5&as_ylo={start_year}&q={query}&start={start}&btnG="

        print(url)
        # user_agent = UserAgent().random

        # header = {
        #     'accept-language': 'en-US,en',
        #     'accept': 'text/html,application/xhtml+xml,application/xml',
        #     'User-Agent': user_agent,
        # }

        try:
            driver.get(url)
            if flag:
                input()
                flag = False

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # print(soup.prettify())
            # input()


            results_found = soup.find_all("h3", class_="gs_rt")
            # print("+---get all tags")
            info_found = soup.find_all("div", class_="gs_a")
            # print("+---get results(year):")
            # print(years_found)

            if not results_found:
                print(f"+---No more results found: {results_found}")
                break

            for i, result in enumerate(results_found):
                a_tag = result.find("a")
                if a_tag:
                    title = a_tag.text
                    link = a_tag["href"]
                else:
                    title = result.get_text(strip=True)
                    link = ""
                    # print("        +---else")
                    print(title)
                # print("        +---get all")

                about_text = info_found[i].text
                # print("years found...")
                # print(about_text)
                # print("_"*20)
                year = extract_year(about_text)
                more_info = extract_about(about_text)
                # print(f"extracted year: {year}")
                # print(f"extracted authors: {authors}")

                results.append({
                    "title": title,
                    "year": year,
                    "more_info": more_info,
                    "link": link,
                    })
                total_fetched += 1
                if total_fetched >= max_results:
                    break

            start += results_per_page
            time.sleep(random.randrange(13, 22))

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o Google Acadêmico: {e}")
            break
        except AttributeError as e:
            print(f"Estrutura da página do Google Acadêmico alterada: {e}")
            break
        except TypeError as e:
            print(f"Erro ao coletar dados: {e}")

    return results

# def extract_year(text):
#     """Extract the year from the publication info text."""
#     parts = text.split("-")
#     print(parts)
#     if len(parts) > 1:
#         try:
#             return int(parts[-1].strip())
#         except ValueError:
#             return None
#     return None

def save_data_csv(results, file_name="./data/data.csv"):
    """Save results of google in csv file."""
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
            fields = [
                "title",
                "year",
                "more_info",
                "link",
            ]
            writer_csv = csv.DictWriter(csv_file, fieldnames=fields)
            writer_csv.writeheader()
            writer_csv.writerows(results)
        print(f"Resultados salvos em '{file_name}' com sucesso!")
    except SaveCSVFileException as e:
        print(e)
