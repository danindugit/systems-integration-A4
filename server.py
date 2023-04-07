from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port
import urllib;  # code to parse for data

import molsql;
import sqlite3;

import cgi;
import io;
import re;

# create database
db = molsql.Database(reset=True);
db.create_tables();
db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000','020000',40);

# reset selectMolecule table
with open('selectMolecule.html', 'w') as f:
   f.write("""<!--  Name: Danindu Marasinghe
      Course: CIS*2750
      Due Date: 2023-04-04 -->

      <!doctype html>
      <html lang="en">
        <head>
          <!-- JQuery -->
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>

          <!-- Local javascript -->
          <script src="script.js" /></script>
      
          <!-- Bootstrap CSS -->
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
      
          <!-- Local stylesheet -->
          <link rel="stylesheet" type="text/css" href="style.css" />
        </head>
        </head>
        <body>
         <!-- navbar -->
         <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="./index.html">Molecule Viewer</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
               <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
               <ul class="navbar-nav">
                  <li class="nav-item">
                     <a class="nav-link" href="./index.html">Home </a>
                  </li>
                  <li class="nav-item">
                     <a class="nav-link" href="./addElement.html">Add Element</a>
                  </li>
                  <li class="nav-item">
                     <a class="nav-link" href="./removeElement.html">Remove Element</a>
                  </li>
                  <li class="nav-item">
                     <a class="nav-link" href="./uploadSDF.html">Upload sdf <span class="sr-only">(current)</span></a>
                  </li>
                  <li class="nav-item active">
                     <a class="nav-link" href="./selectMolecule.html">Select Molecule <span class="sr-only">(current)</span></a>
                  </li>
               </ul>
            </div>
         </nav>
         
         <!-- Title -->
         <h1 class="display-2 text-center title">Select a Molecule</h1>   
         <br>  
         <div class="row content-row">
            <div class="text-center col-md-6">
               <h3>List of Molecules:</h3>
               <br>
               <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Molecule_ID</th>
                      <th scope="col">Molecule Name</th>
                      <th scope="col">Number of Atoms</th>
                      <th scope="col">Number of Bonds</th>
                    </tr>
                  </thead>
                  <tbody>
                  </tbody>
                </table>
            </div>
            <div class="col-md-6 info-col">
               <p>Please enter the name of the molecule you'd like to display.</p>
               <input class="form-control" type="text" placeholder="Molecule Name">
               <button type="button" class="btn btn-primary btn-display">Display Molecule</button>
            </div>
         </div>   
      
         <!-- Bootstrap JavaScript -->
         <!-- <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script> -->
         <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
         <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
      </html>""")

class MyHandler( BaseHTTPRequestHandler ):
   def do_GET(self):

      if self.path == "/selectMolecule.html":
         self.send_response(200);
         self.send_header( "Content-type", "text/html" );

         # open database
         db = molsql.Database(reset=False);

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

         # loop through the rows and extract the first column value
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
         # print("makes it to uploadSDF.");
         # code to handle uploadSDF

         # content_length = int(self.headers['Content-Length']);
         # body = self.rfile.read(content_length);

         # print( repr( body.decode('utf-8') ) );

         # # convert POST content into a dictionary
         # postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

         # print( postvars );


         # print("ok1.");
         # db = molsql.Database(reset=False);
         # content_length = int(self.headers.get('Content-Length'));
         # print("ok1.2");
         # post_data = self.rfile.read(content_length);
         # print("ok1.3");
         # form_data = json.loads(post_data.decode('utf-8'));
         # print("ok1.4");

         form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            );
         fileInputValue = form['fileInfo'];
         formMolNameValue = form.getvalue("mol");

         # print(fileInputValue.filename);
         # print(fileInputValue);
         # print(formMolNameValue);

         fptr = fileInputValue.file.read();

         # convert to text file
         bytesIO = io.BytesIO(fptr);
         fptr = io.TextIOWrapper(bytesIO);

         # fp = os.fopen(fileInputValue.filename);

         db.add_molecule( formMolNameValue, fptr );

         # print("ok2.");
         # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall());

         # message = "sdf file uploaded to database";

         self.send_response( 200 ); # OK
         # self.send_header( "Content-type", "text/plain" );
         # self.send_header( "Content-length", len(message) );
         self.end_headers();

         # self.wfile.write( bytes( message, "utf-8" ) );

      elif self.path == "/form_handler.html":

         # this is specific to 'multipart/form-data' encoding used by POST
         content_length = int(self.headers['Content-Length']);
         body = self.rfile.read(content_length);

         print( repr( body.decode('utf-8') ) );

         # convert POST content into a dictionary
         postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

         print( postvars );

         message = "data received";

         self.send_response( 200 ); # OK
         self.send_header( "Content-type", "text/plain" );
         self.send_header( "Content-length", len(message) );
         self.end_headers();

         self.wfile.write( bytes( message, "utf-8" ) );

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
