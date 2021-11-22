"""A program that takes a Friday Night Funkin' chart converts it into swing tempo.

"""

import json
import math
import sys


def convert(file: str) -> None:
    """Run this. Input the file name, provided it is in the same directory of this .py file.
    It will output a JSON under the name TBA in the same directory of this .py file.

    - Note that file must be the chart you want to process.
    - swing is default to True; set this to false if you want to convert a chart that is ALREADY
    in swing tempo back to regular tempo.
    """

    swing_check = 'swing'
    swing = True
    if swing_check in file:
        swing = False
        print('The file contains the word \'swing\' in it, meaning we are converting from swing.')
    mode = swing
    old_data = read_chart_data(file)
    sn = song_name(old_data)

    if mode:
        new_data = convert_to_swing(old_data)
    else:
        new_data = convert_from_swing(old_data)
    save_chart(new_data, sn, mode)


def read_chart_data(file: str) -> dict:
    """Return the dictionary mapping of the chart data.
    """
    with open(file) as json_file:
        data = json.load(json_file)

    return data


def song_name(cur_chart: dict) -> str:
    """Return the name of the song in all lowercase. It may not be representative of the file name.
    The song name is the name defined by the chart and is not the file name.

    """
    return cur_chart["song"]["song"].lower()


def convert_to_swing(cur_chart: dict) -> dict:
    """Return the dictionary mapping of the chart data converted to swing.

    >>> old_data = read_chart_data('data\\chart.json')
    >>> convert_to_swing(old_data)
    """
    full_data = dict.copy(cur_chart)
    # EVERYTHING BELOW IS IN full_data - WE ARE NOT MUTATING cur_chart
    data = full_data["song"]  # get our song
    bpm = data["bpm"]  # get our bpm
    sections = data["notes"]  # access everything in the list of "notes"
    for section in sections:  # { "lengthInSteps": 16, "mustHitSection": true, "sectionNotes": [] }
        section_notes = section["sectionNotes"]  # a list of note data
        for note in section_notes:  # time, arrow, sus length
            cur_note_time = note[0]  # ms of note time
            beat_count = ms_to_beat(cur_note_time, bpm)  # cur_note_time converted to beat time
            swing_beat_count = to_swing(beat_count)  # make it swing

            swing_ms = beat_to_ms(swing_beat_count, bpm)
            note[0] = swing_ms  # adjust note timing

            if note[2] > 0.01:  # only pushback if it is a sus note
                time_push_diff = swing_beat_count - beat_count  # note was pushed forward by
                time_push_ms = beat_to_ms(time_push_diff, bpm)
                n2 = note[2] - time_push_ms  # note made longer should always make sus shorter
                n3 = max(0.0, n2)  # It will never push back below zero
                note[2] = n3
    return full_data


def convert_from_swing(cur_chart: dict) -> dict:
    """Return the dictionary mapping of the chart data converted to swing.

    >>> old_data = read_chart_data('data\\chart.json')
    >>> convert_to_swing(old_data)
    """
    # I copy pasted the previous code - was too paranoid about errors.
    full_data = dict.copy(cur_chart)
    # EVERYTHING BELOW IS IN full_data - WE ARE NOT MUTATING cur_chart
    data = full_data["song"]  # get our song
    bpm = data["bpm"]  # get our bpm
    sections = data["notes"]  # access everything in the list of "notes"
    for section in sections:  # { "lengthInSteps": 16, "mustHitSection": true, "sectionNotes": [] }
        section_notes = section["sectionNotes"]  # a list of note data
        for note in section_notes:  # time, arrow, sus length
            cur_note_time = note[0]  # ms of note time
            beat_count = ms_to_beat(cur_note_time, bpm)  # cur_note_time converted to beat time
            swing_beat_count = from_swing(beat_count)  # DON'T make it swing

            swing_ms = beat_to_ms(swing_beat_count, bpm)
            note[0] = swing_ms  # adjust note timing

            # if note[2] > 0.01:  # only pushback if it is a sus note
            #    time_push_diff = swing_beat_count - beat_count  # note was pushed forward by
            #    time_push_ms = beat_to_ms(time_push_diff, bpm)
            #    n2 = note[2] - time_push_ms  # note made longer should always make sus shorter
            #    n3 = max(0.0, n2)  # It will never push back below zero
            #    note[2] = n3
    return full_data


def save_chart(data: dict, name: str, mode: bool) -> None:
    """Saves the data into a *.JSON file.

    """
    json_str = json.dumps(data)
    if mode:
        suffix = '-swing.json'
    else:
        suffix = '-non-swing.json'
    file_name = name + suffix
    json_file = open(file_name, 'w')
    json_file.write(json_str)

    json_file.close()
    print('Saved under the name \'' + file_name + '\' in the same directory as this .py file.')


def ms_to_beat(ms: float, bpm: float) -> float:
    """Return the beat time unit of a note originally provided in milliseconds.

    """
    seconds = ms / 1000
    seconds_per_beat = 60 / bpm
    beat_number = seconds / seconds_per_beat
    return beat_number


def beat_to_ms(beat_number: float, bpm: float) -> float:
    """Return the ms timing of a note originally provided in the beat time unit.

    """
    seconds_per_beat = 60 / bpm
    seconds = beat_number * seconds_per_beat  # b * s/b = s
    ms = seconds * 1000
    return ms


def to_swing(beat_count: float) -> float:
    """Return the swing variant of a beat's count.

    """
    beat_decimal = beat_count % 1
    beat_whole_num = math.floor(beat_count)
    # new_beat_decimal = 0.0
    if beat_decimal <= 0.505:  # prevents rounding error
        new_beat_decimal = beat_decimal * (4 / 3)
    else:
        new_beat_decimal = (1 / 3) * ((2 * beat_decimal) + 1)
        # (beat_decimal - 0.5) * (2/3) + (2/3)
    new_beat = beat_whole_num + new_beat_decimal
    return new_beat


def from_swing(beat_count: float) -> float:
    """Return the non-swing variant of the beat count.

    """
    beat_decimal = beat_count % 1
    beat_whole_num = math.floor(beat_count)
    if beat_decimal <= 0.667:
        new_beat_decimal = beat_decimal * (3 / 4)
    else:
        new_beat_decimal = (3 * beat_decimal - 1) / 2
    new_beat = beat_whole_num + new_beat_decimal
    return new_beat


cmdline = ' '.join(sys.argv[1:])
convert(cmdline)
