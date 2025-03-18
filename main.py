"""Get all results google scholar and put in csv file"""

from utils import get_results

# Exemplo de uso
if __name__ == "__main__":
    QUERY = "dashboard and analise and dados and demência idosos"
    get_results(QUERY)
