import os
import sqlite3
from datetime import datetime
from src.pdf_reader import extract_text

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'memory.db')

def init_knowledge_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            category TEXT,
            content TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_knowledge(source, category, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO knowledge_base (source, category, content, timestamp) VALUES (?, ?, ?, ?)",
        (source, category, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_all_knowledge():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, source, category, content FROM knowledge_base")
    rows = c.fetchall()
    conn.close()
    return rows


def get_knowledge_summary():
    rows = get_all_knowledge()
    if not rows:
        return None

    summary = "=== PERSONAL KNOWLEDGE BASE ABOUT SOUD ===\n\n"
    for item_id, source, category, content in rows:
        summary += f"--- {category.upper()} (from {source}) ---\n"
        summary += content[:2000] + "\n\n"

    return summary

def add_manual_fact(category, content):
    add_knowledge("manual_entry", category, content)


def add_file_to_knowledge(filepath, category="general"):
    text = extract_text(filepath)
    if text:
        filename = os.path.basename(filepath)
        add_knowledge(filename, category, text)
        return True
    return False


def clear_knowledge_base():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM knowledge_base")
    conn.commit()
    conn.close()


init_knowledge_db()

def delete_knowledge_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM knowledge_base WHERE id=?", (item_id,))
    conn.commit()
    conn.close()