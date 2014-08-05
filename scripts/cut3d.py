import distutils.spawn
import tempfile, os, numpy
from subprocess import Popen, PIPE, STDOUT

cut3d = distutils.spawn.find_executable('cut3d');

def getden(denfile):
    tf = tempfile.NamedTemporaryFile()
    filepath = os.path.basename(tf.name)
    inp = str(denfile) + "\n1\n0\n5\n" + str(filepath) + "\n0\n"
    p = Popen([cut3d], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_txt = p.communicate(input=inp)[0]
    for line in stdout_txt.split('\n'):
        if 'ngfft(1:3),nkpt' in line:
            ng = line.split()
            ng = map(int,ng[2:5])
        if 'nsppol,nsym,npsp,ntypat' in line:
            nsppol = line.split()
            nsppol = int(nsppol[2])
    data = numpy.loadtxt(filepath)
    os.remove(filepath)
    return data.reshape(ng + [nsppol**2])