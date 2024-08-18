from flask import jsonify, abort, Blueprint, g
import sqlite3

# Path to the SQLite database

v1 = Blueprint('api', __name__)

db_path = "dhammapada.db"


def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # This allows us to access columns by name
    return g.db


@v1.route('/verses', methods=['GET'])
def get_all_verses():
    conn = get_db_connection()
    verses = conn.execute('''
        SELECT Verse.*, Chapter.title AS chapter_title
        FROM Verse
        JOIN Chapter ON Verse.chapter_id = Chapter.id
    ''').fetchall()
    return jsonify([dict(verse) for verse in verses])


@v1.route('/verses/<int:verse_id>', methods=['GET'])
def get_verse_by_id(verse_id):
    conn = get_db_connection()
    verse = conn.execute('''
        SELECT Verse.*, Chapter.title AS chapter_title
        FROM Verse
        JOIN Chapter ON Verse.chapter_id = Chapter.id
        WHERE Verse.id = ?
    ''', (verse_id,)).fetchone()
    if verse is None:
        abort(404, description="Verse not found")
    return jsonify(dict(verse))


@v1.route('/chapters', methods=['GET'])
def get_all_chapters():
    conn = get_db_connection()
    chapters = conn.execute('SELECT * FROM Chapter').fetchall()
    result = []
    for chapter in chapters:
        chapter_dict = dict(chapter)
        verses = conn.execute('''
            SELECT Verse.*, Chapter.title AS chapter_title
            FROM Verse
            JOIN Chapter ON Verse.chapter_id = Chapter.id
            WHERE Verse.chapter_id = ?
        ''', (chapter['id'],)).fetchall()
        chapter_dict['verses'] = [dict(verse) for verse in verses]
        result.append(chapter_dict)
    return jsonify(result)


@v1.route('/chapters/<int:chapter_id>', methods=['GET'])
def get_verses_by_chapter(chapter_id):
    conn = get_db_connection()
    chapter = conn.execute('SELECT * FROM Chapter WHERE id = ?', (id,)).fetchone()
    if chapter is None:
        abort(404, description="Chapter not found")
    verses = conn.execute('''
        SELECT Verse.*, Chapter.title AS chapter_title
        FROM Verse
        JOIN Chapter ON Verse.chapter_id = Chapter.id
        WHERE Verse.chapter_id = ?
    ''', (chapter_id,)).fetchall()
    chapter_dict = dict(chapter)
    chapter_dict['verses'] = [dict(verse) for verse in verses]
    return jsonify(chapter_dict)


@v1.route('/random', methods=['GET'])
def get_random_verse():
    conn = get_db_connection()
    verse = conn.execute('''
        SELECT Verse.*, Chapter.title AS chapter_title
        FROM Verse
        JOIN Chapter ON Verse.chapter_id = Chapter.id
        ORDER BY RANDOM() LIMIT 1
    ''').fetchone()
    return jsonify(dict(verse))


@v1.errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404
