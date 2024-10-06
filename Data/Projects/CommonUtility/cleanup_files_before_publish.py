from pathlib import Path

DATA_FOLDER = Path("C:\Program Files (x86)\Steam\steamapps\common\Baldurs Gate 3\Data")

compiled_files_list = [
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/RawFiles/story_definitions.div",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/RawFiles/story_header.div",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/goals.raw",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/log.txt",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story.div",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story.div.osi",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story_ac.dat",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story_ac.dat",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story_orphanqueries_found.txt",
    DATA_FOLDER / "Mods/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/Story/story_orphanqueries_ignore.txt",

    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/RawFiles/story_definitions.div",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/RawFiles/story_header.div",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/goals.raw",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/log.txt",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story.div",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story.div.osi",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story_ac.dat",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story_ac.dat",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story_orphanqueries_found.txt",
    DATA_FOLDER / "Mods/PPMeter_d2481ff8-5c74-cd1c-8709-6d8314bd1c30/Story/story_orphanqueries_ignore.txt"
]


if __name__ == '__main__':
    for compiled_file in compiled_files_list:
        if compiled_file.exists():
            print(f'Removing {compiled_file}')
            compiled_file.unlink()