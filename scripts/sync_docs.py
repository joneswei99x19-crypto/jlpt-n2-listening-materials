from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "学习资料_修订版"
DEST = ROOT / "docs"
if not SOURCE.is_dir():
    raise SystemExit(f"找不到本地资料目录：{SOURCE}")

copied = 0
for src in SOURCE.rglob("*"):
    if not src.is_file() or src.name == ".DS_Store" or src.name.startswith("._"):
        continue
    dst = DEST / src.relative_to(SOURCE)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or src.read_bytes() != dst.read_bytes():
        shutil.copy2(src, dst)
        copied += 1
print(f"文档同步完成：更新/新增 {copied} 个文件；未执行任何删除。")
