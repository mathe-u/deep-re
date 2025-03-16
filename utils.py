"""Utils."""

import csv
import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from exceptions import SaveCSVFileException

BASE_URL = "https://scholar.google.com.br"

def get_results(query, start_year=2021, results_per_page=10, max_results=30):
    """Get all possible results from Google Scholar."""
    results = []
    start = 0
    total_fetched = 0

    while total_fetched < max_results:
        url = BASE_URL
        url += f"/scholar?hl=pt-BR&as_sdt=0%2C5&as_ylo={start_year}&q={query}&start={start}&btnG="

        print(url)
        user_agent = UserAgent().random

        header = {
            'accept-language': 'en-US,en',
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'User-Agent': user_agent,
        }

        try:
            response = requests.get(url, headers=header, timeout=10)
            print("+---get response")
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            #print(soup.prettify())
            print("+---parse html")

            results_found = soup.find_all("h3", class_="gs_rt")
            print("+---get all tags")
            years_found = soup.find_all("div", class_="gs_a")
            print("+---get results(year):")
            # print(years_found)

            if not results_found:
                print(f"+---No more results found: {results_found}")
                break

            for i, result in enumerate(results_found):
                print(f"    +---loop{i}")
                a_tag = result.find("a")
                if a_tag:
                    title = a_tag.text
                    link = a_tag["href"]
                else:
                    title = result.find("span").text
                    link = ""
                    print("        +---else")
                print("        +---get all")

                year_text = years_found[i].text
                year = extract_year(year_text)

                result.append({"title": title, "year": year, "link": link})
                total_fetched += 1
                if total_fetched >= max_results:
                    break

                # time.sleep(random.randrange(1,3))
                print("    +---endLoop")

            start += results_per_page
            time.sleep(random.randrange(70, 120))

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o Google Acadêmico: {e}")
            break
        except AttributeError as e:
            print(f"Estrutura da página do Google Acadêmico alterada: {e}")
            break
        except TypeError:
            print("Erro ao coletar dados: {e}")

    return results

def extract_year(text):
    """Extract the year from the publication info text."""
    parts = text.split("-")
    if len(parts) > 1:
        try:
            return int(parts[-1].strip())
        except ValueError:
            return None
    return None

def save_data_csv(results, file_name="./data/data.csv"):
    """Save results of google in csv file."""
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as csv_file:
            fields = ["title", "year", "link"]
            writer_csv = csv.DictWriter(csv_file, fieldnames=fields)
            writer_csv.writeheader()
            writer_csv.writerows(results)
        print(f"Resultados salvos em '{file_name}' com sucesso!")
    except SaveCSVFileException as e:
        print(e)
