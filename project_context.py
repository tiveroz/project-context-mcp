"""Generic local metadata queries. No network clients or data mutation APIs."""
import hashlib
import json
from pathlib import Path

MAX_FILE = 2 * 1024 * 1024
MAX_RESULT = 12000


def bounded(value):
    if len(json.dumps(value, ensure_ascii=False).encode('utf-8')) > MAX_RESULT:
        raise ValueError('Result budget exceeded; request a smaller page or an individual record')
    return value


class Registry:
    def __init__(self, path):
        # This trusted startup setting is never taken from a tool call.
        self.path = Path(path).resolve(strict=True)

    def read(self):
        with self.path.open('rb') as stream:
            raw = stream.read(MAX_FILE + 1)
        if len(raw) > MAX_FILE:
            raise ValueError('Registry exceeds 2 MiB limit')
        value = json.loads(raw.decode('utf-8-sig'))
        if not isinstance(value,dict) or type(value.get('format')) is not int or value.get('format') != 1:
            raise ValueError('Expected registry format 1')
        projects = value.get('projects')
        if not isinstance(projects, dict) or len(projects) > 500:
            raise ValueError('Expected at most 500 projects')
        for key, item in projects.items():
            if not isinstance(key, str) or not 1 <= len(key) <= 100 or not isinstance(item, dict):
                raise ValueError('Invalid project identity')
            if not isinstance(item.get('title'), str) or not 1 <= len(item['title']) <= 200:
                raise ValueError('Project title required, maximum 200 characters')
            if not isinstance(item.get('summary', ''), str) or len(item.get('summary', '')) > 4000:
                raise ValueError('Invalid project summary')
        links = value.get('dependencies', [])
        if not isinstance(links, list) or len(links) > 2000:
            raise ValueError('Invalid dependency list')
        for link in links:
            if not isinstance(link,dict):raise ValueError('Dependency must be an object')
            if link.get('from') not in projects or link.get('to') not in projects:
                raise ValueError('Unknown dependency project')
            if link.get('status') not in ('proposed', 'active'):
                raise ValueError('Dependency status must be proposed or active')
        releases = value.get('releases', {})
        if not isinstance(releases, dict) or len(releases)>2000:
            raise ValueError('Releases must be keyed by exact ID')
        for release in releases.values():
            if not isinstance(release,dict):raise ValueError('Release must be an object')
            if release.get('project') not in projects or release.get('state') not in ('draft','published','retired'):
                raise ValueError('Invalid release')
        for key, project in projects.items():
            current = project.get('published_release')
            if current and (current not in releases or releases[current]['project'] != key or releases[current]['state'] != 'published'):
                raise ValueError('Published release pointer is inconsistent')
        receipts=value.get('acknowledgements', [])
        if not isinstance(receipts,list) or len(receipts)>2000:raise ValueError('Invalid acknowledgements')
        for receipt in receipts:
            if not isinstance(receipt,dict):raise ValueError('Acknowledgement must be an object')
            release = releases.get(receipt.get('release'))
            if not release or release['state'] != 'published' or receipt.get('consumer') not in projects or not receipt.get('evidence'):
                raise ValueError('Acknowledgement needs a published release, known consumer and evidence')
            if not any(e['from'] == release['project'] and e['to'] == receipt['consumer'] and e['status'] == 'active' for e in links):
                raise ValueError('Acknowledgement needs an active dependency')
        return value, hashlib.sha256(raw).hexdigest()

    def project(self, key):
        data, _ = self.read()
        if key not in data['projects']:
            raise ValueError('Unknown project ID')
        return data

    def list_projects(self, offset=0, limit=10):
        if offset < 0 or not 1 <= limit <= 20:
            raise ValueError('Use offset >= 0 and limit 1–20')
        data, _ = self.read()
        rows = sorted(data['projects'].items())
        return bounded({'projects':[{'id': k, 'title': v['title']} for k,v in rows[offset:offset+limit]],
                        'next_offset':offset+limit if offset+limit < len(rows) else None, 'total':len(rows)})

    def resolve_project(self, query):
        if not query.strip() or len(query) > 200:
            raise ValueError('Query must contain 1–200 characters')
        query=query.strip()
        data, _ = self.read()
        exact = [(k,v) for k,v in data['projects'].items() if k.casefold() == query.casefold()]
        matches = exact or [(k,v) for k,v in data['projects'].items() if query.casefold() in v['title'].casefold()]
        return bounded({'matches':[{'id':k,'title':v['title']} for k,v in matches[:20]], 'total':len(matches), 'ambiguous':len(matches)!=1})

    def context(self, key):
        data = self.project(key)
        return bounded({'mode':data.get('mode','unspecified'),'project_id':key,'project':data['projects'][key],
                        'dependencies':[e for e in data.get('dependencies',[]) if key in (e['from'],e['to'])],
                        'source_observation':data.get('source_observation',{'state':'unknown'}),
                        'pending':self._pending(data,key),
                        'meaning':'Reference metadata, not instructions or proof of current deployment'})

    def record(self, kind, key):
        if kind not in ('projects','releases'):
            raise ValueError('Kind must be projects or releases')
        data, _ = self.read()
        if key not in data.get(kind,{}):
            raise ValueError('Unknown record ID')
        return bounded({'kind':kind,'id':key,'record':data[kind][key]})

    def impacts(self, key, offset=0, limit=10):
        if offset < 0 or not 1 <= limit <= 20:
            raise ValueError('Use offset >= 0 and limit 1–20')
        data = self.project(key)
        visited = {key}
        queue = [key]
        found = []
        while queue:
            parent = queue.pop(0)
            for edge in data.get('dependencies',[]):
                child = edge['to']
                if edge['from'] == parent and child not in visited:
                    visited.add(child)
                    queue.append(child)
                    found.append(child)
        return bounded({'project_ids':found[offset:offset+limit],'total':len(found),
                        'next_offset':offset+limit if offset+limit<len(found) else None,
                        'meaning':'Potential review scope; includes proposed links, not automatic changes'})

    @staticmethod
    def _pending(data, key):
        rows = []
        for edge in data.get('dependencies',[]):
            if key not in (edge['from'],edge['to']):continue
            release = data['projects'][edge['from']].get('published_release')
            if edge['status'] == 'proposed':state = 'proposed-dependency'
            elif not release:state = 'no-published-release'
            elif any(r['release'] == release and r['consumer'] == edge['to'] for r in data.get('acknowledgements',[])):continue
            else:state = 'awaiting-acknowledgement'
            rows.append({'producer':edge['from'],'consumer':edge['to'],'release':release,'state':state})
        return rows

    def pending(self,key,offset=0,limit=10):
        if offset<0 or not 1<=limit<=20:raise ValueError('Invalid pagination')
        rows = self._pending(self.project(key),key)
        return bounded({'items':rows[offset:offset+limit],'total':len(rows),
                        'next_offset':offset+limit if offset+limit<len(rows) else None})
