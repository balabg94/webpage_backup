#!/usr/bin/env python3

from datetime import datetime
import argparse
import fnmatch
import json
import lz4.block
import os
import sys

home = os.path.expanduser("~")
firefox_path = os.path.join(home,".mozilla/firefox")

def recovery_path(firefox_path):
    for file in os.listdir(firefox_path):
        if fnmatch.fnmatch(file, '*.default*'):
            new_path = os.path.join(firefox_path, file, 'sessionstore-backups/recovery.jsonlz4')
            break
    return new_path

now_obj= datetime.now()
now= now_obj.strftime("%b %d %Y %k:%M:%S")
    
def backup_urls():
    magic = firefox_recovery_file.read(8)
    jdata = json.loads(lz4.block.decompress(firefox_recovery_file.read()).decode("utf-8"))
    urls = []
    for win in jdata.get("windows"):
        for tab in win.get("tabs"):
            i = int(tab.get("index")) - 1
            urls.append(tab.get("entries")[i].get("url"))
    url_new = write_file(urls)
    return 'Done. Recorded {} urls'.format(url_new)

def write_file(urls):
    backup= open('webpage_bk.bk', 'a+')
    backup.seek(0)
    content= backup.read()
    #backup.write('[{}]\n'.format(now))
    for i in urls:
        if i not in content:
            backup.write(i+'\n')
        else:
            urls.remove(i)
            pass
    return len(urls)

def parse_args():
    parser = argparse.ArgumentParser(description='Application for backing up and reopening weburls')
    parser.add_argument('-n', '--new', default= None, action= 'store_true',  help= 'Backup of current open tabs')
    parser.add_argument('-r', '--restore', default= None, action= 'store_true', help= 'Open the urls in the browser.')

    args = parser.parse_args()
    if not args.new and not args.restore:
        parser.error("Please provide an operation")

    return args

def main():
    global firefox_recovery_file
    os.environ['opentabs'] = recovery_path(firefox_path)
    firefox_recovery_file= open(os.environ["opentabs"], "rb")
    args= parse_args()
    if args.new:
        backup = backup_urls()
        print(backup)
    if args.restore:
        print('Restoring')

if __name__ == '__main__':
    sys.exit(main())
