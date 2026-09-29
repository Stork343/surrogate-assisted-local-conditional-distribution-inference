"""Publish V5 editorial PDFs from verified source bytes, without running statistics."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '04_LaTeX_Source'


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True).stdout


def git_hash(path):
    data = path.read_bytes()
    return hashlib.sha1(('blob %d\0' % len(data)).encode() + data).hexdigest()


def pages(path):
    match = re.search(r'^Pages:\s+(\d+)', run(['pdfinfo', str(path)]), re.M)
    if not match:
        raise RuntimeError('Missing page count for ' + str(path))
    return int(match.group(1))


def main():
    manifest = []
    for line in (ROOT / 'SOURCE_GIT_HASHES.txt').read_text().splitlines():
        expected, relative = line.split(None, 1)
        relative = relative.strip()
        path = SOURCE / relative
        if not path.is_file() or git_hash(path) != expected:
            raise RuntimeError('Source-byte mismatch: ' + relative)
        manifest.append(relative)
    outputs = [
        ('paper/manuscript.pdf', '01_Manuscript/manuscript.pdf', 29),
        ('paper/supplement.pdf', '02_Supplementary_Material/supplement.pdf', 53),
        ('submission/cover_letter.pdf', '03_Cover_Letter/cover_letter.pdf', 1),
    ]
    report = {'source_files_verified': len(manifest), 'statistical_analyses_rerun': False,
              'frozen_v3_archive_uploaded': False, 'commit': os.environ.get('GITHUB_SHA'),
              'documents': {}}
    with tempfile.TemporaryDirectory(prefix='jrssb-v5-') as temporary:
        build = Path(temporary) / 'source'
        shutil.copytree(SOURCE, build)
        process = subprocess.run(['bash', 'build_all.sh'], cwd=build, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(process.stdout)
        process.check_returncode()
        for relative, destination, expected_pages in outputs:
            pdf = build / relative
            count = pages(pdf)
            if count != expected_pages:
                raise RuntimeError('%s: expected %d pages, got %d' % (relative, expected_pages, count))
            log = pdf.with_suffix('.log').read_text(errors='replace')
            if re.search(r'Overfull \\[hv]box|There were undefined references|Citation .* undefined|Reference .* undefined', log):
                raise RuntimeError('Unresolved reference or overflow in ' + relative)
            if relative.endswith('supplement.pdf') and pdf.stat().st_size >= 2_000_000:
                raise RuntimeError('Supplement exceeds PDF size limit')
            target = ROOT / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf, target)
            report['documents'][destination] = {'pages': count, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    figure_map = {
        'Figure_1.pdf': 'figure1_separation.pdf',
        'Figure_2.pdf': 'v2/figure2_simulation_comparison.pdf',
        'Figure_3.pdf': 'v3/validation.pdf',
        'Figure_4.pdf': 'v2/figure3_binary_certification.pdf',
        'Figure_5.pdf': 'figure2_epa_discrepancy.pdf',
        'Figure_6.pdf': 'v3/epa_budget_full.pdf',
        'Figure_S1.pdf': 'v2/figure5_epa_intervals.pdf',
    }
    separate = ROOT / '05_Separate_Figures'
    separate.mkdir(exist_ok=True)
    for name, source in figure_map.items():
        shutil.copy2(SOURCE / 'figures' / source, separate / name)
    downloads = ROOT / 'downloads'
    downloads.mkdir(exist_ok=True)
    run(['pdfunite', str(ROOT / outputs[0][1]), str(ROOT / outputs[1][1]),
         str(downloads / 'manuscript_and_supplement.pdf')])
    with zipfile.ZipFile(downloads / 'LaTeX_Source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for relative in manifest:
            archive.write(SOURCE / relative, '04_LaTeX_Source/' + relative)
    (ROOT / 'build_report.json').write_text(json.dumps(report, indent=2) + '\n')
    shipping = [ROOT / 'README.md', ROOT / 'SOURCE_GIT_HASHES.txt', ROOT / 'build_report.json']
    shipping.extend(ROOT / item[1] for item in outputs)
    shipping.extend(sorted(separate.glob('*.pdf')))
    shipping.extend(SOURCE / item for item in manifest)
    shipping.extend([downloads / 'LaTeX_Source.zip', downloads / 'manuscript_and_supplement.pdf'])
    checks = ''.join(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + str(path.relative_to(ROOT)) + '\n'
                     for path in sorted(shipping))
    (ROOT / 'SHA256SUMS.txt').write_text(checks)
    shipping.append(ROOT / 'SHA256SUMS.txt')
    with zipfile.ZipFile(downloads / 'JRSSB_V5_editorial_submission.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in shipping:
            archive.write(path, 'JRSSB_Submission_v5/' + str(path.relative_to(ROOT)))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
