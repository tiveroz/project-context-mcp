from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import yaml

class SubmissionTests(unittest.TestCase):
    def test_manifest_requires_real_public_pin(self):
        script=Path('submission/render_manifest.py').resolve()
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'manifest.yaml'
            bad=subprocess.run([sys.executable,str(script),'--repo','example/project-context-mcp','--commit','main','--output',str(output)],capture_output=True)
            self.assertNotEqual(bad.returncode,0)
            self.assertFalse(output.exists())
            good=subprocess.run([sys.executable,str(script),'--repo','example/project-context-mcp','--commit','a'*40,'--output',str(output)],capture_output=True)
            self.assertEqual(good.returncode,0,good.stderr)
            manifest=yaml.safe_load(output.read_text())
            self.assertEqual(manifest['install']['ref'],'a'*40)
            self.assertEqual(manifest['auth']['type'],'none')
            self.assertFalse(manifest['auth']['env'][0]['secret'])
            self.assertEqual(len(manifest['tools']['default_enabled']),6)
            self.assertEqual(manifest['transport']['type'],'stdio')
            duplicate=subprocess.run([sys.executable,str(script),'--repo','example/project-context-mcp','--commit','a'*40,'--output',str(output)],capture_output=True)
            self.assertNotEqual(duplicate.returncode,0)
