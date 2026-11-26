"""All-frame motion screen. Flags require viewed review; never auto-approve a video."""
import argparse
import hashlib
import json
import statistics
import subprocess
import time
from pathlib import Path
from PIL import Image, ImageChops, ImageStat


def inspect(clip, expected_frames=None, expected_fps=None):
    clip = Path(clip).resolve()
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(clip)]))
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = 192 if video['width'] >= video['height'] else 108
    height = max(2, round(width * video['height'] / video['width']))
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(clip),
        '-vf', f'scale={width}:{height}', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'], capture_output=True)
    size = width * height
    frames = [Image.frombytes('L', (width, height), decoded.stdout[i:i+size])
        for i in range(0, len(decoded.stdout)-size+1, size)]
    numerator, denominator = map(int, video['avg_frame_rate'].split('/'))
    fps = numerator / denominator if denominator else 0
    reasons = []
    if decoded.returncode or decoded.stderr.strip() or len(decoded.stdout) % size or len(frames) < 2:
        reasons.append('decode_error_or_incomplete_video')
    if expected_frames is not None and len(frames) != expected_frames:
        reasons.append('unexpected_frame_count')
    if expected_fps is not None and abs(fps-expected_fps) > 0.001:
        reasons.append('unexpected_frame_rate')
    deltas = [ImageStat.Stat(ImageChops.difference(a,b)).mean[0] for a,b in zip(frames, frames[1:])]
    span = [ImageStat.Stat(ImageChops.difference(frames[0],f)).mean[0] for f in frames[1:]] if frames else []
    mean_delta = statistics.mean(deltas) if deltas else 0
    max_from_first = max(span, default=0)
    longest = run = 1
    for delta in deltas:
        run = run+1 if delta < 0.015 else 1
        longest = max(longest, run)
    if max_from_first < 1.5 and mean_delta < 0.30:
        reasons.append('very_low_motion_suspected')
    if longest >= max(2, round(fps)):
        reasons.append('one_second_freeze_suspected')
    if deltas and max(deltas) > max(12.0, statistics.median(deltas)*15):
        reasons.append('abrupt_frame_jump_suspected')
    return dict(path=str(clip), sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),
        checked_at=time.time(), decoded_frames=len(frames), fps=fps,
        dimensions=[video['width'],video['height']], screen_dimensions=[width,height],
        mean_adjacent_luma_delta=mean_delta, max_from_first_luma_delta=max_from_first,
        longest_near_identical_run=longest, frame_deltas=deltas,
        flagged=bool(reasons), reasons=reasons, visual_review_required=True,
        automatic_acceptance=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('clip', type=Path)
    parser.add_argument('--expected-frames', type=int)
    parser.add_argument('--expected-fps', type=float)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.clip, args.expected_frames, args.expected_fps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_suffix('.tmp')
    temp.write_text(json.dumps(result, indent=2)); temp.replace(args.output)
    print(json.dumps({k:result[k] for k in ['path','decoded_frames','flagged','reasons']}))
    raise SystemExit(2 if result['flagged'] else 0)
