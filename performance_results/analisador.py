import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def process_csv_and_plot(file_path):
    # Inicializa variáveis para armazenar resultados
    distances_with_paths = []
    city_counter = Counter()
    
    # Lê o arquivo CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Obtém a distância e o caminho
            distance = float(row['Best Distance'])
            path = row['Best Path'].split(" -> ")
            
            # Atualiza o contador de cidades
            city_counter.update(path)
            
            # Armazena a distância e o caminho
            distances_with_paths.append((distance, path))
    
    # Ordena as distâncias para facilitar a análise
    distances_with_paths.sort(key=lambda x: x[0])
    
    # Calcula menor, maior e mediana das distâncias
    distances = [d[0] for d in distances_with_paths]
    min_distance = distances[0]
    max_distance = distances[-1]
    median_distance = np.median(distances)
    
    # Gera gráficos
    plt.figure(figsize=(8, 6))
    
    # Gráfico de barras: Menor, Maior e Mediana
    labels = ['Menor Distância', 'Maior Distância', 'Mediana']
    values = [min_distance, max_distance, median_distance]
    plt.bar(labels, values, color=['green', 'red', 'blue'])
    plt.title('Análise de Distâncias')
    plt.ylabel('Distância')
    plt.xlabel('Categorias')
    
    # Exibe o gráfico
    plt.tight_layout()
    plt.show()
    
    return distances_with_paths
def process_csv_with_plots(file_path):
    # Inicializa variáveis para armazenar resultados
    min_distance = float('inf')
    max_distance = float('-inf')
    min_distance_path = []
    max_distance_path = []
    city_counter = Counter()
    run_distances = []
    run_labels = []
    
    # Lê o arquivo CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Obtém a distância e o caminho
            distance = float(row['Best Distance'])
            path = row['Best Path'].split(" -> ")
            
            # Atualiza o contador de cidades
            city_counter.update(path)
            
            # Adiciona informações para o gráfico de linhas
            run_distances.append(distance)
            run_labels.append(row['Run'])
            
            # Verifica menor distância
            if distance < min_distance:
                min_distance = distance
                min_distance_path = path
            
            # Verifica maior distância
            if distance > max_distance:
                max_distance = distance
                max_distance_path = path
    
    # Cidade mais frequente
    most_common_city = city_counter.most_common(1)
    
    # Gera gráficos
    plt.figure(figsize=(12, 6))

    # Gráfico de barras: Contagem de cidades
    plt.subplot(1, 2, 1)
    cities, counts = zip(*city_counter.most_common())
    plt.bar(cities, counts, color='skyblue')
    plt.title('Ocorrência de Cidades nas Rotas')
    plt.xlabel('Cidades')
    plt.ylabel('Ocorrências')
    plt.xticks(rotation=45, ha='right')
    
    # Gráfico de linha: Distâncias por execução
    plt.subplot(1, 2, 2)
    plt.plot(run_labels, run_distances, marker='o', color='green', linestyle='--')
    plt.title('Distâncias por Execução')
    plt.xlabel('Execução (Run)')
    plt.ylabel('Distância')
    plt.xticks(rotation=45)
    
    # Ajusta layout e exibe
    plt.tight_layout()
    plt.show()
    
    return {
        "min_distance_path": min_distance_path,
        "max_distance_path": max_distance_path,
        "most_common_city": most_common_city[0] if most_common_city else None
    }
def process_csv(file_path):
    # Inicializa variáveis para armazenar resultados
    min_distance = float('inf')
    max_distance = float('-inf')
    min_distance_path = []
    max_distance_path = []
    city_counter = Counter()
    
    # Lê o arquivo CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Obtém a distância e o caminho
            distance = float(row['Best Distance'])
            path = row['Best Path'].split(" -> ")
            
            # Atualiza o contador de cidades
            city_counter.update(path)
            
            # Verifica menor distância
            if distance < min_distance:
                min_distance = distance
                min_distance_path = path
            
            # Verifica maior distância
            if distance > max_distance:
                max_distance = distance
                max_distance_path = path
    
    # Cidade mais frequente
    most_common_city = city_counter.most_common(1)
    
    return {
        "min_distance_path": min_distance_path,
        "max_distance_path": max_distance_path,
        "most_common_city": most_common_city[0] if most_common_city else None
    }
def process_and_filter_csv(file_path):
    # Inicializa variáveis para armazenar resultados
    unique_paths = {}
    city_counter = Counter()
    
    # Lê o arquivo CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Obtém a distância e o caminho
            distance = float(row['Best Distance'])
            path = tuple(row['Best Path'].split(" -> "))  # Usar tuple para garantir unicidade
            
            # Adiciona ao dicionário de caminhos únicos
            if path not in unique_paths:
                unique_paths[path] = distance
            
            # Atualiza o contador de cidades
            city_counter.update(path)
    
    # Ordena os caminhos únicos por distância
    sorted_paths = sorted(unique_paths.items(), key=lambda x: x[1])
    
    # Obtém menor e maior distância
    min_distance, min_path = sorted_paths[0]
    max_distance, max_path = sorted_paths[-1]
    
    # Obtém as cidades mais frequentes
    most_common_city_count = city_counter.most_common(1)
    if most_common_city_count:
        most_common_city, count = most_common_city_count[0]
        cities_with_count = [city for city, _ in city_counter.most_common() if city_counter[city] == count]
    else:
        most_common_city = count = 0
        cities_with_count = []
    
    # Retorno no formato desejado
    result = [
        {"menor Distancia": min_distance, "lista": list(min_path)},
        {"maior Distancia": max_distance, "lista": list(max_path)},
        {"lista de cidades que mais repete": count, "lista": cities_with_count}
    ]
    
    return result

def process_and_filter_csv_fixed(file_path):
    # Inicializa variáveis para armazenar resultados
    unique_paths = {}
    city_counter = Counter()
    
    # Lê o arquivo CSV
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            # Obtém a distância e o caminho
            distance = float(row['Best Distance'])
            path = tuple(row['Best Path'].split(" -> "))  # Usar tuple para garantir unicidade
            
            # Adiciona ao dicionário de caminhos únicos
            if path not in unique_paths:
                unique_paths[path] = distance
            
            # Atualiza o contador de cidades
            city_counter.update(path)
    
    # Ordena os caminhos únicos por distância
    sorted_paths = sorted(unique_paths.items(), key=lambda x: x[1])  # Lista de (path, distance)
    
    # Obtém menor e maior distância
    min_path, min_distance = sorted_paths[0]
    max_path, max_distance = sorted_paths[-1]
    
    # Obtém as cidades mais frequentes
    most_common_city_count = city_counter.most_common(1)
    if most_common_city_count:
        most_common_city, count = most_common_city_count[0]
        cities_with_count = [city for city, freq in city_counter.most_common() if freq == count]
    else:
        most_common_city = count = 0
        cities_with_count = []
    
    # Retorno no formato desejado
    result = [
        {"menor Distancia": min_distance, "lista": list(min_path)},
        {"maior Distancia": max_distance, "lista": list(max_path)},
        {"lista de cidades que mais repete": count, "lista": cities_with_count}
    ]
    
    return result


# Caminho para salvar e testar o arquivo CSV
csv_file_path = 'ga_results_tournment.csv'


# Processa o arquivo e retorna o resultado filtrado com a lógica corrigida
filtered_results_fixed = process_and_filter_csv_fixed(csv_file_path)
print(filtered_results_fixed)