#!/usr/bin/env python

import os
from subprocess import check_output
import json
import sys

# summarization length in second
sum_length = 30

if len(sys.argv) < 2:
    print "Usage: \"python {} <input video file>\"".format(sys.argv[0])
    print "Exitting..."
    sys.exit(-1)

vid_file = sys.argv[1]
video_dir = os.path.dirname(vid_file)
hecate_bin = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "distribute/bin/hecate"
    )
if not os.path.isfile(hecate_bin):
    print "Vid-sum binary file, {} doesn not exist.".format(hecate_bin)
    print "Check if hecage has been built properly -- `make all && make distribute`. Exitting..."
    sys.exit(-2)

run_cmd = [
        hecate_bin,
        "--in_video",
        vid_file,
        "--out_dir",
        video_dir,
        "--lmov",
        str(sum_length),
        "--generate_mov",
        "--print_shot_info",
        "--print_keyfrm_info",
        "--print_sum_info",
        ]

# convert output text into json that contains only "timelines" info
sum_out_raw = check_output(run_cmd)
print "[Debug] sum_out_raw={}".format(sum_out_raw)
sum_out = dict()
for sum_out_line in sum_out_raw.splitlines():
    if sum_out_line.startswith('summaries:'):
        #print "summaries={}".format(sum_out_line)
        sum_out['timelines'] = list()
        summaries = sum_out_line.split(' ')[1]
        summaries = summaries.split(',')
        for summary in summaries:
            summary = summary[1:-1].split(':')
            summary_start = summary[0]
            summary_end = summary[1]
            sum_out['timelines'].append([float(summary_start), float(summary_end)])

summary_file = os.path.join(
        video_dir,
        os.path.basename(vid_file)[:-4] + "_sum.json"
        )
with open(summary_file, "w") as f:
    json.dump(sum_out, f)
