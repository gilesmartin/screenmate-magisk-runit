#!/usr/bin/env python3
"""Owner-only private script export. Never copy this output to a public repo."""
import argparse,pathlib,subprocess,os,json,hashlib
ALLOWLIST=('start-supervisor.sh','services/magisk/run','magisk/bin/magisk-service.sh','magisk/bin/magisk-boot-gate.sh','magisk/bin/magisk-recover.sh')
EXCLUDED=('policies','databases','keys','APK/stub','VPN','logs','binaries','raw SELinux policy','full unrelated boot watchdog')
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--adb',default='adb');p.add_argument('--serial',required=True);p.add_argument('--destination',required=True);a=p.parse_args();dest=pathlib.Path(a.destination).expanduser().absolute();repo=pathlib.Path(__file__).resolve().parents[1]
if dest.resolve().is_relative_to(repo):p.error('Private backup must be outside the repository.')
if dest.exists():p.error('Refusing existing destination; create a fresh private backup path.')
# Check every input before creating the backup. No recursion or arbitrary remote path input.
contents={}
for name in ALLOWLIST:
 remote='/data/local/screenmate-services/'+name
 command='test -f '+remote+' && test ! -L '+remote+' && cat '+remote
 try:r=subprocess.run([a.adb,'-s',a.serial,'exec-out',command],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
 except (OSError,subprocess.TimeoutExpired):p.error('Read-only export transport failed; no device changes made.')
 if r.returncode or not r.stdout.startswith(b'#!/')or len(r.stdout)>262144:p.error('Allowlisted script unavailable or unexpected payload.')
 if b'PRIVATE KEY-----'in r.stdout:p.error('Unexpected key marker in script; refusing export.')
 r.stdout.decode('utf-8');contents[name]=r.stdout
os.umask(0o077);dest.mkdir(mode=0o700,parents=True);manifest={}
for name,data in contents.items():
 path=dest/name;path.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
 with path.open('xb')as f:f.write(data)
 path.chmod(0o600);manifest[name]=hashlib.sha256(data).hexdigest()
(dest/'PRIVATE-MANIFEST.json').write_text(json.dumps({'private':True,'scripts':manifest,'excluded':EXCLUDED,'device_modified':False},indent=2)+'\n');print('Private owner backup completed. Never publish its contents.')
