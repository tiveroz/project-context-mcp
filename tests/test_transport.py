import json
from pathlib import Path
import sys
import unittest

class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_stdio_tools_are_read_only(self):
        from mcp import ClientSession,StdioServerParameters
        from mcp.client.stdio import stdio_client
        path=Path('examples/registry.json').resolve();before=path.read_bytes()
        params=StdioServerParameters(command=sys.executable,args=[str(Path('server.py').resolve()),'--registry',str(path)])
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as client:
                await client.initialize()
                tools=await client.list_tools()
                self.assertEqual(len(tools.tools),6)
                self.assertTrue(all(t.annotations.readOnlyHint for t in tools.tools))
                cases=[('list_projects',{},'total'),('resolve_project',{'query':'research'},'matches'),
                       ('get_project_context',{'project_id':'research'},'project'),
                       ('get_record',{'kind':'releases','record_id':'research-v1'},'record'),
                       ('list_impacts',{'project_id':'research'},'project_ids'),
                       ('list_pending',{'project_id':'research'},'items')]
                for name,args,field in cases:
                    r=await client.call_tool(name,args)
                    self.assertFalse(r.isError,name)
                    self.assertIn(field,json.loads(r.content[0].text))
                bad=await client.call_tool('get_record',{'kind':'files','record_id':'../secret'})
                self.assertTrue(bad.isError)
        self.assertEqual(before,path.read_bytes())
