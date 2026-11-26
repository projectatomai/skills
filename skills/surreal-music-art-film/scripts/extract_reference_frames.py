#!/usr/bin/env python3
"""Extract local reference frames without uploading or generating anything."""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--output', type=Path, required=True,
                        help='New reference directory; existing manifests are not overwritten')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--count', type=int, default=None,
                       help='Uniform sample count, default 24; visual review still required')
    group.add_argument('--times', nargs='+', type=float,
                       help='Explicit timestamps in seconds')
    args = parser.parse_args()
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        parser.error('FFmpeg and FFprobe must already be installed')
    video = args.video.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not video.is_file():
        parser.error(f'Video not found: {video}')
    if output.exists() and any(output.iterdir()):
        parser.error('Output directory is nonempty; reuse its manifest or choose a new directory')
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_format',
                            '-show_streams', '-of', 'json', str(video)]))
    stream = next((s for s in probe.get('streams', [])
                   if s.get('codec_type') == 'video'), None)
    if not stream:
        parser.error('Source has no video stream')
    duration = float(probe.get('format', {}).get('duration') or stream.get('duration') or 0)
    if not math.isfinite(duration) or duration <= 0:
        parser.error('Source duration is unavailable or invalid')
    if args.times is not None:
        timestamps = sorted(set(args.times))
        if not timestamps or any(not math.isfinite(t) or t < 0 or t >= duration
                                 for t in timestamps):
            parser.error('Timestamps must be finite seconds from zero up to source duration')
        method = 'explicit timestamps'
    else:
        count = args.count if args.count is not None else 24
        if count < 1 or count > 1000:
            parser.error('Count must be between 1 and 1000')
        timestamps = [duration * (i + 0.5) / count for i in range(count)]
        method = 'uniform sample-bin midpoints'
    output.mkdir(parents=True, exist_ok=True)
    frames_dir = output / 'frames'
    frames_dir.mkdir()
    manifest = {'source': str(video), 'duration_seconds': duration,
                'source_dimensions': [stream.get('width'), stream.get('height')],
                'sampling_method': method, 'status': 'extracting',
                'visual_review_complete': False, 'uploaded': False,
                'frames': []}
    manifest_path = output / 'reference-manifest.json'
    def save():
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    save()
    seen = {}
    try:
        for index, timestamp in enumerate(timestamps, 1):
            frame = frames_dir / f'frame-{index:03d}.jpg'
            run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin',
                 '-ss', f'{timestamp:.9f}', '-i', str(video), '-map', '0:v:0',
                 '-frames:v', '1', '-q:v', '2', '-n', str(frame)])
            if not frame.is_file() or not frame.stat().st_size:
                raise RuntimeError(f'No frame captured at {timestamp:.6f} seconds')
            digest = hashlib.sha256(frame.read_bytes()).hexdigest()
            item = {'id': f'{index:03d}', 'timestamp_seconds': timestamp,
                    'file': str(frame), 'sha256': digest,
                    'visual_review_complete': False, 'selected': False,
                    'uploaded': False}
            if digest in seen:
                item['identical_to'] = seen[digest]
            else:
                seen[digest] = item['id']
            manifest['frames'].append(item)
            save()
    except Exception as exc:
        manifest['status'] = 'failed'
        manifest['error'] = str(exc)
        save()
        raise
    manifest['status'] = 'extracted'
    manifest['frame_count'] = len(manifest['frames'])
    manifest['unique_file_hash_count'] = len(seen)
    save()
    print(json.dumps({'manifest': str(manifest_path),
                      'frames': len(manifest['frames']),
                      'unique_hashes': len(seen),
                      'next': 'Visually review frames; extraction does not upload them.'}))


if __name__ == '__main__':
    try:
        main()
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print(getattr(exc, 'stderr', None) or str(exc), file=sys.stderr)
        sys.exit(1)
