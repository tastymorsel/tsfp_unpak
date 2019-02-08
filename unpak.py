import struct, sys, gzip, os, shutil

if (len(sys.argv) < 2 or sys.argv[1] == "--help"):
    print "unpak.py [pakfilename] [optional_c2n_filename]"
    sys.exit(0)

f = open(sys.argv[1], "rb")
header = f.read(12)
magic0, magic1, magic2, magic3, offset, length = struct.unpack("ccccii", header)

c2n_file = {}
if (len(sys.argv) == 3):
    with open(sys.argv[2], "r") as c2n:
        z = c2n.readlines()
        for n in z:
            crc,name = n.split()
            c2n_file[crc] = name.replace('/', '_')

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
    outname = "{0:#0{1}x}".format(fi[0], 10)
    print ':' + outname + ':'
    if (c2n_file.has_key(outname)):
        outname = c2n_file[outname]
    if (fi[3] == 0):
        fd = f.read(fi[2])
        with open("./unpak/" + outname, "wb") as o:
            o.write(fd)
    else:
        fd = f.read(fi[3])
        with open("temp.gz", "wb") as g:
            g.write(fd)
            g.close()
        with gzip.open("temp.gz", "rb") as gz:
            data = gz.read()
            with open("./unpak/" + outname, "wb") as o:
                o.write(data)       

f.close()
