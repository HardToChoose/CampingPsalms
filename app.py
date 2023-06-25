from flask import Flask, render_template, request, jsonify
import sqlite3

database = 'db/songs.db'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/records/<id>', methods=['GET'])
def get_record(id):
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

@app.route('/autocompletion', methods=['GET'])
def autocompletion():
    query = request.args.get('search')

    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Perform the autocomplete query
    cursor.execute("SELECT Id, Title FROM Songs WHERE UPPER(Title) LIKE UPPER(?)", ('%' + query + '%',))
    rows = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Extract the Title and Url values from the rows
    results = [{'id': row[0], 'title': row[1]} for row in rows]

    return jsonify(results)
   
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
