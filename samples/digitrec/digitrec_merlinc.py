import os
import heterocl as hcl
from digitrec_main import top

code = top('merlinc')
with open('krnl.cpp', 'w') as f:
    f.write(code)

# Here we use gcc to evaluate the functionality
os.system('g++ -std=c++11 digitrec_host.cpp krnl.cpp')
os.system('./a.out')
os.system('rm a.out')

# Here we use Merlin to show the FPGA performance estimation
os.system('merlincc -c krnl.cpp -o krnl --platform=sdaccel::xilinx_aws-vu9p-f1-04261818_dynamic_5_0')
os.system('merlincc krnl.mco --report=estimate --platform=sdaccel::xilinx_aws-vu9p-f1-04261818_dynamic_5_0')
os.system('cat merlin.rpt')
os.system('rm -R .Mer krnl.mco merlin.rpt merlin.log libkrnl.so __merlinkrnl.h')
