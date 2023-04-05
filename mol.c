/*
 Student Name: Danindu Marasinghe
 Student ID: 1093791
 Due Date: March 21, 2023 | 9:00am
 Course: CIS*2750
 */

#include "mol.h"

/******
 atomset:  copies inputted data into an inputted atom
 In: a pointer to an atom struct, an element string, and coordinates as doubles
 Out: none
*******/
void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

/******
 atomget:  copies inputted atom into an inputted data variables
 In: a pointer to an atom struct, an element string, and coordinates as doubles
 Out: none
*******/
void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

/******
 bondset:  copies inputted bond data into an inputted bond
 In: a pointer to a bond struct, 2 pointers to atom structs, and the number of electron pairs
 Out: none
*******/
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

void compute_coords(bond *bond)
{
    // compute x, y, and z
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2.0;

    // compute len
    bond->len = sqrt(pow((bond->x2 - bond->x1), 2) + pow((bond->y2 - bond->y1), 2));

    // compute dx and dy
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}

/******
 bondget:  copies inputted bond into inputted bond data
 In: a pointer to a bond struct, 2 pointers to atom structs, and the number of electron pairs
 Out: none
*******/
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

/******
 molmalloc:  allocates memory for a new molecule
 In: the max number of atoms in the molecule and the max number of bonds in the molecule
 Out: pointer to the new molecule
*******/
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    molecule *mol = malloc(sizeof(molecule));
    if (mol == NULL)
    {
        return NULL;
    }
    atom *atoms = malloc(sizeof(atom) * atom_max);
    if (atoms == NULL && atom_max > 0)
    {
        return NULL;
    }
    atom **atom_ptrs = malloc(sizeof(atom *) * atom_max);
    if (atom_ptrs == NULL && atom_max > 0)
    {
        return NULL;
    }
    bond *bonds = malloc(sizeof(bond) * bond_max);
    if (bonds == NULL && bond_max > 0)
    {
        return NULL;
    }
    bond **bond_ptrs = malloc(sizeof(bond *) * bond_max);
    if (bond_ptrs == NULL && bond_max > 0)
    {
        return NULL;
    }

    mol->atom_max = atom_max;
    mol->atom_no = 0;
    mol->bond_max = bond_max;
    mol->bond_no = 0;

    mol->atoms = atoms;
    mol->atom_ptrs = atom_ptrs;
    mol->bonds = bonds;
    mol->bond_ptrs = bond_ptrs;

    return mol;
}

/******
 molcopy:  allocates memory for a new molecule based on a source molecule
 In: the source molecule
 Out: pointer to the new molecule
*******/
molecule *molcopy(molecule *src)
{
    if (src == NULL)
    {
        return NULL;
    }

    molecule *newMol = molmalloc(src->atom_max, src->bond_max);
    if (newMol == NULL)
    {
        return NULL;
    }

    for (int i = 0; i < src->atom_no; i++)
    {
        molappend_atom(newMol, &(src->atoms[i]));
    }

    for (int i = 0; i < src->bond_no; i++)
    {
        molappend_bond(newMol, &(src->bonds[i]));
    }

    return newMol;
}

/******
 molfree:  frees a molecule
 In: a pointer to the molecule
 Out: none
*******/
void molfree(molecule *ptr)
{
    free(ptr->atoms);
    free(ptr->bonds);
    free(ptr->atom_ptrs);
    free(ptr->bond_ptrs);
    free(ptr);
}

/******
 molappend_atom:  appends an atom to a molecule
 In: a pointer to the molecule and a pointer to the atom
 Out: none
*******/
void molappend_atom(molecule *molecule, atom *atom)
{
    if (atom == NULL)
    {
        return;
    }

    // check if atoms are maxed out
    if (molecule->atom_no == molecule->atom_max)
    {
        if (molecule->atom_max == 0)
        {
            molecule->atom_max = 1;
        }
        else
        {
            molecule->atom_max = molecule->atom_max * 2;
        }
        // realloc accordingly
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
    }

    // update atom_no
    molecule->atom_no++;

    // set the current atom to the input atom
    memcpy(&(molecule->atoms[molecule->atom_no - 1]), atom, sizeof(struct atom));

    // set the atom_ptr to point to this atom
    for (int i = 0; i < molecule->atom_no; i++)
    {
        molecule->atom_ptrs[i] = &(molecule->atoms[i]);
    }
}

