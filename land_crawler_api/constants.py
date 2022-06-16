import os
# Files names
fname_a = 'a_lvr_land_a.csv'
fname_b = 'b_lvr_land_a.csv'
fname_e = 'e_lvr_land_a.csv'
fname_f = 'f_lvr_land_a.csv'
fnames = fname_a, fname_b, fname_e, fname_f

# File directory
file_dir = 'data_set'

# file paths
fpaths = tuple(os.path.join(file_dir, fname) for fname in fnames)

# Named Tuple name
land_class_name = 'LvrLand'


