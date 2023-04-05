#  Student Name: Danindu Marasinghe
#  Student ID: 1093791
#  Due Date: March 21, 2023 | 9:00am
#  Course: CIS*2750

import os;
import sqlite3;
import MolDisplay;

class Database:
    def __init__(self, reset = False):
        # if reset is true, delete the existing molecule.db file
        if reset == True:
            if os.path.exists( 'molecule.db' ):
                os.remove( 'molecule.db' );

        # create a database connection to molecule.db
        self.conn = sqlite3.connect( 'molecule.db' );

    # method to create tables
    def create_tables(self):
        # create Elements table
        if(not self.table_exists("Elements")):
            self.conn.execute( """CREATE TABLE Elements 
                                  ( ELEMENT_NO      INTEGER NOT NULL,
                                    ELEMENT_CODE    VARCHAR(3) NOT NULL,
                                    ELEMENT_NAME    VARCHAR(32) NOT NULL,
                                    COLOUR1         CHAR(6) NOT NULL,
                                    COLOUR2         CHAR(6) NOT NULL,
                                    COLOUR3         CHAR(6) NOT NULL,
                                    RADIUS          DECIMAL(3) NOT NULL, 
                                    PRIMARY KEY (ELEMENT_CODE) );""");
    
        # create Atoms table
        if(not self.table_exists("Atoms")):
            self.conn.execute( """CREATE TABLE Atoms 
                                  ( ATOM_ID         INTEGER PRIMARY KEY AUTOINCREMENT,
                                    ELEMENT_CODE    VARCHAR(3) NOT NULL,
                                    X               DECIMAL(7, 4) NOT NULL,
                                    Y               DECIMAL(7, 4) NOT NULL,
                                    Z               DECIMAL(7, 4) NOT NULL,
                                    FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements );""");
        
        # create Bonds table
        if(not self.table_exists("Bonds")):
            self.conn.execute( """CREATE TABLE Bonds 
                                  ( BOND_ID         INTEGER PRIMARY KEY AUTOINCREMENT,
                                    A1              INTEGER NOT NULL,
                                    A2              INTEGER NOT NULL,
                                    EPAIRS          INTEGER NOT NULL);""");
        
        # create Molecules table
        if(not self.table_exists("Molecules")):
            self.conn.execute( """CREATE TABLE Molecules 
                                  ( MOLECULE_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
                                    NAME            TEXT NOT NULL UNIQUE);""");
        
        # create MoleculeAtom table
        if(not self.table_exists("MoleculeAtom")):
            self.conn.execute( """CREATE TABLE MoleculeAtom 
                                  ( MOLECULE_ID     INTEGER AUTO_INCREMENT,
                                    ATOM_ID         INTEGER AUTO_INCREMENT,
                                    PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                    FOREIGN KEY (ATOM_ID) REFERENCES Atoms );""");
        
        # create MoleculeBond table
        if(not self.table_exists("MoleculeBond")):
            self.conn.execute( """CREATE TABLE MoleculeBond 
                                  ( MOLECULE_ID     INTEGER AUTO_INCREMENT,
                                    BOND_ID         INTEGER AUTO_INCREMENT,
                                    PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                    FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                                    FOREIGN KEY (BOND_ID) REFERENCES Bonds );""");
    
        self.conn.commit();
    
    def __setitem__(self, table, values):
        # execute insert command
        self.conn.execute(f"""INSERT
                              INTO {table}
                              VALUES {values}; """);

        self.conn.commit();

    # method to add a new atom to the database
    def add_atom(self, molname, atom):
        # insert atom into Atoms table
        self.conn.execute(f"""INSERT
                              INTO Atoms (ELEMENT_CODE,         X,              Y,              Z)
                              VALUES     ('{atom.element}',     '{atom.x}',     '{atom.y}',     '{atom.z}'); """);
        
        # get atom id and molecule id
        atom_id = self.conn.execute(f"SELECT MAX(ATOM_ID) FROM Atoms").fetchone()[0];        
        mol_id = self.conn.execute(f"SELECT MOLECULE_ID FROM Molecules WHERE NAME = '{molname}'").fetchone()[0];
    
        # insert link into MoleculeAtom table
        self.conn.execute(f"""INSERT
                              INTO MoleculeAtom (MOLECULE_ID, ATOM_ID)
                              VALUES            ('{mol_id}',    '{atom_id}'); """);
    
        self.conn.commit();

    
    # method to add a new bond to the database
    def add_bond(self, molname, bond):
        # insert bond into Bonds table
        self.conn.execute(f"""INSERT
                              INTO Bonds (A1,               A2,             EPAIRS)
                              VALUES     ('{bond.a1}',      '{bond.a2}',    '{bond.epairs}'); """);
        
        # get bond id and molecule id
        bond_id = self.conn.execute(f"SELECT MAX(BOND_ID) FROM Bonds").fetchone()[0];
        mol_id = self.conn.execute(f"SELECT MOLECULE_ID FROM Molecules WHERE NAME = '{molname}'").fetchone()[0];
    
        # insert link into MoleculeBond table
        self.conn.execute(f"""INSERT
                              INTO MoleculeBond (MOLECULE_ID, BOND_ID)
                              VALUES            ('{mol_id}',    '{bond_id}'); """);
    
        self.conn.commit();

    # method to add a new molecule to the database
    def add_molecule(self, name, fp):
        # create a Molecule object
        new_mol = MolDisplay.Molecule();
        new_mol.parse(fp);
        fp.close();
    
        # add new molecule to the Molecules table
        self.conn.execute(f"""INSERT
                             INTO Molecules (NAME)
                             VALUES         ('{name}');""");
    
        # add each atom and bond in the molecule to the database
        # atoms
        for i in range(new_mol.atom_no):
            self.add_atom(name, new_mol.get_atom(i));
        # bonds
        for i in range(new_mol.bond_no):
            self.add_bond(name, new_mol.get_bond(i));
    
        self.conn.commit();
    
    # method to load a molecule from the database
    def load_mol(self, name):
        # create a Molecule object
        new_mol = MolDisplay.Molecule();

        # get molecule id
        mol_id = self.conn.execute(f"""SELECT MOLECULE_ID FROM Molecules WHERE NAME = '{name}'""").fetchone()[0];
        # select all atoms associated with the input Molecule name
        atom_data = self.conn.execute(f"""SELECT * FROM Atoms, MoleculeAtom
                                          WHERE (MoleculeAtom.ATOM_ID = Atoms.ATOM_ID)
                                            AND MOLECULE_ID = '{mol_id}'
                                          ORDER BY ATOM_ID;""");
    
        # loop through the table and append atoms to the new molecule
        atom_table = atom_data.fetchall();
        for i in range(len(atom_table)):
            new_mol.append_atom(atom_table[i][1], atom_table[i][2], atom_table[i][3], atom_table[i][4]);

        # select all bonds associated with the input Molecule name
        bond_data = self.conn.execute(f"""SELECT * FROM Bonds, MoleculeBond
                                          WHERE (MoleculeBond.BOND_ID = Bonds.BOND_ID)
                                            AND MOLECULE_ID = '{mol_id}'
                                          ORDER BY BOND_ID;""");

        # loop through the table and append atoms to the new molecule
        bond_table = bond_data.fetchall();
        for i in range(len(bond_table)):
            new_mol.append_bond(bond_table[i][1], bond_table[i][2], bond_table[i][3]);

        return new_mol;

    # returns a dictionary that maps elements to their radius
    def radius(self):
        # query the elements table
        radius_data = self.conn.execute(f"""SELECT ELEMENT_CODE, RADIUS FROM Elements;""");
    
        # create a radius dictionary
        return dict(radius_data);

    # returns a dictionary that maps elements to their element name
    def element_name(self):
        # query the elements table
        element_name_data = self.conn.execute(f"""SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;""");
    
        # create a element name dictionary
        return dict(element_name_data);

    # returns a string that dictates the appearance of elements in an svg
    def radial_gradients(self):
        # query the elements table
        element_data = self.conn.execute(f"""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements;""");
    
        result_str = "";
    
        # append the specified string for each element to result_str
        element_table = element_data.fetchall();
        for i in range(len(element_table)):
            result_str += """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                               <stop offset="0%%" stop-color="#%s"/>
                               <stop offset="50%%" stop-color="#%s"/>
                               <stop offset="100%%" stop-color="#%s"/>
                             </radialGradient>""" % (element_table[i][0], element_table[i][1], element_table[i][2], element_table[i][3]);

        return result_str;
        
    # helper function to check if a table exists
    def table_exists(self, name):
        # create cursor object
        cursor = self.conn.cursor();

        # execute a pragma statement to retrieve table information
        cursor.execute(f"PRAGMA table_info({name})");

        # store table information
        table_info = cursor.fetchone();

        if table_info:
            return True;
        else:
            return False;
