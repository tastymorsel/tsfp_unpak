import struct, sys, gzip, os, shutil

if (len(sys.argv) < 2 or sys.argv[1] == "--help"):
    print "unpak.py [pakfilename]"
    sys.exit(0)

f = open(sys.argv[1], "rb")
header = f.read(12)
magic0, magic1, magic2, magic3, offset, length = struct.unpack("ccccii", header)

if (magic0 != 'P' or magic1 != '5' or magic2 != 'C' or magic3 != 'K'):
    print "This doesn't look like a pak file."
    sys.exit(-1)

if (os.path.exists("./unpak") and os.path.isdir("./unpak")):
    print "Output folder already exists."
    sys.exit(-1)

os.makedirs("./unpak")

f.seek(offset, 0)

single_file_struct = struct.Struct("Iiii")
num_files = length / single_file_struct.size

file_infos = []

for n in range(num_files):
    this_file = f.read(single_file_struct.size)
    filename, filepos, filelen, compresslen = single_file_struct.unpack(this_file)
    file_infos.append((filename,filepos,filelen,compresslen))

for fi in file_infos:
    f.seek(fi[1])
    if (fi[3] == 0):
        fd = f.read(fi[2])
        with open("./unpak/" + hex(fi[0]), "wb") as o:
            o.write(fd)
    else:
        fd = f.read(fi[3])
        with open("temp.gz", "wb") as g:
            g.write(fd)
            g.close()
        with gzip.open("temp.gz", "rb") as gz:
            data = gz.read()
            with open("./unpak/" + hex(fi[0]), "wb") as o:
                o.write(data)       

f.close()
