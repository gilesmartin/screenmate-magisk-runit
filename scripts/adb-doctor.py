#!/usr/bin/env python3
"""Run the fixed read-only doctor through an already authorized ADB transport."""
import argparse,pathlib,subprocess,sys
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--adb',default='adb');p.add_argument('--serial',required=True);a=p.parse_args()
try:
 r=subprocess.run([a.adb,'-s',a.serial,'shell','/system/bin/sh'],input=(pathlib.Path(__file__).with_name('doctor.sh')).read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25)
except (OSError,subprocess.TimeoutExpired):sys.exit('Authorized ADB transport unavailable; no recovery actions attempted.')
if r.returncode:sys.exit('Read-only doctor failed; no device changes attempted.')
sys.stdout.buffer.write(r.stdout)
