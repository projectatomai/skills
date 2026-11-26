#!/usr/bin/env python3
"""Report decoded audio sample-clock differences. Does not measure mouth sync."""
import argparse,json,subprocess
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--threshold-ms',type=float,default=2);a=p.parse_args()
def probe(opts):return json.loads(subprocess.check_output(['ffprobe','-v','error',*opts,'-of','json',a.video]))
streams=probe(['-show_streams'])['streams'];audio=next((s for s in streams if s['codec_type']=='audio'),None)
if audio is None:raise SystemExit('No audio stream')
sr=int(audio['sample_rate']);frames=probe(['-select_streams','a:0','-show_frames','-show_entries','frame=best_effort_timestamp_time,nb_samples'])['frames']
n=0;initial=None;previous=0;changes=[];offsets=[]
for f in frames:
 if 'best_effort_timestamp_time' not in f:raise SystemExit('Missing decoded timestamps')
 t=float(f['best_effort_timestamp_time']);offset=t-n/sr
 if initial is None:initial=offset;previous=offset
 offsets.append(offset)
 if abs(offset-previous)*1000>a.threshold_ms:
  changes.append({'at_seconds':round(t,6),'offset_ms':round(offset*1000,3)});previous=offset
 n+=int(f['nb_samples'])
if not offsets:raise SystemExit('No decoded audio frames')
print(json.dumps({'file':a.video,'sample_rate':sr,'decoded_samples':n,'decoded_seconds':n/sr,'initial_offset_ms':initial*1000,'final_offset_ms':offsets[-1]*1000,'offset_span_ms':(max(offsets)-min(offsets))*1000,'changes':changes,'interpretation':'A growing discrepancy warrants overlap/gap investigation. A clean clock does not prove lip sync.'},indent=2))
