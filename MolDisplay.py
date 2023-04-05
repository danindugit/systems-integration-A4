#  Student Name: Danindu Marasinghe
#  Student ID: 1093791
#  Due Date: March 21, 2023 | 9:00am
#  Course: CIS*2750

import molecule

header = """<svg version="1.1" width="1000" height="1000"
            xmlns="http://www.w3.org/2000/svg">""";

footer = """</svg>""";

offsetx = 500;
offsety = 500;

class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom;
        self.z = c_atom.z;

    def __str__(self):
        return "ATOM: element = %s | x = %lf | y = %lf | z = %lf\n" % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z);

    # create an svg element for an atom
    def svg(self):
        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (self.c_atom.x * 100.0 + offsetx, self.c_atom.y * 100.0 + offsety, radius[self.c_atom.element], element_name[self.c_atom.element]);

class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond;
        self.z = c_bond.z;

    def __str__(self):
        return "BOND: a1 = %hu | a2 = %hu | epairs = %d | x1 = %lf | x2 = %lf | y1 = %lf | y2 = %lf | z = %lf | len = %lf | dx = %lf | dy = %lf\n" % (self.c_bond.a1, self.c_bond.a2, self.c_bond.epairs, self.c_bond.x1, self.c_bond.x2, self.c_bond.y1, self.c_bond.y2, self.c_bond.z, self.c_bond.len, self.c_bond.dx, self.c_bond.dy);

    # create an svg element for a bond
    def svg(self):
        svgx1 = self.c_bond.x1 * 100 + offsetx;
        svgx2 = self.c_bond.x2 * 100 + offsetx;
        svgy1 = self.c_bond.y1 * 100 + offsety;
        svgy2 = self.c_bond.y2 * 100 + offsety;
        svgdx = self.c_bond.dx * 10;
        svgdy = self.c_bond.dy * 10;
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (svgx1 - svgdy, svgy1 + svgdx, svgx1 + svgdy, svgy1 - svgdx, svgx2 + svgdy, svgy2 - svgdx, svgx2 - svgdy, svgy2 + svgdx);

class Molecule (molecule.molecule):
    def __str__(self):
        return "MOLECULE: atom_no = %hu | atom_max = %hu | bond_no = %hu | bond_max = %hu" % (self.atom_no, self.atom_max, self.bond_no, self.bond_max);

    # create a string that displays a molecule as an svg
    def svg(self):
        svgStr = header + "\n";
        atomIndex = 0;
        bondIndex = 0;

        # append atoms and bonds in the specified order until one of them is complete
        while(atomIndex < self.atom_no) and (bondIndex < self.bond_no):
            a1 = Atom(self.get_atom(atomIndex));
            b1 = Bond(self.get_bond(bondIndex));

            if a1.z < b1.z:
                svgStr += a1.svg();
                atomIndex += 1;
            else:
                svgStr += b1.svg();
                bondIndex += 1;

        # it has come out of the loop if it has run out of atoms or bonds or both
        # check for which case here and append the rest
        while atomIndex < self.atom_no:
            a1 = Atom(self.get_atom(atomIndex));
            svgStr += a1.svg();
            atomIndex += 1;
        
        while bondIndex < self.bond_no:
            b1 = Bond(self.get_bond(bondIndex));
            svgStr += b1.svg();
            bondIndex += 1;

        svgStr += footer;

        return svgStr;

    # parse an sdf file into a molecule
    def parse(self, fp):
        for _ in range(3):  # skip first 3 lines
            next(fp);

        # read atom max and bond max
        atomMax, bondMax, *_ = fp.readline().split();
        
        atomMax = int(atomMax);
        bondMax = int(bondMax);

        # read atoms
        for _ in range(atomMax):
            x, y, z, elName, *_ = fp.readline().split();
            x = float(x);
            y = float(y);
            z = float(z);
            self.append_atom(elName, x, y, z);

        # read bonds
        for _ in range(bondMax):
            a1, a2, epairs, *_ = fp.readline().split();
            a1 = int(a1) - 1;
            a2 = int(a2) - 1;
            epairs = int(epairs);
            self.append_bond(a1, a2, epairs);
