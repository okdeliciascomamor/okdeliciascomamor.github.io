"""
Upload de criativos para 02 - Posts e Stories no Google Drive
Usa o perfil real do Chrome (já logado no Google)
"""

import os, time
from playwright.sync_api import sync_playwright

BASE_DIR    = r"C:\Users\nasci\Documents\Kaempf Business\Jobs 2026\Ok - Delicias com Amor"
CHROME_PROFILE = r"C:\Users\nasci\AppData\Local\Google\Chrome\User Data"
FOLDER_URL  = "https://drive.google.com/drive/folders/1hglIvxzLp6KbsD9akWlAlBzS09bffkZK"

FILES = [
    os.path.join(BASE_DIR, "post_maio18.png"),
    os.path.join(BASE_DIR, "story_maio18_1.png"),
    os.path.join(BASE_DIR, "story_maio18_2.png"),
    os.path.join(BASE_DIR, "story_maio18_3.png"),
    os.path.join(BASE_DIR, "story_maio19_1.png"),
    os.path.join(BASE_DIR, "story_maio19_2.png"),
    os.path.join(BASE_DIR, "story_maio19_3.png"),
]

def main():
    print("Iniciando upload...")
    for f in FILES:
        if not os.path.exists(f):
            print(f"  ARQUIVO NAO ENCONTRADO: {f}")
            return

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            channel="chrome",
            headless=False,
            args=["--no-sandbox", "--profile-directory=Default"],
        )

        page = ctx.new_page()
        print(f"Navegando para a pasta...")
        page.goto(FOLDER_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)

        # Localiza o input de upload oculto que o Drive usa
        # Dispara via JS para não precisar abrir o dialog nativo
        print("Preparando upload via input oculto...")

        for filepath in FILES:
            filename = os.path.basename(filepath)
            print(f"  Enviando: {filename}")

            # Usa a API de upload oculto do Drive (input[type=file] oculto)
            file_input = page.locator("input[type=file]").first
            if file_input.count() == 0:
                # Tenta abrir o menu "Novo" para ativar o input
                new_btn = page.locator('[aria-label="Novo"]').first
                if new_btn.count() == 0:
                    new_btn = page.locator('button:has-text("Novo")').first
                new_btn.click()
                time.sleep(1)
                upload_file_btn = page.locator('[data-id="file-upload"]').first
                if upload_file_btn.count() == 0:
                    upload_file_btn = page.locator('text=Fazer upload de arquivo').first
                upload_file_btn.click()
                time.sleep(1)
                file_input = page.locator("input[type=file]").first

            file_input.set_input_files(filepath)
            time.sleep(5)  # aguarda upload
            print(f"    OK: {filename}")

        print("\nAguardando sincronização...")
        time.sleep(6)
        print("Upload concluído. Pode fechar a janela se desejar.")
        ctx.close()

if __name__ == "__main__":
    main()