/******
 molappend_bond:  appends an bond to a molecule
 In: a pointer to the molecule and a pointer to the bond
 Out: none
*******/
void molappend_bond(molecule *molecule, bond *bond)
{
    if (bond == NULL)
    {
        return;
    }

    // check if bonds are maxed out
    if (molecule->bond_no == molecule->bond_max)
    {
        if (molecule->bond_max == 0)
        {
            molecule->bond_max = 1;
        }
        else
        {
            molecule->bond_max = molecule->bond_max * 2;
        }
        // realloc accordingly
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
    }

    // update bond_no
    molecule->bond_no++;

    // set the current bond to the input bond
    memcpy(&(molecule->bonds[molecule->bond_no - 1]), bond, sizeof(struct bond));

    // set the bond_ptr to point to this bond
    for (int i = 0; i < molecule->bond_no; i++)
    {
        molecule->bond_ptrs[i] = &(molecule->bonds[i]);
    }
}

/******
 atomCompar:  compares 2 atoms
 In: void pointers to the atoms
 Out: integer comparison
*******/
int atom_comp(const void *a, const void *b)
{
    // converting to atom pointers
    atom **atom_ptr_a, **atom_ptr_b;

    atom_ptr_a = (struct atom **)a;
    atom_ptr_b = (struct atom **)b;

    // computing an int to sort these atoms
    if ((*atom_ptr_a)->z - (*atom_ptr_b)->z < 0.0)
    {
        return -1;
    }
    else if ((*atom_ptr_a)->z - (*atom_ptr_b)->z > 0.0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

/******
 bondCompar:  compares 2 bonds
 In: void pointers to the bonds
 Out: integer comparison
*******/
int bond_comp(const void *a, const void *b)
{
    // converting to bond pointers
    bond **bond_ptr_a, **bond_ptr_b;

    bond_ptr_a = (struct bond **)a;
    bond_ptr_b = (struct bond **)b;

    // computing an int to sort these bonds
    // double avg_Z_a, avg_Z_b;
    // avg_Z_a = ((double)(*bond_ptr_a)->a1->z + (double)(*bond_ptr_a)->a2->z) / 2.0;
    // avg_Z_b = ((double)(*bond_ptr_b)->a1->z + (double)(*bond_ptr_b)->a2->z) / 2.0;

    if ((*bond_ptr_a)->z < (*bond_ptr_b)->z)
    {
        return -1;
    }
    else if ((*bond_ptr_a)->z > (*bond_ptr_b)->z)
    {
        return 1;
    }
    return 0;
}

/******
 molsort:  sorts the atoms and bonds in a molecule
 In: the molecule
 Out: none
*******/
void molsort(molecule *molecule)
{
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom **), atom_comp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond **), bond_comp);
}

/******
 xrotation:  builds a matrix for a rotation in the x-axis
 In: the matrix and the number of degrees
 Out: none
*******/
void xrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * M_PI / 180.0;

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -1.0 * sin(rad);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

/******
 yrotation:  builds a matrix for a rotation in the y-axis
 In: the matrix and the number of degrees
 Out: none
*******/
void yrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * M_PI / 180.0;

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -1.0 * sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

/******
 zrotation:  builds a matrix for a rotation in the z-axis
 In: the matrix and the number of degrees
 Out: none
*******/
void zrotation(xform_matrix xform_matrix, unsigned short deg)
{
    double rad = deg * M_PI / 180.0;

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -1.0 * sin(rad);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

/******
 mol_xform:  applies a transformation matrix to the atoms of a molecule
 In: the matrix and the molecule
 Out: none
*******/
void mol_xform(molecule *molecule, xform_matrix matrix)
{
    double oldX = 0;
    double oldY = 0;
    double oldZ = 0;

    for (int i = 0; i < molecule->atom_no; i++)
    {
        // storing original coords
        oldX = molecule->atoms[i].x;
        oldY = molecule->atoms[i].y;
        oldZ = molecule->atoms[i].z;
        // applying transformation
        molecule->atoms[i].x = matrix[0][0] * oldX + matrix[0][1] * oldY + matrix[0][2] * oldZ;
        molecule->atoms[i].y = matrix[1][0] * oldX + matrix[1][1] * oldY + matrix[1][2] * oldZ;
        molecule->atoms[i].z = matrix[2][0] * oldX + matrix[2][1] * oldY + matrix[2][2] * oldZ;
    }
    for (int i = 0; i < molecule->bond_no; i++)
    {
        // re-compute the coordinates
        compute_coords(&(molecule->bonds[i]));
    }
}
