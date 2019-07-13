import sys,os


file = sys.argv[2]
os.system('echo ' + file + ' >>/root/g1.txt')
file = file.split("/")[3]

upload_file = 'gdrive upload -r /root/Downloads/"%s"' % file
#os.system('echo ' + upload_file + ' >>/root/g1.txt')

os.system(upload_file)
os.system('rm -rf /root/Downloads/"%s"' % file)

   
