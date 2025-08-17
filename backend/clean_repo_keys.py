import os
import re
import subprocess
import tempfile

PLACEHOLDER_KEY = "OPENAI_API_KEY=your_openai_key_here"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}\n{result.stderr}")
        raise SystemExit(1)
    return result.stdout.strip()

def remove_keys_from_repo():
    pattern = re.compile(r"sk-[a-zA-Z0-9]{32,}")
    for root, _, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = pattern.sub("OPENAI_API_KEY", content)
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except (UnicodeDecodeError, PermissionError):
                pass

def ensure_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(PLACEHOLDER_KEY + "\n")
    with open(".gitignore", "a", encoding="utf-8") as f:
        f.write("\n.env\n")

def rewrite_git_history():
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write("sk-[a-zA-Z0-9]{32,}==>OPENAI_API_KEY\n")
        tmp_path = tmp.name
    run_cmd("pip install git-filter-repo")
    run_cmd(f"git filter-repo --replace-text {tmp_path}")
    os.remove(tmp_path)

print("[INFO] Премахвам ключове от файловете...")
remove_keys_from_repo()

print("[INFO] Създавам .env файл с placeholder и го добавям в .gitignore...")
ensure_env_file()

print("[INFO] Пренаписвам историята, за да махна ключовете...")
rewrite_git_history()

print("[SUCCESS] Готово! Ключовете са премахнати и .env е добавен в .gitignore.")
