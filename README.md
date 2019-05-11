"#addepar" 

Code requires Python 3.4 or higher. Please install Python 3 through https://www.python.org/

Run instructions
================
Run this code as follows: python <path to this folder>/src/merge_files.py <input_path> <output_file_path>.

Analysis of Computational Complexity
====================================
O(m*n log n) - where 'm' is avg number of lines in files and 'n' is number of files.

This solution uses a mergesort-ish algorithm to combine files. For each file it needs 
to also read through all the lines.

Analysis of Space Complexity
============================
O(n) - where 'n' is number of files.

Since problem places heavy emphasis on RAM, we write intermediate output to the hard disk 
on a temporary storage space which gets automatically cleared at the end of the run. We only
ever store an array of the intermediate file names and it can never exceed the total number
of initial input files.