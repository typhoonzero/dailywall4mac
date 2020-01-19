from appscript import app, mactypes
import os
import time
import subprocess
import urllib, urllib2
import re
import operator
import json

def download_bing_today_wallpaper():
    fd = urllib2.urlopen("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&uhdwidth=3840&uhdheight=2160&uhd=1")
    daily_json = json.loads(fd.read())
    fd.close()
    image_url = daily_json["images"][0]["url"]
    full_image_url = "".join(["https://cn.bing.com", image_url])

    wallpaper_dir = "%s/Pictures/bing-wallpapers"%os.getenv("HOME")
    file_name = os.path.join(wallpaper_dir, daily_json["images"][0]["hsh"] + ".jpg")
    if os.path.isfile(file_name):
        return
    urllib.urlretrieve(full_image_url, file_name)

# for single monitor
SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

SCRIPT_MULTI = """/usr/bin/osascript<<END
tell application "System Events"
    set desktopCount to count of desktops
    repeat with desktopNumber from 1 to desktopCount
        tell desktop desktopNumber
            set picture to "%s"
        end tell
    end repeat
end tell
END
"""

def set_desktop_background(filename):
    subprocess.call(SCRIPT_MULTI % filename, shell=True)

def main():
    download_bing_today_wallpaper()
    
    wallpaper_dir = "%s/Pictures/bing-wallpapers"%os.getenv("HOME")
    to_set_picture = ""
    file_list = []
    for f in os.listdir(wallpaper_dir):
        if f.endswith(".jpg"):
            full_file_path = '/'.join([wallpaper_dir, f])
            file_ctime = os.path.getctime(full_file_path)
            file_list.append((full_file_path, file_ctime))
    file_list.sort(key=operator.itemgetter(1))
    if file_list:
        to_set_picture=file_list[-1][0]
    if to_set_picture:
        set_desktop_background(to_set_picture)

if __name__ == "__main__":
    main()
