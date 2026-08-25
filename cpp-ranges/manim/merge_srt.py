"""
Merge individual SRT subtitle files into one combined SRT,
accounting for the duration of title cards (which have no subtitles).

Usage:
    python merge_srt.py [--quality 1080p60|480p15] [-o output.srt]

Requires: ffprobe (from ffmpeg) on PATH.
"""

import subprocess
import re
import os
import argparse
from pathlib import Path

# Same merge order as Makefile (scene class names in order)
MERGE_ORDER = [
    ("ranges-algo0", "RangesIntro"),
    ("title_cards", "TitleSort"),
    ("ranges-algo1", "RangesSort"),
    ("title_cards", "TitleFind"),
    ("ranges-algo1", "RangesFind"),
    ("title_cards", "TitleCount"),
    ("ranges-algo1", "RangesCount"),
    ("title_cards", "TitleTransform"),
    ("ranges-algo1", "RangesTransform"),
    ("title_cards", "TitleCopyIf"),
    ("ranges-algo2", "RangesCopyIf"),
    ("title_cards", "TitleBoolPred"),
    ("ranges-algo2", "RangesBoolPredicates"),
    ("title_cards", "TitleMinMax"),
    ("ranges-algo3", "RangesMinMax"),
    ("title_cards", "TitleReverse"),
    ("ranges-algo3", "RangesReverse"),
    ("title_cards", "TitleUnique"),
    ("ranges-algo4", "RangesUnique"),
    ("title_cards", "TitleRemoveIf"),
    ("ranges-algo4", "RangesRemoveIf"),
    ("title_cards", "TitleFill"),
    ("ranges-algo5", "RangesFill"),
    ("title_cards", "TitleGenerate"),
    ("ranges-algo5", "RangesGenerate"),
    ("title_cards", "TitleReplaceIf"),
    ("ranges-algo6", "RangesReplaceIf"),
    ("title_cards", "TitlePartition"),
    ("ranges-algo6", "RangesPartition"),
    ("title_cards", "TitleIsSorted"),
    ("ranges-algo7", "RangesIsSorted"),
    ("title_cards", "TitleBinarySearch"),
    ("ranges-algo7", "RangesBinarySearch"),
    ("title_cards", "TitleNthElement"),
    ("ranges-algo8", "RangesNthElement"),
    ("title_cards", "TitleWithStrings"),
    ("ranges-algo8", "RangesWithStrings"),
    ("title_cards", "TitleProjections"),
    ("ranges-algo9", "RangesProjections"),
    ("title_cards", "TitleViewsPipeline"),
    ("ranges-algo10", "RangesViewsPipeline"),
]


def get_duration(mp4_path):
    """Get video duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(mp4_path)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def parse_srt_time(time_str):
    """Parse SRT timestamp to seconds."""
    m = re.match(r"(\d+):(\d+):(\d+),(\d+)", time_str)
    h, mi, s, ms = int(m[1]), int(m[2]), int(m[3]), int(m[4])
    return h * 3600 + mi * 60 + s + ms / 1000


def format_srt_time(seconds):
    """Format seconds to SRT timestamp."""
    h = int(seconds // 3600)
    mi = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{mi:02d}:{s:02d},{ms:03d}"


def parse_srt(srt_path):
    """Parse an SRT file into a list of (start, end, text) tuples."""
    entries = []
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if not content:
        return entries

    blocks = re.split(r"\n\n+", content)
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        # lines[0] is the index
        time_match = re.match(r"(.+?)\s*-->\s*(.+)", lines[1])
        if not time_match:
            continue
        start = parse_srt_time(time_match.group(1).strip())
        end = parse_srt_time(time_match.group(2).strip())
        text = "\n".join(lines[2:])
        entries.append((start, end, text))
    return entries


def main():
    parser = argparse.ArgumentParser(description="Merge SRT files for combined video")
    parser.add_argument("--quality", default="1080p60", help="Quality folder (1080p60 or 480p15)")
    parser.add_argument("-o", "--output", default="media/CppRanges_subtitles.srt", help="Output SRT path")
    args = parser.parse_args()

    media_dir = Path("media/videos")
    quality = args.quality

    merged_entries = []
    time_offset = 0.0
    counter = 1

    for folder, scene in MERGE_ORDER:
        mp4_path = media_dir / folder / quality / f"{scene}.mp4"
        srt_path = media_dir / folder / quality / f"{scene}.srt"

        if not mp4_path.exists():
            print(f"WARNING: {mp4_path} not found, skipping")
            continue

        duration = get_duration(mp4_path)

        # If SRT exists, merge its entries with offset
        if srt_path.exists():
            entries = parse_srt(srt_path)
            for start, end, text in entries:
                merged_entries.append((
                    time_offset + start,
                    time_offset + end,
                    text,
                ))

        time_offset += duration
        print(f"  {scene:30s}  dur={duration:6.2f}s  offset={time_offset:7.2f}s  "
              f"({'srt' if srt_path.exists() else 'no srt'})")

    # Write merged SRT
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(merged_entries, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(start)} --> {format_srt_time(end)}\n")
            f.write(f"{text}\n\n")

    print(f"\nMerged {len(merged_entries)} subtitle entries -> {args.output}")
    print(f"Total video duration: {format_srt_time(time_offset)}")


if __name__ == "__main__":
    main()
