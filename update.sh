#!/bin/sh
set -eu
cd "$(dirname "$0")"

python3 scripts/sync_docs.py

if [ -z "$(git status --porcelain)" ]; then
  echo "没有文件变化，无需提交。"
  exit 0
fi

echo "即将提交的变更："
git status --short

if git diff --name-only --diff-filter=D | grep . >/dev/null 2>&1; then
  echo "检测到工作区文件删除；按保护规则停止，不会提交删除。" >&2
  exit 1
fi

if git diff --cached --name-only --diff-filter=D | grep . >/dev/null 2>&1; then
  echo "暂存区包含删除；按保护规则停止，不会提交删除。" >&2
  exit 1
fi

python3 scripts/check_public_files.py

echo "安全检查通过。请输入本次更新说明（留空使用默认说明）："
IFS= read -r message || true
if [ -z "${message:-}" ]; then message="更新学习资料"; fi

git add --all
if git diff --cached --name-only --diff-filter=D | grep . >/dev/null 2>&1; then
  echo "暂存后发现删除项，停止提交。" >&2
  git reset
  exit 1
fi

git diff --cached --stat
git commit -m "$message"
if ! git push; then
  echo "推送失败。请检查网络、GitHub 登录/SSH 或仓库权限后重试。" >&2
  exit 1
fi
