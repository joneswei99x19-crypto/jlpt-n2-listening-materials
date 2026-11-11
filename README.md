# JLPT N2 Listening Docs Site

MkDocs Material static documentation site. Source Markdown remains in the sibling `学习资料_修订版/` directory; `docs/` is a public deployment copy.

## Local preview

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Update and publish

Run `./update.sh`. It copies changed/new source files without deleting anything, checks for likely secrets, shows changes, asks for a commit message, commits, and pushes. GitHub Actions then builds and deploys Pages.
