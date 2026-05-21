"""
drive_reorganize.py
Reorganiza o Google Drive da Ok Delícias com Amor:
- Renomeia pastas com emoji para prefixos numéricos
- Move post_maio17.png para "02 - Posts e Stories"
- Move pasta vazia "Fotos do Produto" para lixeira
"""

import os, json, base64, sqlite3, shutil, tempfile, time, ctypes, requests
from ctypes import wintypes
from playwright.sync_api import sync_playwright

LOG = r"C:\Temp\drive_reorganize.log"
os.makedirs(r"C:\Temp", exist_ok=True)
open(LOG, 'w').close()

def log(msg):
    print(msg)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')


# ── EXTRAÇÃO DE COOKIES DO CHROME (igual ao drive_upload_v3.py) ──────────────

class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_char))]

def dpapi_decrypt(data):
    p = ctypes.create_string_buffer(data, len(data))
    blobin  = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    ok = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not ok:
        raise OSError(f"DPAPI erro: {ctypes.GetLastError()}")
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

def get_chrome_key():
    local_state = r"C:\Users\nasci\AppData\Local\Google\Chrome\User Data\Local State"
    with open(local_state, encoding='utf-8') as f:
        data = json.load(f)
    enc_key = base64.b64decode(data['os_crypt']['encrypted_key'])[5:]
    return dpapi_decrypt(enc_key)

def decrypt_cookie(enc_val, key):
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        if enc_val[:3] in (b'v10', b'v11'):
            nonce = enc_val[3:15]
            return AESGCM(key).decrypt(nonce, enc_val[15:], None).decode('utf-8', errors='replace')
    except:
        pass
    try:
        return enc_val.decode('utf-8', errors='replace')
    except:
        return ""

