import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- Suas Informações Pessoais ---
MEU_CPF_NUMEROS = "60517796392"
MEU_CPF_FORMATADO = "605177963-92"
MINHA_DATA_NASCIMENTO = "16121994"
# ---------------------------------

def preencher_vaga(driver):
    """
    Função que executa o preenchimento dos formulários para uma única vaga.
    """
    try:
        print(f"Iniciando preenchimento para a vaga: {driver.title}")

        # --- TELA 1: Como ficou sabendo ---
        print("Preenchendo 'Como você ficou sabendo sobre nós?'...")
        wait = WebDriverWait(driver, 10)
        como_soube_input = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-automation-id='source']")))
        como_soube_input.send_keys("carreira")
        time.sleep(1) # Pequena pausa para o site processar
        como_soube_input.send_keys(Keys.ENTER)
        
        salvar_continuar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='bottom-navigation-next-button']")))
        salvar_continuar_btn.click()

        # --- TELA 2: Minha Experiência ---
        print("Avançando na tela de Experiência Profissional...")
        # Apenas clica em "Salvar e continuar", pois já está preenchido
        salvar_continuar_btn_exp = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='bottom-navigation-next-button']")))
        salvar_continuar_btn_exp.click()

        # --- TELA 3: Perguntas da candidatura ---
        print("Preenchendo perguntas (PCD e CPF)...")
        # Espera pelo campo de CPF para garantir que a página carregou
        cpf_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@data-automation-id='nationalId']")))
        
        # Clica em 'Não' para a pergunta sobre deficiência
        nao_pcd_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Não']")))
        nao_pcd_radio.click()

        cpf_input.send_keys(MEU_CPF_NUMEROS)

        salvar_continuar_btn_perg = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='bottom-navigation-next-button']")))
        salvar_continuar_btn_perg.click()
        
        # --- TELA 4: Informações Pessoais ---
        print("Preenchendo informações pessoais...")
        data_nascimento_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@data-automation-id='dateOfBirth']")))
        data_nascimento_input.send_keys(MINHA_DATA_NASCIMENTO)
        data_nascimento_input.send_keys(Keys.TAB, Keys.TAB)
        
        time.sleep(0.5) # Pausa para o preenchimento automático
        driver.switch_to.active_element.send_keys("BRA")
        driver.switch_to.active_element.send_keys(Keys.TAB)

        time.sleep(0.5)
        driver.switch_to.active_element.send_keys("CE", Keys.ENTER)
        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB)
        
        time.sleep(0.5)
        driver.switch_to.active_element.send_keys("B")
        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB)

        time.sleep(0.5)
        driver.switch_to.active_element.send_keys("BRA")
        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB)
        
        time.sleep(0.5)
        driver.switch_to.active_element.send_keys("M")
        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB)

        time.sleep(0.5)
        driver.switch_to.active_element.send_keys(Keys.SPACE) # Marca o checkbox de termos
        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB)
        
        time.sleep(0.5)
        driver.switch_to.active_element.send_keys(Keys.SPACE) # Clica em Salvar e Continuar

        # --- TELA 5: Revisar e Enviar ---
        print("Revisando e enviando a candidatura...")
        enviar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='bottom-navigation-next-button']")))
        enviar_btn.click()

        # --- TELA 6: Tarefas Pendentes ---
        print("Iniciando tarefa de alteração de identificadores...")
        iniciar_tarefa_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Iniciar']")))
        iniciar_tarefa_btn.click()

        # --- TELA 7: Preencher CPF novamente ---
        print("Preenchendo CPF novamente...")
        novo_id_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@data-automation-id='textInput-governmentId']")))
        novo_id_input.send_keys(MEU_CPF_FORMATADO)

        enviar_final_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='submitButton']")))
        enviar_final_btn.click()
        
        print(f"Candidatura para a vaga '{driver.title}' enviada com SUCESSO!")
        return True

    except (NoSuchElementException, TimeoutException) as e:
        print(f"ERRO: Não foi possível encontrar um elemento na página '{driver.title}'. O site pode ter mudado.")
        print(f"Detalhe do erro: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado na vaga '{driver.title}': {e}")
        return False

# --- LÓGICA PRINCIPAL ---
if __name__ == "__main__":
    # Configura o Selenium para se conectar ao Chrome já aberto
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)

    # Guarda a aba original para voltar no final
    aba_original = driver.current_window_handle
    todas_as_abas = driver.window_handles

    print(f"Encontradas {len(todas_as_abas)} abas abertas. Verificando vagas...")

    for aba in todas_as_abas:
        driver.switch_to.window(aba)
        url_atual = driver.current_url
        print(f"\nAnalisando URL: {url_atual}")

        # Verifica se a URL é de uma página de vaga do Santander
        if "santander.wd3.myworkdayjobs.com" in url_atual and "/job/" in url_atual:
            preencher_vaga(driver)
            time.sleep(3) # Pausa para você ver o resultado antes de ir para a próxima
        else:
            print("Esta aba não é uma vaga do Santander. Pulando.")
    
    # Volta para a aba onde o script começou
    driver.switch_to.window(aba_original)
    print("\nProcesso finalizado. Todas as abas foram verificadas.")