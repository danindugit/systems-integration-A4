from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port

import molsql;

import cgi;
import io;
import re;

import MolDisplay;

# create database
db = molsql.Database(reset=True);
db.create_tables();
db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000','020000',40);

# initialize MolDisplay
MolDisplay.radius = db.radius();
MolDisplay.element_name = db.element_name();
MolDisplay.header += db.radial_gradients();

# default element
db.radius().setdefault('-', 10)
db.element_name().setdefault('-', 'default')
db['Elements'] = ( -1, '-', 'default', '000000', '000000', '000000',10)

# reset selectMolecule table
with open('emptySelectMolecule.html', 'r') as f:
   reset_html = f.read();
with open('selectMolecule.html', 'w') as f:
   f.write(reset_html);

# reset removeElement table
with open('emptyRemoveElement.html', 'r') as f:
   reset_html = f.read();
with open('removeElement.html', 'w') as f:
   f.write(reset_html);

class MyHandler( BaseHTTPRequestHandler ):
   def do_GET(self):

      if self.path == "/selectMolecule.html":
         self.send_response(200);
         self.send_header( "Content-type", "text/html" );

         # Execute an SQL query to select all rows from the Molecules table
         rows = db.conn.execute('SELECT * FROM Molecules').fetchall();

         # Convert the list of tuples to a 2D array of strings
         rows_2d = [[str(cell) for cell in row] for row in rows];

         # add number of atoms and number of bonds
         for row in rows_2d:
            row.append(db.load_mol(row[1]).atom_no)
            row.append(db.load_mol(row[1]).bond_no)
      
         # save file to a string
         with open('selectMolecule.html', 'r') as f:
            html_string = f.read();

         # find the start and end indices of the <tbody> tag
         tbody_start = html_string.find('<tbody>')
         tbody_end = html_string.find('</tbody>')

         # extract the table rows from the HTML string using regex
         pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
         rows = pattern.findall(html_string[tbody_start:tbody_end])

         # loop through the rows and extract the first column value (mol id)
         col1_values = []
         for row in rows:
            # extract the column values using regex
            col_pattern = re.compile(r'<td>(.*?)</td>')
            columns = col_pattern.findall(row)
            
            # add the first column value to the list
            col1_values.append(columns[0])

         # Define a regex pattern to match the closing </tbody> tag
         pattern = re.compile(r'</tbody>')

         # Iterate over each row in the 2D array and append it to the HTML string
         for row in rows_2d:
            # skip if row already exists
            if row[0] in col1_values:
               continue;
            
            # Build the HTML string for the current row
            row_html = '<tr>'
            for cell in row:
               row_html += f'<td>{cell}</td>'
            row_html += '</tr>\n'
            
            # Find the position of the </tbody> tag in the HTML string
            match = pattern.search(html_string)
            if match:
               pos = match.start()
               
               # Insert the current row HTML before the </tbody> tag
               html_string = html_string[:pos] + row_html + html_string[pos:]

         with open('selectMolecule.html', 'w') as f:
            f.write(html_string)
      
         self.write_file( "selectMolecule.html" );

      elif self.path == "/removeElement.html":
         self.send_response(200);
         self.send_header( "Content-type", "text/html" );

         # Execute an SQL query to select all rows from the Elements table
         rows = db.conn.execute('SELECT * FROM Elements').fetchall();

         # Convert the list of tuples to a 2D array of strings
         rows_2d = [[str(cell) for cell in row] for row in rows];

         # save file to a string
         with open('emptyRemoveElement.html', 'r') as f:
            html_string = f.read();

         # find the start and end indices of the <tbody> tag
         tbody_start = html_string.find('<tbody>')
         tbody_end = html_string.find('</tbody>')

         # extract the table rows from the HTML string using regex
         pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
         rows = pattern.findall(html_string[tbody_start:tbody_end])

         # loop through the rows and extract the second column value (element code)
         col1_values = []
         for row in rows:
            # extract the column values using regex
            col_pattern = re.compile(r'<td>(.*?)</td>')
            columns = col_pattern.findall(row)
            
            # add the second column value to the list
            col1_values.append(columns[1])

         # Define a regex pattern to match the closing </tbody> tag
         pattern = re.compile(r'</tbody>')

         # Iterate over each row in the 2D array and append it to the HTML string
         for row in rows_2d:
            # skip if row already exists
            if row[1] in col1_values:
               continue;
            
            # Build the HTML string for the current row
            row_html = '<tr>'
            for cell in row:
               row_html += f'<td>{cell}</td>'
            row_html += '</tr>\n'
            
            # Find the position of the </tbody> tag in the HTML string
            match = pattern.search(html_string)
            if match:
               pos = match.start()
               
               # Insert the current row HTML before the </tbody> tag
               html_string = html_string[:pos] + row_html + html_string[pos:]

         with open('removeElement.html', 'w') as f:
            f.write(html_string)
      
         self.write_file( "removeElement.html" );

      elif self.path == "/" or self.path.endswith(".html"):   # make sure it's a valid file
         self.send_response( 200 );  # OK
         self.send_header( "Content-type", "text/html" );

         if self.path == "/":
            self.write_file("index.html");
         else:
            self.write_file(self.path[1:]);

      elif self.path == "/style.css":
         self.send_response(200); # ok
         self.send_header( "Content-type", "text/css" );   

         self.write_file( "style.css" );

      elif self.path == "/script.js":
         self.send_response(200); # ok
         self.send_header( "Content-type", "text/javascript" );   

         self.write_file( "script.js" );

      else:
         # if the requested URL is not one of the public_files
         self.send_response( 404 );
         self.end_headers();
         self.wfile.write( bytes( "404: not found", "utf-8" ) );



   def do_POST(self):

      if self.path == "/uploadSDF":
         form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            );
         fileInputValue = form['fileInfo'];
         formMolNameValue = form.getvalue("mol");

         fptr = fileInputValue.file.read();

         # convert to text file
         bytesIO = io.BytesIO(fptr);
         fptr = io.TextIOWrapper(bytesIO);

         db.add_molecule( formMolNameValue, fptr );

         self.send_response( 200 ); # OK
         self.end_headers();

      elif self.path == "/display":
         form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            );
      
         molNameValue = form.getvalue("mol");
         mol = db.load_mol(molNameValue);
         svg = mol.svg();

         self.send_response( 200 ); # OK
         self.send_header( "Content-type", "image/svg+xml" );
         self.end_headers();
         self.wfile.write(svg.encode());

      elif self.path == "/addElement":
         form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            );

         numberValue = form.getvalue("number");
         codeValue = form.getvalue("code");
         nameValue = form.getvalue("name");
         colour1Value = form.getvalue("colour1");
         colour2Value = form.getvalue("colour2");
         colour3Value = form.getvalue("colour3");
         radiusValue = form.getvalue("radius");

         db['Elements'] = ( numberValue, codeValue, nameValue, colour1Value, colour2Value, colour3Value, radiusValue );
      
         self.send_response( 200 ); # OK
         self.end_headers();
      
      elif self.path == "/removeElement":
         form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            );

         codeValue = form.getvalue("code");

         db.conn.execute(f"""DELETE FROM Elements WHERE ELEMENT_CODE='{codeValue}';""");

         self.send_response( 200 ); # OK
         self.end_headers();

      else:
         self.send_response( 404 );
         self.end_headers();
         self.wfile.write( bytes( "404: not found", "utf-8" ) );

   def write_file(self, filename):
      self.send_response(200); # ok
      fp = open(filename);

      # load the specified file
      page = fp.read();
      fp.close();

      # create and send headers
      self.send_header( "Content-length", len(page) );
      self.end_headers();

      # send the contents
      self.wfile.write( bytes( page, "utf-8" ) );

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );

httpd.serve_forever();
