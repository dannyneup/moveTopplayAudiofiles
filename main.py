import os
import logging
from eyed3 import id3
from shutil import copy, move


def create_audiofilelist(src_path: str):
    filelist = []
    for path in os.listdir(src_path):
        full_path = os.path.join(src_path, path)
        if os.path.isdir(full_path):
            filelist += create_audiofilelist(full_path)
        elif os.path.isfile(full_path) and os.path.splitext(full_path)[-1] in ['.mp3', '.wav', '.aif', '.aif']:
            filelist.append(full_path)
    return filelist

def move_file(srcfile: str, dst: str):
    if not os.path.isdir(dst):
        os.makedirs(dst)
        log.write(f"created directory {dst}\n")
    files_in_dst = os.listdir(dst)
    if os.path.basename(srcfile) in files_in_dst:
        log.write(f"file {srcfile} already exists in destination folder {dst}.\n")
    else:
        # copy(srcfile, dst)
        # log.writelines(f"file {srcfile} copyed to folder {dst}.\n")
        move(srcfile, dst)
        log.write(f"file {srcfile} moved to folder {dst}.\n")

def check_comment(file: str):
    tag = id3.Tag()
    tag.parse(file)
    if tag.comments:
        comment = tag.comments[0].text
        if "topplay" in comment.lower():
            if tag.recording_date:
                year = tag.recording_date.year
                if 2020 <= year <= 2029:
                    return ["TopPlay", "2020"]
                elif 2010 <= year <= 2019:
                    return ["TopPlay", "2010"]
                elif 2000 <= year <= 2009:
                    return ["TopPlay", "2000"]
                elif 1990 <= year <= 1999:
                    return ["TopPlay", "1990"]
                elif 1980 <= year <= 1989:
                    return ["TopPlay", "1980"]
                elif 1970 <= year <= 1979:
                    return ["TopPlay", "1970"]
                elif 1960 <= year <= 1969:
                    return ["TopPlay", "1960"]
                else:
                    return ["TopPlay", "<1960"]
            else:
                return ["TopPlay", None]
        else:
            return None
    else:
        return None

def create_top_play_filelist(path_music: str, path_sorted: str):
    filelist = create_audiofilelist(path_music)
    if path_sorted:
        filelist += create_audiofilelist(path_sorted)
    for file in filelist:
        if check_comment(file):
            crate, year = check_comment(file)
            if check_comment(file)[1]:
                move_file(file, path_sorted + f"/{crate}/{year}")
            else:
                move_file(file, path_sorted + f"/{crate}")
        else:
            if path_sorted in os.path.splitext(file)[0]:
                move_file(file, path_music)


if __name__ == '__main__':
    log = open("log.txt", "w")
    create_top_play_filelist("Assets", "Crates")
