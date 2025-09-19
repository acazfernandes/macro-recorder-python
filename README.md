# Gravador de Macros em Python

Um simples gravador e reprodutor de macros de teclado e mouse, construído em Python para automatizar tarefas simples e repetitivas.

## Funcionalidades

- Gravação de cliques do mouse e digitação do teclado.
- Salvamento da sequência de ações em um arquivo JSON.
- Reprodução fiel das ações gravadas.

## Pré-requisitos

- Python 3.x

## Instalação

1. Clone este repositório.
2. Navegue até a pasta do projeto e crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   ```bash
   # Windows
   .\.venv\Scripts\activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

1. Execute o script principal:
   ```bash
   python macro_recorder.py
   ```
2. Siga as instruções no menu para gravar ou executar uma macro.
3. Para parar uma gravação, pressione a tecla `Esc`ou mecha o mouse várias vezes.