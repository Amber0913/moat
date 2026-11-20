"""Generate the original A/B and edited showcase GIFs without changing inputs."""
import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
WORKSPACE = SITE.parent
SETTINGS = {'fps': 10, 'original_width': 192, 'edited_width': 384,
            'palette': 192, 'dither': 'bayer', 'bayer_scale': 3, 'version': 2}


def convert(job, ffmpeg):
    case, name, relative_source, width = job
    source = WORKSPACE/relative_source
    target = SITE/'assets'/case/name
    stamp = target.with_suffix('.gif.json')
    if not source.is_file():
        raise FileNotFoundError(source)
    fingerprint = {'source': relative_source,
                   'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                   'width': width, **SETTINGS}
    if target.is_file() and stamp.is_file() and json.loads(stamp.read_text()) == fingerprint:
        return target, False
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name('.'+target.stem+'.tmp.gif')
    graph = (f'[0:v]fps={SETTINGS["fps"]},scale={width}:-2:flags=lanczos,'
             'split[frames][colors];'
             f'[colors]palettegen=max_colors={SETTINGS["palette"]}:stats_mode=full:reserve_transparent=0[palette];'
             f'[frames][palette]paletteuse=dither=bayer:bayer_scale={SETTINGS["bayer_scale"]}:diff_mode=rectangle')
    command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
               '-threads', '1', '-filter_complex_threads', '1', '-i', str(source),
               '-filter_complex', graph, '-an', '-loop', '0', '-threads', '1',
               str(temporary)]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'{case}/{name}: {result.stderr[-2000:]}')
        with temporary.open('rb') as stream:
            if stream.read(6) not in [b'GIF87a', b'GIF89a']:
                raise RuntimeError(f'Not a GIF: {temporary}')
        os.replace(temporary, target)
        stamp.write_text(json.dumps(fingerprint, indent=2)+'\n')
    finally:
        temporary.unlink(missing_ok=True)
    return target, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        fallback = Path('/home/sidan/miniforge3/envs/wan22/bin/ffmpeg')
        if fallback.is_file():
            ffmpeg = str(fallback)
    if not ffmpeg:
        raise RuntimeError('ffmpeg with palettegen and paletteuse is required.')
    cases = json.loads((SITE/'scripts/showcases.json').read_text())
    if args.limit:
        cases = cases[:args.limit]
    jobs = []
    for case in cases:
        jobs.extend([(case['asset_slug'], 'original-a.gif', case['source_a'], SETTINGS['original_width']),
                     (case['asset_slug'], 'original-b.gif', case['source_b'], SETTINGS['original_width']),
                     (case['asset_slug'], 'edited.gif', case['edited_source'], SETTINGS['edited_width'])])
    started = time.monotonic()
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(convert, job, ffmpeg) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            target, changed = future.result()
            completed += 1
            if completed == 1 or completed % 15 == 0 or completed == len(jobs):
                print(f'{completed}/{len(jobs)} GIFs ready · {time.monotonic()-started:.1f}s', flush=True)
    total = sum((SITE/'assets'/case/name).stat().st_size for case, name, _, _ in jobs)
    print(f'GIF total: {total/1024**2:.1f} MiB', flush=True)


if __name__ == '__main__':
    main()
