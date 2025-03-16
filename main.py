"""Get all results google scholar and put in csv file"""

from utils import get_results, save_data_csv


# Exemplo de uso
QUERY = "dem%C3%AAncia+and+idosos+and+aplicativo+movel"
res = get_results(QUERY)

if res:
    save_data_csv(res)
else:
    print(f"Nenhum resultado encontrado: {res}")
