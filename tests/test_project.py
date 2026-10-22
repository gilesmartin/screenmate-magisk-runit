import unittest, subprocess, pathlib, json, tempfile, os, re
R=pathlib.Path(__file__).resolve().parents[1]
class ProjectTests(unittest.TestCase):
 def plan(self,action):return subprocess.run(['sh',str(R/'scripts'/ (action+'.sh'))],capture_output=True,text=True)
 def test_install_plan_idempotent(self):
  a=self.plan('install');b=self.plan('install');self.assertEqual(a.returncode,0,a.stderr);self.assertEqual(a.stdout,b.stdout);x=json.loads(a.stdout);self.assertFalse(x['executes_device_changes']);self.assertEqual(x['action'],'install');self.assertTrue(x['steps'])
 def test_uninstall_plan_idempotent(self):
  a=self.plan('uninstall');b=self.plan('uninstall');self.assertEqual(a.returncode,0,a.stderr);self.assertEqual(a.stdout,b.stdout);self.assertFalse(json.loads(a.stdout)['executes_device_changes'])
 def test_apply_not_supported(self):
  for action in ['install','uninstall']:
   p=subprocess.run(['sh',str(R/'scripts'/(action+'.sh')),'--apply'],capture_output=True,text=True);self.assertNotEqual(p.returncode,0)
 def test_plans_cannot_invoke_tools(self):
  with tempfile.TemporaryDirectory()as d:
   fake=pathlib.Path(d)/'adb';marker=pathlib.Path(d)/'called';fake.write_text('#!/bin/sh\ntouch "'+str(marker)+'"\nexit 99\n');fake.chmod(0o700)
   for action in ['install','uninstall']:
    p=subprocess.run(['sh',str(R/'scripts'/(action+'.sh'))],env=dict(os.environ,PATH=d+os.pathsep+os.environ['PATH']),capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr)
   self.assertFalse(marker.exists())
 def test_reference_scripts_fail_before_any_original_command(self):
  for f in (R/'reference').rglob('*.in'):
   p=subprocess.run(['sh',str(f)],env=dict(os.environ,SCREENMATE_REVIEWED_REFERENCE=''),capture_output=True,text=True);self.assertEqual(p.returncode,64,str(f)+p.stderr)
 def test_shell_syntax(self):
  for f in list(R.rglob('*.sh'))+list(R.rglob('*.in'))+[R/'reference/services/magisk/run.in']:
   p=subprocess.run(['sh','-n',str(f)],capture_output=True,text=True);self.assertEqual(p.returncode,0,str(f)+p.stderr)
 def test_no_device_policy_pin(self):
  for f in [R/'reference/magisk/bin/magisk-service.sh.in',R/'reference/magisk/bin/magisk-recover.sh.in']:
   t=f.read_text();self.assertIn('EXPECTED=__LOCAL_POLICY_SHA256_REQUIRED__',t);self.assertNotRegex(t,r'EXPECTED=[a-f0-9]{64}')
 def test_doctor_is_observational(self):
  t=(R/'scripts/doctor.sh').read_text();self.assertNotRegex(t,r'(?m)^\s*(?:mount|umount|kill|touch|chmod|chown|setprop|rm|cp|mv)\b');self.assertNotIn('--live',t);self.assertNotIn('--sqlite',t)
 def test_private_export_uses_exact_allowlist(self):
  t=(R/'scripts/private-export.py').read_text();self.assertNotIn('rglob(',t);self.assertNotIn('tar ',t);self.assertIn('EXCLUDED',t)
 def test_export_with_fake_adb_and_private_destination(self):
  with tempfile.TemporaryDirectory()as d:
   d=pathlib.Path(d);a=d/'adb';a.write_text('#!/bin/sh\nprintf "#!/system/bin/sh\\nprintf harmless\\\\n\\n"\n');a.chmod(0o700);dest=d/'private';p=subprocess.run(['python3',str(R/'scripts/private-export.py'),'--adb',str(a),'--serial','fixture','--destination',str(dest)],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);files=list(dest.rglob('*.sh'))+list(dest.rglob('run'));self.assertEqual(len(files),5);self.assertEqual(dest.stat().st_mode&0o777,0o700)
   p=subprocess.run(['python3',str(R/'scripts/private-export.py'),'--adb',str(a),'--serial','fixture','--destination',str(dest)],capture_output=True,text=True);self.assertNotEqual(p.returncode,0)
 def test_export_refuses_repo_destination(self):
  p=subprocess.run(['python3',str(R/'scripts/private-export.py'),'--serial','fixture','--destination',str(R/'forbidden-backup')],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertFalse((R/'forbidden-backup').exists())
 def test_markdown_local_links(self):
  for f in R.rglob('*.md'):
   for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
    if '://'not in link and not link.startswith('#'):self.assertTrue((f.parent/link.split('#')[0]).exists(),str(f)+': '+link)
 def test_privacy_and_no_binaries(self):
  bad=[r'mart'+r'ins\.ink',r'robe'+r'rtmartin',r'co\.puppy'+r'port\.boot',r'\b'+str(10200+59)+r'\b',r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----\s+[A-Za-z0-9+/=]{64,}']
  for f in R.rglob('*'):
   if not f.is_file()or'.git'in f.parts or'__pycache__'in f.parts:continue
   self.assertNotIn(f.suffix,['.apk','.so','.deb','.db','.bin','.jks','.pk8','.p12']);data=f.read_bytes();self.assertFalse(data.startswith(b'\x7fELF'));text=data.decode()
   for pattern in bad:self.assertIsNone(re.search(pattern,text),str(f))
 def test_claims_owner_reboot_not_new_test(self):
  t=(R/'docs/testing.md').read_text();self.assertIn('owner-reported',t);self.assertIn('several successful reboots',t);self.assertIn('No reboot was performed',t)
if __name__=='__main__':unittest.main()
