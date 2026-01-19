import re
import csv
from collections import Counter
from itertools import combinations

ARQUIVO_ROTEIRO = 'roteiro_avengers_endgame.txt'
ARQUIVO_SAIDA = 'rede_vingadores_final.csv'

# dicionario pra unificar nomes
SINONIMOS = {
    'TONY STARK': 'TONY',
    'STEVE ROGERS': 'STEVE',
    'NATASHA ROMANOV': 'NATASHA',
    'CLINT BARTON': 'CLINT',
    'BRUCE BANNER': 'BANNER',
    'SMART HULK': 'BANNER',
    'PETER PARKER': 'PETER',
    'CAROL DANVERS': 'CAPTAIN MARVEL',
    'SCOTT LANG': 'SCOTT'
}

# termos técnicos pra ignorar
IGNORAR = ['INT', 'EXT', 'DAY', 'NIGHT', 'CONTINUED', 'CONT\'D', 'O.S.', 'FLASHBACK', 'TITLE']

def limpar_nome(nome):
    nome = nome.strip().upper()
    # remove sufixos como (O.S.) ou (CONT'D)
    nome = re.sub(r'\(.*\)', '', nome).strip()
    return SINONIMOS.get(nome, nome)

def extrair_rede():
    try:
        with open(ARQUIVO_ROTEIRO, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo {ARQUIVO_ROTEIRO} não foi encontrado.")
        return

    # dividi por cenas usando INT. ou EXT. como separadores
    cenas = re.split(r'INT\.|EXT\.', conteudo)
    
    todas_conexoes = []
    
    print(f"Processando {len(cenas)} cenas...")

    for cena in cenas:
        # regex procura por nomes q aparecem antes dos diálogos, no caso MAIÚSCULOS
        candidatos = re.findall(r'\n\s*([A-Z]{3,}(?:\s[A-Z]+)*)\s*\n', cena)
        
        personagens_cena = set()
        for p in candidatos:
            nome_limpo = limpar_nome(p)
            if nome_limpo not in IGNORAR and len(nome_limpo) > 2:
                personagens_cena.add(nome_limpo)
        
        # cria conexoes, combinations('ABC', 2) -> AB, AC, BC
        lista_personagens = sorted(personagens_cena)
        if len(lista_personagens) > 1:
            pares = list(combinations(lista_personagens, 2))
            todas_conexoes.extend(pares)

    contagem = Counter(todas_conexoes)

    # exportar pra CSV
    with open(ARQUIVO_SAIDA, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Source', 'Target', 'Weight'])
        for (p1, p2), peso in contagem.items():
            writer.writerow([p1, p2, peso])

    print(f"Concluido! O arquivo '{ARQUIVO_SAIDA}' foi gerado com sucesso.")

if __name__ == "__main__":
    extrair_rede()
