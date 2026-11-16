"""Render a proposed MCP catalogue entry after the public source commit exists."""
import argparse
from pathlib import Path
import re

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,help='Public owner/project-context-mcp')
    p.add_argument('--commit',required=True,help='Full immutable public source SHA')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/project-context-mcp',a.repo):p.error('Expected owner/project-context-mcp')
    if not re.fullmatch(r'[a-f0-9]{40}',a.commit) or a.commit=='0'*40:p.error('Expected non-zero full commit SHA')
    text=(Path(__file__).parent/'manifest.yaml.in').read_text()
    text=text.replace('REPOSITORY_OWNER/project-context-mcp',a.repo).replace('PUBLIC_SOURCE_COMMIT_REQUIRED',a.commit)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as f:f.write(text)
