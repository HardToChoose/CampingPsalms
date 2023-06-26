from flask import Flask, render_template, request, jsonify
import sqlite3

database = 'db/songs.db'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/songs/<id>', methods=['GET'])
def get_song(id):
    if id:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        query = "SELECT Id, Title, Lyrics FROM Songs WHERE Id = ?"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        
        id = result[0] if result else 0
        title = result[1] if result else 'Unknown song'
        lyrics = result[2] if result else 'Song was not found'
        
        if request.args.get('hideAccords') == 'true':
            lyrics = remove_accords(lyrics)

    return jsonify({'id': id, 'title': title, 'lyrics': lyrics})

@app.route('/songs', methods=['GET'])
def search_songs_by_lyrics():
    match_expr = build_match_expr(request.args.get('lyricsSearch'))
    hide_accords = request.args.get('hideAccords') == 'true'

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT SongId, Title, Lyrics FROM SongsFTI WHERE Lyrics MATCH ? ORDER BY Title ASC", (match_expr,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    results = [{'id': row[0], 'title': row[1], 'lyrics': remove_accords(row[2]) if hide_accords else row[2]} for row in rows]
    return jsonify(results)

@app.route('/autocompletion', methods=['GET'])
def autocompletion():
    match_expr = build_match_expr(request.args.get('titleSearch'))

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT SongId, Title FROM SongsFTI WHERE Title MATCH ? ORDER BY Title ASC", (match_expr,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    results = [{'id': row[0], 'title': row[1]} for row in rows]
    return jsonify(results)

def build_match_expr(search):
    words = search \
        .strip() \
        .replace('\t', ' ') \
        .replace('"', '') \
        .replace("'", '') \
        .split(' ')
    
    return ' '.join(word + '*' for word in words)
   
def remove_accords(lyrics):
    notes = set(chr(n) for n in range(ord('A'), ord('H') + 1))

    def is_accord(word):
        if not word:
            return False
        
        if word in notes:
            return True

        for note in notes:
            if word.startswith(note + '#') or \
                word.startswith(note + '/') or \
                word.startswith(note + '7') or \
                word.startswith(note + 'b') or \
                word.startswith(note + 'm'):
                return True

        return False            
    
    lines = lyrics.split('<br>')
    lines.append('')
    
    total_lines = len(lines)
    i = 0
    
    result = []
    
    while i <= total_lines - 2:
        line = lines[i]
        words = set(line.split(' '))
        
        if not any(is_accord(_) for _ in words):
            if line != '':
                result.append(line)
            result.append('<br>')
        
        i += 1
            
    return ''.join(result)

if __name__ == '__main__':
    app.run(debug=True)
