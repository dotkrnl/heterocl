import os
import heterocl as hcl
from digitrec_main import top, run
import argparse

PLATFORM='sdaccel::xilinx_aws-vu9p-f1-04261818_dynamic_5_0'

code = top('merlinc')

parser = argparse.ArgumentParser(description='Build digitrec kernel for MerlinC')
parser.add_argument('action', choices=['run', 'codegen', 'gcc', 'sw_emu', 'hw_emu', 'hw', 'report', 'clean'])
args = parser.parse_args()

def codegen():
    with open('krnl.cpp', 'w') as f:
        f.write(code)

def gcc():
    clean()
    codegen()
    # Here we use gcc to evaluate the functionality
    os.system('g++ -std=c++11 digitrec_host.cpp krnl.cpp')
    os.system('./a.out')

def emu(target):
    clean()
    codegen()
    # Here we use Merlin to compile kernel for sw emulation
    os.system('merlincc -c krnl.cpp -o krnl --platform=' + PLATFORM)
    os.system('merlincc krnl.mco -march=' + target + ' -o krnl_' + target + ' --platform=' + PLATFORM)
    os.system('g++ -DMCC_ACC -DMCC_ACC_H_FILE=\\"__merlinkrnl.h\\" digitrec_host.cpp libkrnl.so')
    os.system('XCL_EMULATION_MODE=' + target + ' ./a.out krnl_' + target + '.xclbin')

def sw_emu():
    emu('sw_emu')

def hw_emu():
    emu('hw_emu')

def hw():
    clean()
    codegen()
    # Here we use Merlin to compile kernel for sw emulation
    os.system('merlincc -c krnl.cpp -o krnl --platform=' + PLATFORM)
    os.system('merlincc krnl.mco -o krnl --platform=' + PLATFORM)
    os.system('g++ -DMCC_ACC -DMCC_ACC_H_FILE=\\"__merlinkrnl.h\\" digitrec_host.cpp libkrnl.so')

def report():
    clean()
    codegen()
    # Here we use Merlin to show the FPGA performance estimation
    os.system('merlincc -c krnl.cpp -o krnl --platform=' + PLATFORM)
    os.system('merlincc krnl.mco --report=estimate --platform=' + PLATFORM)
    os.system('cat merlin.rpt')

def clean():
    os.system('rm -fR .Mer a.out krnl.mco merlin.rpt merlin.log libkrnl.so __merlinkrnl.h .log_license .merlin_prj/ .run/ *.xclbin emconfig.json')

actions = {
    'run': run,
    'codegen': codegen,
    'gcc': gcc,
    'sw_emu': sw_emu,
    'hw_emu': hw_emu,
    'hw': hw,
    'report': report,
    'clean': clean,
}

actions[args.action]()