def _copy_locked_file(src, dst):
    """Copia arquivo bloqueado usando .NET FileShare.ReadWrite via PowerShell."""
    import subprocess
    ps = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    script = (
        f"$fs = [System.IO.File]::Open('{src}', "
        f"[System.IO.FileMode]::Open, "
        f"[System.IO.FileAccess]::Read, "
        f"[System.IO.FileShare]::ReadWrite);"
        f"$fd = [System.IO.File]::Create('{dst}');"
        f"$fs.CopyTo($fd); $fd.Flush(); $fd.Close(); $fs.Close();"
        f"Write-Output 'OK'"
    )
    result = subprocess.run(
        [ps, "-NonInteractive", "-Command", script],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0 or "OK" not in result.stdout:
        raise OSError(f"PowerShell copy falhou: {result.stderr.strip()}")


def extract_cookies():
    log("Extraindo cookies do Chrome...")
    key = get_chrome_key()
    cookies_db = r"C:\Users\nasci\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"
    tmp     = os.path.join(tempfile.gettempdir(), "tmp_cookies_reorg.db")
    tmp_wal = tmp + "-wal"
    tmp_shm = tmp + "-shm"
    wal_src = cookies_db + "-wal"
    shm_src = cookies_db + "-shm"

    # Copia o banco principal
    try:
        shutil.copy2(cookies_db, tmp)
    except (PermissionError, OSError):
        log("  Chrome aberto - copiando via PowerShell (FileShare.ReadWrite)...")
        _copy_locked_file(cookies_db, tmp)

    # Copia WAL e SHM se existirem (necessário para Chrome com WAL mode)
    for src_extra, dst_extra in [(wal_src, tmp_wal), (shm_src, tmp_shm)]:
        if os.path.exists(src_extra):
            try:
                shutil.copy2(src_extra, dst_extra)
            except (PermissionError, OSError):
                try:
                    _copy_locked_file(src_extra, dst_extra)
                except Exception:
                    pass  # WAL opcional

    conn = sqlite3.connect(tmp)

    cur  = conn.cursor()
    cur.execute("""
        SELECT host_key, name, encrypted_value, path, expires_utc, is_secure, is_httponly, samesite
        FROM cookies WHERE host_key LIKE '%google.com%'
    """)
    rows = cur.fetchall()
    conn.close()
    if tmp and os.path.exists(tmp):
        os.unlink(tmp)

    pw_cookies = []
    for host_key, name, enc_val, path, expires_utc, is_secure, is_httponly, samesite in rows:
        value = decrypt_cookie(enc_val, key)
        if not value:
            continue
        exp = None
        if expires_utc and expires_utc > 0:
            exp = (expires_utc / 1_000_000) - 11_644_473_600
            if exp < 0:
                continue
        same   = {-1:"None", 0:"None", 1:"Lax", 2:"Strict"}.get(samesite, "None")
        domain = host_key if host_key.startswith('.') else f".{host_key}"
        c = {"name": name, "value": value, "domain": domain,
             "path": path or "/", "secure": bool(is_secure),
             "httpOnly": bool(is_httponly), "sameSite": same}
        if exp:
            c["expires"] = exp
        pw_cookies.append(c)

    log(f"  {len(pw_cookies)} cookies prontos")
    return pw_cookies


# ── IDs DO DRIVE ──────────────────────────────────────────────────────────────

ROOT_ID          = "1uNAvaht-8FPi1x_S_LILdg4m42i2Qcms"

# Mapeamento: ID -> novo nome
RENAMES = {
    "1NDx_Uj_e2-H2lGNAI5vmOwIyy-Ui_7ea": "01 - Documentos Estratégicos",
    "1078tTdx3JS8A_diLAgzJgBjkbino2Rw_": "02 - Posts e Stories",
    "1TCSvAYtJWQVkxRV_7ntcBBmEVdldEKQC": "03 - Fotos do Produto",
    "1XrjGhzLVTfvEvNMmtH13hLWdI4UZ51Hj": "04 - Scripts de Producao",
}

# post_maio17.png (solto na raiz) -> mover para "02 - Posts e Stories"
POST17_ID         = "1fgTsSfRvdQ9rZGN2ieeVxVw-Xmae8sn8"
POSTS_FOLDER_ID   = "1078tTdx3JS8A_diLAgzJgBjkbino2Rw_"

# Pasta vazia "📷 Fotos do Produto" -> lixeira
EMPTY_FOLDER_ID   = "1SoYN6nRZMtNqGeBOxJQEcTNKsAsqb5t8"


# ── CAPTURA DO ACCESS TOKEN ───────────────────────────────────────────────────

def get_access_token(cookies):
    """Abre Drive em headless, intercepta o Bearer token das chamadas à API."""
    log("Iniciando browser headless para capturar token...")
    token_holder = [None]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )

        # Injeta cookies
        ok_count = 0
        for c in cookies:
            try:
                ctx.add_cookies([c])
                ok_count += 1
            except:
                pass
        log(f"  {ok_count} cookies injetados")

        page = ctx.new_page()

        def on_request(request):
            if token_holder[0]:
                return
            auth = request.headers.get('authorization', '')
            if auth.startswith('Bearer ') and 'googleapis.com' in request.url:
                token_holder[0] = auth[7:]
                log(f"  Token capturado: {token_holder[0][:20]}...")

        page.on('request', on_request)

        # Navega para a pasta raiz do projeto
        page.goto(
            f"https://drive.google.com/drive/folders/{ROOT_ID}",
            wait_until="domcontentloaded", timeout=30000
        )
        time.sleep(6)

        # Fallback: tenta My Drive se não capturou ainda
        if not token_holder[0]:
            log("  Tentando My Drive como fallback...")
            page.goto("https://drive.google.com/drive/my-drive",
                      wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)

        browser.close()

    return token_holder[0]


# ── CHAMADAS À API ────────────────────────────────────────────────────────────

def drive_patch(token, file_id, body, extra_params=""):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
    if extra_params:
        url += f"?{extra_params}"
    resp = requests.patch(
        url,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=20
    )
    return resp.status_code, resp.json()


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    log("=== Drive Reorganize - Ok Delicias com Amor ===\n")

    cookies = extract_cookies()

    token = get_access_token(cookies)
    if not token:
        log("ERRO: token nao capturado. Chrome precisa estar logado no Google.")
        return

    log("\n--- Renomeando pastas ---")
    for folder_id, new_name in RENAMES.items():
        log(f"  '{folder_id[:16]}...' -> '{new_name}'")
        status, resp = drive_patch(token, folder_id, {"name": new_name})
        if status == 200:
            log(f"    OK: {resp.get('name')}")
        else:
            log(f"    ERRO {status}: {resp}")

    log("\n--- Movendo post_maio17.png ---")
    status, resp = drive_patch(
        token, POST17_ID, {},
        f"addParents={POSTS_FOLDER_ID}&removeParents={ROOT_ID}&fields=id,parents"
    )
    if status == 200:
        log("    OK: post_maio17.png movido para 02 - Posts e Stories")
    else:
        log(f"    ERRO {status}: {resp}")

    log("\n--- Pasta vazia para lixeira ---")
    status, resp = drive_patch(token, EMPTY_FOLDER_ID, {"trashed": True})
    if status == 200:
        log("    OK: pasta vazia na lixeira")
    else:
        log(f"    ERRO {status}: {resp}")

    log("\n=== CONCLUIDO ===")
    log(f"Log: {LOG}")


if __name__ == "__main__":
    main()
