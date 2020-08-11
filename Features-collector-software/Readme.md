### Programas e arquivos utilizados para obter as features empregadas nos métodos de aprendizado de máquina

Durante o projeto eu criei um programa em python para obter de forma automática os atributos necessários nos testes com a ferramenta WEKA. O arquivo ```counter.py``` recebe os léxicos de palavras de sentimento, de advérbios de intensidade e negação, de pontuação, de stopwords(se desejar utilizar), as sentenças do córpus e os arquivos RST das sentenças; e gera um arquivo ```atributos.csv``` contendo todos os atributos lexicais e discursivos.

As medidas de centralidade foram obtidas utilizando as ferramentas desenvolvidas no trabalho de Vilarinho e Ruiz (2018), citado nos artigos mencionados no ```Readme.md``` principal.