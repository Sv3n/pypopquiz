"""Main entry point for the pypopquiz package"""

import argparse
from pathlib import Path

import pypopquiz as ppq
import pypopquiz.io
import pypopquiz.video


def parse_arguments():
    """Sets the command-line arguments"""
    parser = argparse.ArgumentParser(description="pypopquiz interface")
    parser.add_argument("-i", "--input_file", required=True, help="Input JSON file with popquiz info", type=Path)
    parser.add_argument("-o", "--output_dir", required=True, help="Output dir with popquiz data", type=Path)
    parser.add_argument("-b", "--backend", required=False, help="Backend selection", type=str, default='ffmpeg')
    return vars(parser.parse_args())


def popquiz(input_file: Path, output_dir: Path, backend: str) -> None:
    """The main routine, constructing the entire popquiz output"""

    input_data = ppq.io.read_input(input_file)
    ppq.io.log("Processing popquiz round {:d}".format(input_data["round"]))

    add_spacer = input_data.get('spacers', False)

    for question in input_data["questions"]:
        for source in question["sources"]:
            ppq.io.get_video(source, output_dir, input_file.parent)

    q_videos, a_videos = [], []
    for index, question in enumerate(input_data["questions"]):
        question_id = index + 1
        round_id = input_data["round"]
        ppq.io.log("Processing question {:d}: {:s} - {:s}".format(question_id, question["artist"], question["title"]))
        q_video = ppq.video.create_video("question", round_id, question, question_id, output_dir,
                                         backend=backend, add_spacer=add_spacer)
        a_video = ppq.video.create_video("answer", round_id, question, question_id, output_dir,
                                         backend=backend, add_spacer=add_spacer)
        q_videos.append(q_video)
        a_videos.append(a_video)


if __name__ == "__main__":
    popquiz(**parse_arguments())
