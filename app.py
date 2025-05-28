from flask import Flask, request, send_file, jsonify, Response
import molsql
import io
import re
import MolDisplay

app = Flask(__name__)

# Initialize the database
db = molsql.Database(reset=True)
db.create_tables()

# Default element
db['Elements'] = (-1, '-', 'default', 'adfff8', 'adfff8', 'adfff8', 35)

MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()

# Load empty HTML templates (normally read from files)
with open('emptySelectMolecule.html', 'r') as f:
    empty_select_html = f.read()
with open('emptyRemoveElement.html', 'r') as f:
    empty_remove_html = f.read()

def generate_molecule_table():
    rows = db.conn.execute('SELECT * FROM Molecules').fetchall()
    rows_2d = [[str(cell) for cell in row] for row in rows]
    for row in rows_2d:
        row.append(db.load_mol(row[1]).atom_no)
        row.append(db.load_mol(row[1]).bond_no)

    html_string = empty_select_html
    tbody_start = html_string.find('<tbody>')
    tbody_end = html_string.find('</tbody>')

    pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    rows_existing = pattern.findall(html_string[tbody_start:tbody_end])

    col1_values = []
    for row in rows_existing:
        col_pattern = re.compile(r'<td>(.*?)</td>')
        columns = col_pattern.findall(row)
        col1_values.append(columns[0])

    insert_point = re.compile(r'</tbody>')
    for row in rows_2d:
        if row[0] in col1_values:
            continue
        row_html = '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>\n'
        match = insert_point.search(html_string)
        if match:
            pos = match.start()
            html_string = html_string[:pos] + row_html + html_string[pos:]
    return html_string

def generate_element_table():
    rows = db.conn.execute('SELECT * FROM Elements').fetchall()
    rows_2d = [[str(cell) for cell in row] for row in rows]

    html_string = empty_remove_html
    tbody_start = html_string.find('<tbody>')
    tbody_end = html_string.find('</tbody>')

    pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    rows_existing = pattern.findall(html_string[tbody_start:tbody_end])

    col1_values = []
    for row in rows_existing:
        col_pattern = re.compile(r'<td>(.*?)</td>')
        columns = col_pattern.findall(row)
        col1_values.append(columns[1])

    insert_point = re.compile(r'</tbody>')
    for row in rows_2d:
        if row[1] in col1_values:
            continue
        row_html = '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>\n'
        match = insert_point.search(html_string)
        if match:
            pos = match.start()
            html_string = html_string[:pos] + row_html + html_string[pos:]
    return html_string

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/selectMolecule.html')
def select_molecule():
    return Response(generate_molecule_table(), mimetype='text/html')

@app.route('/removeElement.html')
def remove_element():
    return Response(generate_element_table(), mimetype='text/html')

@app.route('/uploadSDF', methods=['POST'])
def upload_sdf():
    mol_name = request.form.get("mol")
    file = request.files['fileInfo']
    fptr = io.TextIOWrapper(file.stream)
    db.add_molecule(mol_name, fptr)
    return "Uploaded", 200

@app.route('/display', methods=['POST'])
def display():
    mol_name = request.form.get("mol")
    mol = db.load_mol(mol_name)
    svg = mol.svg()
    return Response(svg, mimetype="image/svg+xml")

@app.route('/addElement', methods=['POST'])
def add_element():
    data = request.form
    db['Elements'] = (
        data.get("number"),
        data.get("code"),
        data.get("name"),
        data.get("colour1"),
        data.get("colour2"),
        data.get("colour3"),
        data.get("radius")
    )
    return "Element Added", 200

@app.route('/removeElement', methods=['POST'])
def remove_element_post():
    code = request.form.get("code")
    if code == '-':
        return "Cannot delete default element", 404
    db.conn.execute("DELETE FROM Elements WHERE ELEMENT_CODE=?", (code,))
    return "Element Removed", 200

@app.route('/<path:path>')
def static_files(path):
    return send_file(path)
