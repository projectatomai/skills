#!/usr/bin/env python3
"""Check and reserve exact source images before paid or queued animation work."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def source_key(url=None, file=None):
    """Return one stable key per exact source image, so the same image is never animated twice by accident."""
    if file:
        return 'sha256:' + hashlib.sha256(Path(file).read_bytes()).hexdigest()
    parsed = urlparse(url or '')
    if parsed.scheme != 'https' or not parsed.hostname:
        raise ValueError('Use the exact https link of the source image, or a local source file.')
    # Midjourney links come in two shapes for the same image, so fold them into one key.
    match = re.search(r'/jobs/([0-9a-f-]{36})', parsed.path, re.I)
    if match and parsed.hostname.endswith('midjourney.com'):
        index = parse_qs(parsed.query).get('index', [None])[0]
        if index is None:
            raise ValueError('Source image URL needs its exact index; a set ID alone is insufficient.')
        return f'midjourney:{match[1].lower()}:{int(index)}'
    match = re.search(r'/([0-9a-f-]{36})/0_(\d+)(?:[_.])', parsed.path, re.I)
    if match and parsed.hostname == 'cdn.midjourney.com':
        return f'midjourney:{match[1].lower()}:{int(match[2])}'
    # Any other generator: the host, path and query together name the image.
    query = ('?' + parsed.query) if parsed.query else ''
    return 'url:' + parsed.hostname.lower() + parsed.path + query


def job_id(url):
    """Return a stable id for an observed video job link from any service."""
    parsed = urlparse(url or '')
    if parsed.scheme != 'https' or not parsed.hostname:
        return None
    match = re.search(r'/jobs/([0-9a-f-]{36})', parsed.path, re.I)
    if match:
        return match[1].lower()
    query = ('?' + parsed.query) if parsed.query else ''
    return parsed.hostname.lower() + parsed.path + query


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'reserve', 'complete'])
    parser.add_argument('--registry', required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--source-url')
    source.add_argument('--source-file')
    parser.add_argument('--video-job-url', action='append', default=[])
    args = parser.parse_args()
    path = Path(args.registry)
    key = source_key(args.source_url, args.source_file)
    registry = json.loads(path.read_text()) if path.exists() else {'schema_version': 1, 'sources': {}}
    entry = registry['sources'].get(key)
    active = entry and entry.get('status') in {'reserved', 'submitted', 'queued', 'rendering', 'completed'}
    if args.action in {'check', 'reserve'} and active:
        print(json.dumps({'allowed': False, 'source_key': key, 'status': entry['status'], 'reason': 'Already used or reserved; a repeat needs an explicit human request.', 'video_jobs': entry.get('video_jobs', [])}, indent=2))
        return 2
    if args.action == 'check':
        print(json.dumps({'allowed': True, 'source_key': key, 'status': 'unused'}))
        return 0
    now = datetime.now(timezone.utc).isoformat()
    if args.action == 'complete' and not args.video_job_url:
        parser.error('Complete requires an observed --video-job-url.')
    entry = entry or {'source_key': key, 'video_jobs': []}
    entry.update({'status': 'reserved' if args.action == 'reserve' else 'completed', 'updated_at': now})
    if args.source_url:
        entry['source_image_url'] = args.source_url
    if args.source_file:
        entry['source_file'] = str(Path(args.source_file).resolve())
    for url in args.video_job_url:
        observed = job_id(url)
        if not observed:
            parser.error('Video job URL must be the https link of a job you observed.')
        if not any(v.get('job_id') == observed for v in entry['video_jobs']):
            entry['video_jobs'].append({'job_id': observed, 'url': url, 'status': 'completed', 'observed_at': now})
    registry['sources'][key] = entry
    registry['updated_at'] = now
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(registry, indent=2) + '\n')
    temporary.replace(path)
    print(json.dumps({'source_key': key, 'status': entry['status']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
