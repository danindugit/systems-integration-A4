from http.server import HTTPServer, BaseHTTPRequestHandler;

import sys;     # to get command line argument for port
import urllib;  # code to parse for data

import molsql;

import cgi;
import io;

# list of files that we allow the web-server to serve to clients
# (we don't want to serve any file that the client requests)
public_files = [ '/index.html', '/style.css', '/script.js' , '/addElement.html', '/removeElement.html', '/uploadSDF.html', '/selectMolecule.html'];

class MyHandler( BaseHTTPRequestHandler ):
   def do_GET(self):

      if self.path == "/selectMolecule.html":
         self.send_response(200);
         self.send_header( "Content-type", "text/html" );
      
         # save file to a string
         with open('selectMolecule.html', 'r') as f:
            html_string = f.read();
         
         # # Find the line number of the <tbody> tag
         # tbody_line_number = None;
         # for i, line in enumerate(html_string.splitlines()):
         #    if '<tbody>' in line:
         #       tbody_line_number = i;
         #       break;

         # # Append a new row right after the <tbody> tag
         # if tbody_line_number is not None:
         #    new_row = '';
         #    lines = html_string.splitlines();
         #    lines.insert(tbody_line_number+1, new_row);
         #    html_string = '\n'.join(lines);

         # Find the line number of the </tbody> tag
         tbody_line_number = None
         for i, line in enumerate(html_string.splitlines()):
            if '</tbody>' in line:
               tbody_line_number = i
               break

         # Append a new row right before the </tbody> tag
         if tbody_line_number is not None:
            new_row = '<tr><td>1</td><td>Meth</td></tr>'
            lines = html_string.splitlines()
            lines.insert(tbody_line_number, new_row)
            html_string = '\n'.join(lines)

         # print(html_string);

         with open('selectMolecule.html.html', 'w') as f:
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
         print("makes it to uploadSDF.");
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
         print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall());

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


db = molsql.Database(reset=True);
db.create_tables();
db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000','020000',40);

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );

httpd.serve_forever();
