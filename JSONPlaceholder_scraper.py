import requests
import time
import csv
import concurrent.futures

BASE_URL = 'https://jsonplaceholder.typicode.com/posts/'
MAX_THREADS = 10

def extract_details(post_id):
    time.sleep(0.1)

    try:
        url = f"{BASE_URL}{post_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', 'N/A')
            user_id = data.get('userId', 'N/A')
            
            with open('exercicio_ebac.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([post_id, title, user_id])
                print(f"Sucesso: ID {post_id} capturado.")
        else:
            print(f"Erro no ID {post_id}: Status {response.status_code}")

    except Exception as e:
        print(f"Falha: {e}")

def main():
    start_time = time.time()
    post_ids = list(range(1, 51))
    print(f"Iniciando processamento de {len(post_ids)} itens...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(extract_details, post_ids)

    print(f"\n--- Tempo Total: {time.time() - start_time:.2f} segundos ---")

if __name__ == '__main__':
    with open('exercicio_ebac.csv', mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['ID', 'Titulo_Post', 'ID_Usuario'])
    
    main()