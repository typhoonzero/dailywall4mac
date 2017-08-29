from appscript import app, mactypes
import os
import time
import subprocess
import urllib, urllib2
import re

def download_bing_today_wallpaper():
    wallpaper_dir = "%s/Pictures/bing-wallpapers"%os.getenv("HOME")
    # g_img={url: "/az/hprichbg/rb/OregonPainted_ZH-CN8553728911_1920x1080.jpg"
    fd = urllib2.urlopen("http://cn.bing.com")
    content = fd.read()
    fd.close()
    matches = re.search(r"g_img\=\{url\:\ \"\/az\/hprichbg.*\.jpg\"\,", content)
    image_string = matches.group(0)[13:-2]
    full_image_url = "http://cn.bing.com" + image_string
    file_name = wallpaper_dir + "/" + image_string.split("/")[-1]
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
    for f in os.listdir(wallpaper_dir):
        if f.endswith(".jpg"):
            full_file_path = '/'.join([wallpaper_dir, f])
            file_ctime = os.path.getctime(full_file_path)
            if (time.time() - file_ctime) < 3600 * 24:
                to_set_picture = full_file_path
    if to_set_picture:
        set_desktop_background(to_set_picture)

if __name__ == "__main__":
    main()
