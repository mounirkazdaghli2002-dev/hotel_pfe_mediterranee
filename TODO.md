# Environment Variables Implementation TODO

## Status: [ ] In Progress

### Steps:
1. [x] Update requirements.txt (add python-dotenv==1.0.1)
2. [x] Create .env.example with template vars
3. [x] Update .gitignore (.env, *.db)
4. [x] Update config.yml with env var documentation
5. [x] Create .streamlit/secrets.toml for Streamlit secrets
6. [x] Edit app.py: add load_dotenv(), use os.getenv for file paths
7. [x] Edit init_db.py: use DB_PATH=os.getenv()
8. [x] Edit check_db.py: use DB_PATH=os.getenv()
9. [x] Run `pip install -r requirements.txt`
10. [x] Test: copy .env.example to .env, edit if needed, run app.py (local success, deployment needs git push)
11. [ ] Mark complete, remove TODO.md

**Instructions:** Edit this file as steps complete. Use `[x]` for done.

