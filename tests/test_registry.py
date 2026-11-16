import copy
import json
from pathlib import Path
import tempfile
import unittest
from project_context import Registry,bounded,MAX_FILE

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'registry.json'
        self.data=json.loads(Path('examples/registry.json').read_text())
        self.write()
        self.registry=Registry(self.path)
    def write(self):self.path.write_text(json.dumps(self.data),encoding='utf-8')
    def test_pagination(self):
        page=self.registry.list_projects(limit=2)
        self.assertEqual(page['next_offset'],2)
        self.assertEqual(len(self.registry.list_projects(offset=2)['projects']),1)
    def test_exact_resolution(self):self.assertEqual(self.registry.resolve_project('research')['total'],1)
    def test_context_marks_demo(self):self.assertEqual(self.registry.context('research')['mode'],'synthetic-demo')
    def test_cycle_terminates(self):self.assertEqual(self.registry.impacts('research')['project_ids'],['documentation','product'])
    def test_proposed_differs_from_pending(self):
        self.assertEqual({r['state'] for r in self.registry.pending('research')['items']},{'proposed-dependency','awaiting-acknowledgement'})
    def test_receipt_clears_only_actual_consumer(self):
        self.data['acknowledgements']=[{'release':'research-v1','consumer':'documentation','evidence':'Synthetic fixture'}]
        self.write();self.assertTrue(all(r['state']=='proposed-dependency' for r in self.registry.pending('research')['items']))
    def test_draft_pointer_rejected(self):
        self.data['releases']['research-v1']['state']='draft';self.write()
        with self.assertRaises(ValueError):self.registry.read()
    def test_unknown_edge_rejected(self):
        self.data['dependencies'][0]['to']='missing';self.write()
        with self.assertRaises(ValueError):self.registry.read()
    def test_unknown_project_does_not_become_file_read(self):
        with self.assertRaises(ValueError):self.registry.context('../secret')
    def test_rejects_large_file(self):
        self.path.write_bytes(b' '*(MAX_FILE+1))
        with self.assertRaises(ValueError):self.registry.read()
    def test_rejects_large_output(self):
        with self.assertRaises(ValueError):bounded({'text':'x'*13000})
    def test_read_queries_do_not_modify_file(self):
        before=self.path.read_bytes();self.registry.context('research');self.registry.impacts('research')
        self.assertEqual(before,self.path.read_bytes())
    def test_unknown_record_kind_rejected(self):
        with self.assertRaises(ValueError):self.registry.record('files','anything')
    def test_live_reload_of_explicit_file(self):
        self.data['projects']['research']['title']='Updated example';self.write()
        self.assertEqual(self.registry.resolve_project('research')['matches'][0]['title'],'Updated example')
