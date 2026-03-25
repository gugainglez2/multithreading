# O IMDB não quis me dar as informações, então fiz um outro script para realizar o exercício mirando em um site menos rigoroso
# (Erro ao acessar lista principal: Status 202)
# movies_ebac.csv: "Titulo,Nota,Link" (Só o cabeçalho)

import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

MAX_THREADS = 10

def extract_movie_details(movie_link):
    time.sleep(random.uniform(0.2, 0.6))
    try:
        response = requests.get(movie_link, headers=headers, timeout=10)
        movie_soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = movie_soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else "N/A"

        rating_tag = movie_soup.find('span', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        
        if not rating_tag:
            rating_tag = movie_soup.find('span', class_=lambda x: x and 'cCwtqy' in x)
            
        rating = rating_tag.get_text().split('/')[0] if rating_tag else "N/A"

        if title != "N/A":
            with open('movies_ebac.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([title, rating, movie_link])
                print(f"Sucesso: {title} | Nota: {rating}")
        else:
            print(f"Aviso: Não consegui extrair dados de {movie_link}")

    except Exception as e:
        print(f"Erro na conexão: {e}")

def main():
    start_time = time.time()
    
    url = 'https://www.imdb.com/chart/moviemeter/'
    session = requests.Session()
    res = session.get(url, headers=headers, timeout=15)
    
    if res.status_code != 200:
        print(f"Erro ao acessar lista principal: Status {res.status_code}")
        return

    soup = BeautifulSoup(res.content, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/title/tt' in href and '/?ref_' in href:
            full_link = 'https://www.imdb.com' + href.split('?')[0]
            if full_link not in links:
                links.append(full_link)
    
    movie_links = links[:20]
    print(f"Links encontrados: {len(movie_links)}")

    if not movie_links:
        print("Nenhum link foi encontrado. O IMDb mudou a estrutura novamente.")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(extract_movie_details, movie_links)

    print(f"\n--- Total de tempo: {time.time() - start_time:.2f} segundos ---")

if __name__ == '__main__':
    with open('movies_ebac.csv', mode='w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['Titulo', 'Nota', 'Link'])
    
    main()