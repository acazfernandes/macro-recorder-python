import time
import json
from pynput import mouse, keyboard
import pyautogui

# --- Configurações ---
RECORDING_FILE = 'macro_actions.json'
STOP_KEY = keyboard.Key.esc

# --- Variáveis Globais ---
# Usaremos esta variável para sinalizar quando parar
is_recording = True
# Lista para armazenar as ações gravadas
recorded_actions = []
start_time = 0


# --- Funções de Gravação (Listeners) ---

def on_press(key):
    """Callback chamado quando uma tecla é pressionada."""
    global is_recording

    # Se a tecla pressionada for a de parada, apenas sinaliza para parar.
    if key == STOP_KEY:
        print("Sinal de parada recebido...finalizando.")
        is_recording = False
        return False  # Retornar False para parar o listener do teclado

    # O resto da gravação só acontece se estivermos no modo de gravação
    if is_recording:
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        action = {
            'action': 'key_press',
            'key': key_char,
            'time': time.time() - start_time
        }
        recorded_actions.append(action)
        print(f"Ação gravada: Pressionado '{key_char}'")

def on_click(x, y, button, pressed):
    """Callback chamado quando o mouse é clicado."""
    # A gravação de cliques só acontece se estivermos no modo de gravação
    if is_recording and pressed:
        action = {
            'action': 'mouse_click',
            'x': x,
            'y': y,
            'button': str(button),
            'time': time.time() - start_time
        }
        recorded_actions.append(action)
        print(f"Ação gravada: Clique em ({x}, {y}) com o botão {button}")


# --- Funções Principais ---

def record_macro():
    """Inicia a gravação das ações do usuário."""
    global recorded_actions, is_recording, start_time

    # Reseta as variáveis para uma nova gravação
    recorded_actions = []
    is_recording = True
    start_time = time.time()
    pyautogui.FAILSAFE = False

    # Configura e inicia os listeners em segundo plano
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    
    keyboard_listener.start()
    mouse_listener.start()

    print("--- GRAVAÇÃO INICIADA ---")
    print(f"Realize as ações que deseja gravar. Pressione a tecla '{str(STOP_KEY)}' para parar.")

    # ****** ESTA É A MUDANÇA PRINCIPAL ******
    # Em vez de travar o programa com .join(), ficamos em um loop
    # esperando a variável is_recording se tornar False.
    while is_recording:
        time.sleep(0.1)

    # Quando o loop termina, paramos os listeners explicitamente.
    mouse_listener.stop()
    print("Listener do mouse parado.")

    # Salva as ações gravadas em um arquivo JSON
    with open(RECORDING_FILE, 'w') as f:
        json.dump(recorded_actions, f, indent=4)
    
    print(f"--- GRAVAÇÃO FINALIZADA ---")
    print(f"Macro salva em '{RECORDING_FILE}' com {len(recorded_actions)} ações.")


def play_macro():
    """Executa uma macro gravada a partir do arquivo."""
    try:
        with open(RECORDING_FILE, 'r') as f:
            actions = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo de macro '{RECORDING_FILE}' não encontrado. Grave uma macro primeiro.")
        return
    
    print(f"--- EXECUÇÃO INICIADA ---")
    print(f"Executando {len(actions)} ações. Para parar forçadamente, mova o mouse para o canto superior esquerdo da tela.")
    
    pyautogui.FAILSAFE = True
    last_action_time = 0

    for action in actions:
        delay = action['time'] - last_action_time
        time.sleep(delay)

        if action['action'] == 'mouse_click':
            print(f"Executando: Clique em ({action['x']}, {action['y']})")
            pyautogui.click(x=action['x'], y=action['y'], button=action['button'].split('.')[-1])
        
        elif action['action'] == 'key_press':
            key = action['key']
            if 'Key.' in key:
                # Converte 'Key.xxx' para 'xxx' em minúsculas
                pyautogui.press(key.split('.')[-1].lower())
                print(f"Executando: Pressionando tecla especial '{key}'")
            else:
                pyautogui.write(key)
                print(f"Executando: Escrevendo '{key}'")

        last_action_time = action['time']

    print("--- EXECUÇÃO FINALIZADA ---")


# --- Menu Principal ---
if __name__ == "__main__":
    while True:
        print("\nO que você deseja fazer?")
        print("1. Gravar nova macro")
        print("2. Executar a última macro gravada")
        print("3. Sair")
        choice = input("Escolha uma opção (1/2/3): ")

        if choice == '1':
            record_macro()
        elif choice == '2':
            play_macro()
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")