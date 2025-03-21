"""Get all results google scholar and put in csv file"""
import argparse
import datetime
from utils import get_results

# Exemplo de uso
if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    parser = argparse.ArgumentParser(description="Get all results google scholar.")

    parser.add_argument("search", help="Sua String de busca.")
    parser.add_argument(
        "-i",
        "--start-year",
        type=int,
        default=2021,
        help="Ano de inicio da busca."
    )
    parser.add_argument(
        "-f",
        "--file-name",
        type=str,
        default=f"./data/results-tcc-{now}.csv",
        help="Nome do arquivo.",
    )

    args = parser.parse_args()
    query = args.search
    year = args.start_year
    file = args.file_name
    # "dashboard and analise and dados and demência idosos"
    # "BI dashboard and analise and dados and diagnóstico and exames radiológicos"
    get_results(query=query, start_year=year, file_name=file)
