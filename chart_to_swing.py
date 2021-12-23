"""A program that takes a Friday Night Funkin' chart converts it into swing tempo.

"""

import easygui
import json
import math
# import sys


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

    new_data = convert_to_swing(old_data, swing)

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


def convert_to_swing(cur_chart: dict, convert_swing: bool) -> dict:
    """Return the dictionary mapping of the chart data converted to swing.

    >>> old_data = read_chart_data('data\\chart.json')
    >>> convert_to_swing(old_data)
    """

    full_data = dict.copy(cur_chart)
    # EVERYTHING BELOW IS IN full_data - WE ARE NOT MUTATING cur_chart
    data = full_data["song"]  # get our song
    bpm = data["bpm"]  # get our bpm

    bpm_log = [(bpm, 0.0, 0)]  # previous BPMs: BPM, PREV BPM region time lasted, and
    # section no. WHEN THAT HAPPENED
    # when_last_bpm_change = 0.0
    bpm_changed = False

    sections = data["notes"]  # access everything in the list of "notes"

    section_num = 0
    for section in sections:  # { "lengthInSteps": 16, "mustHitSection": true, "sectionNotes": [] }
        # change BPM detection
        if "changeBPM" in section:
            if section["changeBPM"]:
                if "bpm" in section and bpm_log[-1][0] != section["bpm"]:
                    print('BPM change detected.')
                    new_bpm = section["bpm"]
                    if len(bpm_log) <= 1:
                        time_bpm_change_lasted = section_num * (60 / bpm) * 4 * 1000  # sn * bl * 4
                    else:
                        time_bpm_change_lasted = (section_num - bpm_log[-1][2]) * \
                                                 (60 / bpm_log[-1][0]) * 4 * 1000
                        # (section num - prev section num) * (beat length of former BPM) * 4
                    bpm_log.append((new_bpm, time_bpm_change_lasted, section_num))
                    # when_last_bpm_change = bpm_log_to_time_offset(bpm_log)
                    bpm_changed = True
                    print(bpm_log)

        section_notes = section["sectionNotes"]  # a list of note data
        for note in section_notes:  # time, arrow, sus length
            cur_note_time = note[0]  # ms of note time
            if not bpm_changed:
                beat_count = ms_to_beat(cur_note_time, bpm)  # cur_note_time converted to beat time
            else:
                beat_count = ms_to_beat_change(cur_note_time, bpm_log)
            if convert_swing:
                swing_beat_count = to_swing(beat_count)  # make it swing
            else:
                swing_beat_count = from_swing(beat_count)  # make it NOT swing

            if not bpm_changed:
                swing_ms = beat_to_ms(swing_beat_count, bpm)
            else:
                swing_ms = beat_to_ms_change(swing_beat_count, bpm_log)
            # print(str(beat_count) + ', ' + str(swing_beat_count))
            note[0] = swing_ms  # adjust note timing

            if note[2] > 0.01 and convert_swing:  # only pushback if it is a sus note
                time_push_diff = swing_beat_count - beat_count  # note was pushed forward by
                time_push_ms = beat_to_ms(time_push_diff, bpm)
                n2 = note[2] - time_push_ms  # note made longer should always make sus shorter
                n3 = max(0.0, n2)  # It will never push back below zero
                note[2] = n3
        section_num += 1
    return full_data


# bpm_log = [(bpm, 0.0, 0)]

def ms_to_beat_change(ms: float, bpm_log: list[tuple[float, float, int]]) -> float:
    """Return the beat time unit of a note originally provided in milliseconds.

    """
    cmsbc = bpm_log_to_time_offset(bpm_log)  # total ms before change
    time_since_last_bpm_change = ms - cmsbc

    cbbc_so_far = bpm_log[-1][2] * 4  # total beats before the last BPM change
    # which happens to be the section where the previous bpm change occur times 4

    seconds_new = time_since_last_bpm_change / 1000
    seconds_per_beat = 60 / bpm_log[-1][0]
    beat_number_new = seconds_new / seconds_per_beat  # beat no since bpm change
    return cbbc_so_far + beat_number_new


def beat_to_ms_change(beat_number: float, bpm_log: list[tuple[float, float, int]]) -> float:
    """Return the ms timing of a note originally provided in the beat time unit.

    """
    cmsbc = bpm_log_to_time_offset(bpm_log)  # total ms before change

    cbbc_so_far = bpm_log[-1][2] * 4  # total beats before the last BPM change
    # which happens to be the section where the previous bpm change occur times 4
    local_beat_number = beat_number - cbbc_so_far

    seconds_per_beat = 60 / bpm_log[-1][0]
    seconds_new = local_beat_number * seconds_per_beat  # local seconds count
    ms = seconds_new * 1000
    return ms + cmsbc


def bpm_log_to_time_offset(the_log: list[tuple[float, float, int]]) -> float:
    """Return the time where the last BPM change occur, in ms.

    """
    combined_times = [x[1] for x in the_log]
    return sum(combined_times)


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


if __name__ == '__main__':
    path = easygui.fileopenbox(msg='Select the *.json file you want to open.',
                               filetypes=["*.json"])
    # cmdline = ' '.join(sys.argv[1:])
    convert(path)
