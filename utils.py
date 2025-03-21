"""Utils."""
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
from extract import extract_year, extract_about
from save_data import save_data_csv
from search_pubs import search_pubs



def get_results(
        query,
        start_year=2021,
        results_per_page=10,
        max_results=400,
        file_name="./data/results_tcc_1.csv",
    ):
    """Get all possible results from Google Scholar."""
    results = []
    start = 0
    total_fetched = 0

    service = Service()
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=options)
    # driver.get(BASE_URL)

    # search_box = driver.find_element(By.NAME, "q")
    # time.sleep(2)
    # search_box.send_keys("demência and idosos and aplicativo movel")
    # time.sleep(3)
    # search_box.submit()
    # time.sleep(40)
    flag = True

    while total_fetched < max_results:
        # url += f"/scholar?hl=pt-BR&as_sdt=0%2C5&as_ylo={start_year}&q={query}&start={start}&btnG="
        url = search_pubs(query=query, year_start=start_year, start_index=start)

        print(url)
        # user_agent = UserAgent().random

        # header = {
        #     'accept-language': 'en-US,en',
        #     'accept': 'text/html,application/xhtml+xml,application/xml',
        #     'User-Agent': user_agent,
        # }

        try:
            driver.get(f"https://scholar.google.com.br/{url}")
            if flag:
                input()
                flag = False

            soup = BeautifulSoup(driver.page_source, "html.parser")
            # .replace(u'\xa0', u' ')

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
                print(f"extracted year: {year}")
                more_info = extract_about(about_text)
                print(f"extracted authors: {more_info}")

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
            save_data_csv(results=results, file_name=file_name)
            time.sleep(random.randrange(13, 17))

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o Google Acadêmico: {e}")
            break
        except AttributeError as e:
            print(f"Estrutura da página do Google Acadêmico alterada: {e}")
            break
        except TypeError as e:
            print(f"Erro ao coletar dados: {e}")
