import time
import json
from pynput import mouse, keyboard
import pyautogui

# --- Configurações ---
RECORDING_FILE = 'macro_actions.json'
STOP_KEY = keyboard.Key.esc

# --- Variáveis Globais ---
is_recording = True
recorded_actions = []
start_time = 0


# --- Funções de Gravação (Listeners) ---

def get_key_str(key):
    """Converte uma tecla do pynput para uma string consistente."""
    if hasattr(key, 'char') and key.char is not None:
        return key.char
    elif hasattr(key, 'name'):
        return key.name
    else:
        return str(key)

def on_press(key):
    """Callback chamado quando uma tecla é pressionada."""
    if is_recording:
        action = {
            'action': 'key_press',
            'key': get_key_str(key),
            'time': time.time() - start_time
        }
        recorded_actions.append(action)
        print(f"Ação gravada: Pressionado '{get_key_str(key)}'")

# --- MUDANÇA 1: Adicionada a função on_release ---
def on_release(key):
    """Callback chamado quando uma tecla é solta."""
    global is_recording

    if key == STOP_KEY:
        print("Sinal de parada recebido... finalizando.")
        is_recording = False
        return False  # Para o listener do teclado

    if is_recording:
        action = {
            'action': 'key_release',
            'key': get_key_str(key),
            'time': time.time() - start_time
        }
        recorded_actions.append(action)
        print(f"Ação gravada: Solto '{get_key_str(key)}'")

def on_click(x, y, button, pressed):
    """Callback chamado quando o mouse é clicado."""
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

    recorded_actions = []
    is_recording = True
    
    # --- MUDANÇA AQUI ---
    print("Prepare-se! A gravação começará em 3 segundos...")
    time.sleep(3)
    # --- FIM DA MUDANÇA ---

    start_time = time.time()
    pyautogui.FAILSAFE = False

    # --- MUDANÇA 2: Listener do teclado agora escuta on_release também ---
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)
    
    keyboard_listener.start()
    mouse_listener.start()

    print("--- GRAVAÇÃO INICIADA ---")
    print(f"Realize as ações que deseja gravar. Pressione a tecla '{get_key_str(STOP_KEY)}' para parar.")

    while is_recording:
        time.sleep(0.1)

    mouse_listener.stop()
    print("Listeners parados.")

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
    print(f"Executando {len(actions)} ações. Para parar forçadamente, mova o mouse para o canto superior esquerdo.")
    
    pyautogui.FAILSAFE = True
    last_action_time = 0
    
    key_map = {
        'cmd': 'win',
        'ctrl_l': 'ctrl', 'ctrl_r': 'ctrl',
        'alt_l': 'alt', 'alt_r': 'alt',
        'shift_l': 'shift', 'shift_r': 'shift',
    }

    # --- MUDANÇA AQUI: Dicionário para códigos de controle do CTRL ---
    # Mapeia códigos de controle (gerados com Ctrl) de volta para suas letras.
    # \u0001 é Ctrl+A, \u0002 é Ctrl+B, \u0006 é Ctrl+F, etc.
    ctrl_char_map = {chr(i): chr(i + 96) for i in range(1, 27)}

    for action in actions:
        delay = action['time'] - last_action_time
        time.sleep(delay)

        action_type = action.get('action')

        if action_type == 'mouse_click':
            print(f"Executando: Clique em ({action['x']}, {action['y']})")
            pyautogui.click(x=action['x'], y=action['y'], button=action['button'].split('.')[-1])
        
        elif action_type in ['key_press', 'key_release']:
            key = action['key']
            
            # --- MUDANÇA AQUI: Traduz o código de controle de volta para uma letra ---
            # Se a tecla for um dos códigos especiais, converte. Senão, usa o mapeamento normal.
            if key in ctrl_char_map:
                mapped_key = ctrl_char_map[key]
            else:
                mapped_key = key_map.get(key, key)

            if action_type == 'key_press':
                pyautogui.keyDown(mapped_key)
                print(f"Executando: Pressionando '{mapped_key}'")
            elif action_type == 'key_release':
                pyautogui.keyUp(mapped_key)
                print(f"Executando: Soltando '{mapped_key}'")

        last_action_time = action['time']

    print("--- EXECUÇÃO FINALIZADA ---")


# --- Menu Principal (sem alterações) ---
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