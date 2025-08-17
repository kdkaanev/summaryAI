#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

# Патърн за OpenAI API ключове
OPENAI_KEY_PATTERN = r"(sk-[A-Za-z0-9]{32,})"

# Създаваме replacements.txt за git-filter-repo
with open("replacements.txt", "w", encoding="utf-8") as f:
    f.write(f"{OPENAI_KEY_PATTERN}==>OPENAI_API_KEY\n")

# Премахваме ключа от цялата история на git
print("🔍 Премахвам OpenAI ключове от историята...")
subprocess.run(["git", "filter-repo", "--replace-text", "replacements.txt"], check=True)

# Генерираме нов API ключ placeholder в .env
env_path = Path(".env")
if not env_path.exists():
    env_path.write_text("OPENAI_API_KEY=PUT_YOUR_KEY_HERE\n", encoding="utf-8")
    print("✅ Създаден нов .env с placeholder ключ.")
else:
    print("ℹ️ .env вече съществува — не го презаписвам.")

print("🚀 Готово! Сега направи нов ключ в OpenAI и го сложи в .env.")
print("❗ След това push-ни със --force, защото историята е презаписана:")
print("   git push origin main --force")
