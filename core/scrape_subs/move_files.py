import os
import os.path
import shutil    

for root, dir, files in os.walk('/home/jme1991/projects/mk_subs/'):
    for ffile in files:
        if os.path.splitext(ffile)[1] in ('.srt'):
            src = os.path.join(root, ffile)
            shutil.copy(src, '/home/jme1991/projects/mk_subs_files/')
