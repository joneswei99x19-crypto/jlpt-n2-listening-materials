from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_NAMES = re.compile(r"(^|/)(\.env($|\.)|id_rsa|id_ed25519|credentials\.json|secrets?\.|[^/]+\.(pem|key|p12|pfx))", re.I)
PRIVATE_KEY = re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----")
SECRET_ASSIGNMENT = re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[:=]\s*['\"]?[^\s'\"]{10,}")
errors=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or any(part in {".git", ".venv", "site", "__pycache__"} for part in p.parts):
        continue
    rel=p.relative_to(ROOT).as_posix()
    if BLOCKED_NAMES.search(rel): errors.append(f"可疑敏感文件名：{rel}")
    if p.suffix.lower() in {".md", ".yml", ".yaml", ".txt", ".json", ".html", ".py", ".sh"}:
        try: data=p.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        if PRIVATE_KEY.search(data): errors.append(f"包含私钥标记：{rel}")
        if SECRET_ASSIGNMENT.search(data): errors.append(f"疑似凭据赋值：{rel}")
if errors:
    print("公开文件检查失败：")
    print("\n".join(errors))
    raise SystemExit(1)
print("公开文件检查通过。")
