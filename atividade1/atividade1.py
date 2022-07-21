from separador import SeparadorUtils

# PROPN = Substantivo próprio
# NOUN = Substantivo comum
# VERB = Verbo
# PRON = Pronome
# ADV = Adverbios
# CCONJ = Conjunções

source = ''
while(source not in ('w', 'a') or source != 'q'):
  print('------ Separador de palavras - PT-BR ------')
  print('> Deseja buscar no Wikipedia (w) ou de arquivo (a), (q) para sair: ')
  source = input()

  content = ''
  if (source == 'w'):
    print('> Digite o nome da página do Wikipedia: ')
    page = input()
    content = SeparadorUtils.get_from_wikipedia(page)
  elif (source == 'a'):
    print('> Digite o nome do arquivo: ')
    filename = input()
    content = SeparadorUtils.get_from_file(filename)
  elif (source == 'q'):
    break
  else:
    print('Comando inválido')
    continue

  SeparadorUtils.process(content)
