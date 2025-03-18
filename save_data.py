"""Save data"""
import csv
from exceptions import SaveCSVFileException

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
        print(f"Nenhum resultado encontrado: {e}")
