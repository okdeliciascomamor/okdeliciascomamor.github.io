"""
upload_drive.py
Faz upload das fotos e post PNG para o Google Drive da Ok Delicias com Amor.
Usa Playwright para abrir o browser com o perfil do Chrome (ja autenticado).
"""

import os, shutil, tempfile, time
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
FOTOS_DIR = os.path.join(BASE_DIR, "fotos")

# IDs das pastas no Drive
FOLDER_POSTS   = "1078tTdx3JS8A_diLAgzJgBjkbino2Rw_"   # Posts e Stories
FOLDER_FOTOS   = "1SoYN6nRZMtNqGeBOxJQEcTNKsAsqb5t8"   # Fotos do Produto

# Arquivos para upload
POSTS_FILES = [
    os.path.join(BASE_DIR, "post_maio17.png"),
]

FOTOS_FILES = [
    os.path.join(FOTOS_DIR, f)
    for f in sorted(os.listdir(FOTOS_DIR))
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

# Chrome user data dir (para reusar sessao existente)
CHROME_USER_DATA = r"C:\Users\nasci\AppData\Local\Google\Chrome\User Data"
# Copia para temp para evitar conflito com Chrome aberto
TEMP_PROFILE = os.path.join(tempfile.gettempdir(), "pw_drive_upload_profile")


def copy_profile():
    """Copia o perfil Default do Chrome para temp (evita lock)."""
    src = os.path.join(CHROME_USER_DATA, "Default")
    dst = os.path.join(TEMP_PROFILE, "Default")
    if os.path.exists(TEMP_PROFILE):
        shutil.rmtree(TEMP_PROFILE, ignore_errors=True)
    os.makedirs(TEMP_PROFILE, exist_ok=True)
    # Copia apenas os arquivos de sessao/cookies (rapido)
    files_to_copy = ["Cookies", "Cookies-journal", "Login Data",
                     "Login Data For Account", "Secure Preferences", "Preferences"]
    os.makedirs(dst, exist_ok=True)
    for fname in files_to_copy:
        src_f = os.path.join(src, fname)
        if os.path.exists(src_f):
            try:
                shutil.copy2(src_f, os.path.join(dst, fname))
            except Exception as e:
                print(f"  aviso: nao copiou {fname}: {e}")
    return TEMP_PROFILE


def upload_files_to_folder(page, folder_id, file_paths, folder_name):
    """Navega para a pasta do Drive e faz upload dos arquivos."""
    print(f"\nAbrindo pasta: {folder_name}")
    page.goto(f"https://drive.google.com/drive/folders/{folder_id}", wait_until="networkidle", timeout=30000)
    time.sleep(2)

    # Verifica se precisamos fazer login
    if "accounts.google.com" in page.url or "signin" in page.url.lower():
        print("  Aguardando login... Faca login no Google e pressione Enter aqui.")
        input("  [Enter para continuar apos login]")
        page.goto(f"https://drive.google.com/drive/folders/{folder_id}", wait_until="networkidle", timeout=30000)
        time.sleep(2)

    print(f"  Pasta aberta. Iniciando upload de {len(file_paths)} arquivo(s)...")

    # Encontra o input de upload via JavaScript
    # O Drive tem um input[type=file] escondido que aceita multiplos arquivos
    file_input = page.query_selector('input[type="file"]')

    if file_input is None:
        # Tenta acionar via New > File upload
        print("  Buscando botao 'Novo'...")
        # Clica em "Novo" (New button)
        new_btn = page.query_selector('[data-tooltip="Novo"]') or \
                  page.query_selector('button[aria-label*="Novo"]') or \
                  page.query_selector('[aria-label="Novo"]')

        if new_btn:
            new_btn.click()
            time.sleep(1)
            # Clica em "Fazer upload de arquivo"
            upload_item = page.query_selector('[data-tooltip*="arquivo"]') or \
                          page.query_selector('[aria-label*="arquivo"]')
            if upload_item:
                upload_item.click()
                time.sleep(1)

        file_input = page.query_selector('input[type="file"]')

    if file_input is None:
        # Tenta via drag-and-drop area
        print("  Input de arquivo nao encontrado. Tentando via JavaScript...")
        # Injeta input temporario
        file_input = page.evaluate_handle("""() => {
            const input = document.createElement('input');
            input.type = 'file';
            input.multiple = true;
            input.style.display = 'none';
            document.body.appendChild(input);
            return input;
        }""")

    if file_input:
        # Faz upload em lotes de 5 arquivos para nao sobrecarregar
        BATCH = 5
        for i in range(0, len(file_paths), BATCH):
            batch = [f for f in file_paths[i:i+BATCH] if os.path.exists(f)]
            if not batch:
                continue
            print(f"  Enviando lote {i//BATCH + 1}: {[os.path.basename(f) for f in batch]}")
            file_input.set_input_files(batch)
            # Aguarda upload completar (espera os spinners sumirem)
            time.sleep(3)
            # Aguarda ate 60s pelo upload completar
            try:
                page.wait_for_selector('[data-tooltip*="Upload concluido"]', timeout=60000)
            except:
                try:
                    page.wait_for_function(
                        "() => !document.querySelector('.upload-status-bar')",
                        timeout=60000
                    )
                except:
                    pass
            time.sleep(2)
        print(f"  Upload concluido para: {folder_name}")
    else:
        print(f"  ERRO: Nao foi possivel encontrar o input de upload.")
        print(f"  Arquivos para upload manual: {[os.path.basename(f) for f in file_paths]}")


def main():
    print("=== Upload Drive - Ok Delicias com Amor ===")
    print(f"Posts a enviar: {len(POSTS_FILES)} arquivo(s)")
    print(f"Fotos a enviar: {len(FOTOS_FILES)} arquivo(s)")
    print()

    # Copia perfil Chrome para temp
    print("Copiando perfil Chrome (para autenticacao)...")
    try:
        profile_dir = copy_profile()
        print(f"  Perfil copiado para: {profile_dir}")
    except Exception as e:
        print(f"  Aviso: nao copiou perfil ({e}). Abrindo browser sem sessao.")
        profile_dir = None

    with sync_playwright() as p:
        if profile_dir:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=profile_dir,
                headless=False,
                args=["--no-first-run", "--no-default-browser-check", "--disable-blink-features=AutomationControlled"],
                slow_mo=200,
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
        else:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()

        page.set_viewport_size({"width": 1280, "height": 900})

        # Upload dos posts
        if POSTS_FILES:
            upload_files_to_folder(page, FOLDER_POSTS, POSTS_FILES, "Posts e Stories")

        # Upload das fotos
        if FOTOS_FILES:
            upload_files_to_folder(page, FOLDER_FOTOS, FOTOS_FILES, "Fotos do Produto")

        print("\n=== Upload concluido! ===")
        print("Pode fechar o browser.")
        time.sleep(5)

        if profile_dir:
            ctx.close()
        else:
            browser.close()

    # Limpa temp
    if profile_dir and os.path.exists(TEMP_PROFILE):
        shutil.rmtree(TEMP_PROFILE, ignore_errors=True)


if __name__ == "__main__":
    main()
