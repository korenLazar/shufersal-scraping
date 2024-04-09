from glob import glob
import shutil
from timeit import timeit
import yagmail
import datetime
import sqlite3
import subprocess
import requests
import re
import os

RAW_FILES = []
RESULTS = []
def create_mail_account(dict_account: dict):
    return yagmail.SMTP(dict_account["username"], dict_account["pwd"])

def calculate_size(sizes: list[int]):
    little = sizes[0]
    larger = sizes[1]
    counter = 1
    while larger > 1024**counter:
        counter+=1
    sizess = ["byes","KB","MB","GB","TB"]
    return [f"{larger/1024**3}{sizess[2]}",f"{(larger-little)/1024**counter}{sizess[counter-1]}",f"{little/1024**3}{sizess[2]}"]
def create_mail_to_send(
        old_count: int, new_count: int, time_finished: str, updated: int, dict_account: dict, updated_chains: dict, sizes: list[int]):
    mail = create_mail_account(dict_account)
    calc = calculate_size(sizes)
    content = f"""
    Today report:
    the old number of documents in the database was {old_count}. Now you've got {new_count-old_count} new items. At total, {new_count}, and {updated} have benn updated.
    the update has been finished at {time_finished}. The old size was {calc[-1]}, the new size is {calc[0]}. Today have been added {calc[1]}.
    """
    for chain in updated_chains:
        content += f"{chain}: {updated_chains[chain]}"
    mail.send(os.environ['SEND_TO_MAIL'].split(':'),
              f"Mongo Daily Report {datetime.date.today()}", content)

#TODO: create script location and built in scripts
def sqlme(raw: str, res: str):
    subprocess.Popen("/Scripts/sqlite")
    
#TODO: create script location and built in scripts
def zip_res_and_all(dict_account: dict):
    global RAW_FILES, RESULTS
    mail = create_mail_account(dict_account)
    timeing = [f"{os.environ['STATE_DIR']}/{datetime.datetime.now().strftime('%Y-%m-%d--%H,%M')}-all.7z",
               f"{os.environ['STATE_DIR']}/raw.{datetime.datetime.now().strftime('%Y-%m-%d--%H,%M')}.7z",
               f"{os.environ['STATE_DIR']}/{datetime.datetime.now().strftime('%Y-%m-%d--%H,%M')}.7z"]
    send_me_raw_files_rar(dict_account, timeing[1])
    send_me_results_rar(dict_account, timeing[2])
    d = glob(f"{os.environ['STATE_DIR']}/*.7z")
    sqlme(d[0],d[1])
    subprocess.Popen(
        ['sh', '-c',
         f"7zr a {timeing[0]} -mx=9 -m0=lzma {os.environ['STATE_DIR']}/*.7z"]).wait()
    mail.send(os.environ['SEND_TO_MAIL'].split(':'),
              f'raw files in rar, {datetime.date.today()}', attachments=timeing[0], contents=f"those where the raw files and the results of {datetime.date.today()}. The size of the raw files is {os.path.getsize(timeing[1])} and the size of the results is {os.path.getsize(timeing[2])}. The size of the all is {os.path.getsize(timeing[0])}. the files in the rar are {','.join(RAW_FILES)} and {','.join(RESULTS)}. at total in the rar there are {len(RAW_FILES)} raw files, {len(RESULTS)} files. so, there are {len(RESULTS)+len(RAW_FILES)} files.")
    try:
        #with open(timeing[0], "rb") as fileme:
        #    requests.post("https://auto.saret.dev/webhook/68396088-b4cf-4ed4-b67d-b0def3c0dcf6", data=fileme.read(), headers={"filename":timeing[0].split(r'/')[-1]})
        subprocess.Popen(
         ['sh', '-c', f"scp -i {os.environ['PRIVKEY']} {timeing[0]} saret@libre.saret.dev:/bck/all/"]).wait()
    except Exception:
        pass
    move_res_and_raw()


def send_me_results_rar(dict_account: dict, timeing: str):
    global RESULTS
    RESULTS = os.listdir(f"{os.environ['LOCATION']}/results/")
    subprocess.Popen(
        ['sh', '-c',
         f"7zr a {timeing} -mx=9 -m0=lzma {os.environ['LOCATION']}/results/"]).wait()

def send_me_raw_files_rar(dict_account: dict, timeing: str):
    global RAW_FILES
    RAW_FILES = os.listdir(f"{os.environ['LOCATION']}/raw_files/")
    subprocess.Popen(
        ['sh', '-c',
         f"7zr a {timeing} -mx=9 -m0=lzma {os.environ['LOCATION']}/raw_files/"]).wait()


#TODO: create script location and built in scripts
def send_me_logs(dict_account: dict):
    mail = create_mail_account(dict_account)
    subprocess.Popen("/Scripts/MakeReport", shell=True).wait()
    mail.send(os.environ['SEND_TO_MAIL'].split(':'), f"data send {datetime.date.today()}", attachments=f"{os.environ['STATE_DIR']}/report{datetime.date.today()}.txt")
    os.remove(f"{os.environ['STATE_DIR']}/report{datetime.date.today()}.txt")

#TODO: create script location and built in scripts
def move_res_and_raw():
    for file in glob("results/*")+glob('raw_files/*'):
        if not os.path.exists(f"{os.environ['SAVE_LOCATION']}"):
            os.mkdir(f"{os.environ['SAVE_LOCATION']}")
            os.mkdir(f"{os.environ['SAVE_LOCATION']}/raw_files")
            os.mkdir(f"{os.environ['SAVE_LOCATION']}/results")
        shutil.move(file, f"{os.environ['SAVE_LOCATION']}/{file}")
