import os
os.system('echo "uploading..." >>/root/Downloads/gdrive/uploading...')
a = os.popen('ls -m /root/Downloads/gdrive/').readlines()
os.system('gdrive sync upload /root/Downloads/gdrive/ 1r-uOyLfjWHGwbjvgJ8-6x-3AYyQwg6k8')

#print(a)
a = a[0].split(',')
for i in a :
    i = "'/root/Downloads/gdrive/"+i.strip()+"'"
    print(i)
    os.system("rm -rf %s" %i)

