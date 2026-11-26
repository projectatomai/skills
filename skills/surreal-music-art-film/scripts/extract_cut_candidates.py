#!/usr/bin/env python3
"""Capture sensitive cut candidates; visual classification is still required."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageStat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--threshold', type=float, default=0.045)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    frames = args.output / 'candidates'
    frames.mkdir(exist_ok=True)
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(args.source)]))
    process = subprocess.run([
        'ffmpeg', '-hide_banner', '-y', '-i', str(args.source), '-vf',
        f"select='eq(n,0)+gt(scene,{args.threshold})',metadata=print",
        '-fps_mode', 'passthrough', '-q:v', '2', str(frames / 'candidate-%04d.jpg')],
        capture_output=True, text=True, check=True)
    (args.output / 'scene-scores.log').write_text(process.stderr)
    records = []
    blocks = re.findall(r'frame:\s*(\d+).*?pts_time:([\d.]+)\s*\n([^\n]*)', process.stderr)
    paths = sorted(frames.glob('candidate-*.jpg'))
    if len(paths) != len(blocks):
        raise RuntimeError(f'Frame/timestamp mismatch: {len(paths)} versus {len(blocks)}')
    for path, block in zip(paths, blocks):
        score = re.search(r'lavfi.scene_score=([\d.]+)', block[2])
        with Image.open(path) as picture:
            mean = ImageStat.Stat(picture.convert('L')).mean[0]
        records.append({'candidate': len(records)+1, 'timestamp': float(block[1]),
                        'scene_score': float(score[1]) if score else None,
                        'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'mean_luma': mean, 'status': 'requires_visual_classification'})
    sheets = []
    for start in range(0, len(records), 36):
        subset = records[start:start+36]
        sheet = Image.new('RGB', (6*160, 6*255), '#151515')
        draw = ImageDraw.Draw(sheet)
        for index, record in enumerate(subset):
            x, y = (index%6)*160, (index//6)*255
            with Image.open(record['path']) as picture:
                picture.thumbnail((156, 228))
                sheet.paste(picture, (x+(160-picture.width)//2, y))
            draw.text((x+3, y+231), f"{record['candidate']:03} {record['timestamp']:.3f}s", fill='white')
        name = args.output / f'contact-{start//36+1:02d}.jpg'
        sheet.save(name, quality=90)
        sheets.append(str(name.resolve()))
    manifest = {'source': str(args.source.resolve()),
                'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
                'probe': probe, 'threshold': args.threshold, 'candidate_count': len(records),
                'coverage_status': 'full_decode_candidates_require_visual_cut_audit',
                'candidates': records, 'contact_sheets': sheets}
    (args.output / 'audit.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'source': args.source.name, 'candidates': len(records), 'contacts': sheets}))


if __name__ == '__main__':
    main()
