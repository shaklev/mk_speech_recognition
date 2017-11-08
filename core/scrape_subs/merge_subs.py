
import glob
all_subs = glob.glob("/home/jme1991/projects/mk_subs_files/*")



for sub_file in all_subs:
	print(sub_file)
	with open(sub_file) as f:
		s = f.read()
		with open('mk_subs.txt', 'a') as file:
	   		file.write(s)
