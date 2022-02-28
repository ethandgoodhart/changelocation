import subprocess
import sys
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    import requests
except ModuleNotFoundError:
    os.system("pip{}.{} install requests".format(sys.version.split('.')[0], sys.version.split('.')[1]))

idevicesetlocation_installed = subprocess.getoutput("idevicesetlocation --help").split("\n")[0] == 'Usage: idevicesetlocation [OPTIONS] -- <LAT> <LONG>'

if not idevicesetlocation_installed:
    normallyinstalled = subprocess.getoutput("brew install libimobiledevice").split('\n')[0] == 'Error: Cannot install under Rosetta 2 in ARM default prefix (/opt/homebrew)!'
    if not normallyinstalled:
        subprocess.getoutput("arch -arm64 brew install libimobiledevice")

print("\n" + bcolors.OKGREEN + "ChangeLocation" + bcolors.ENDC)
print("by " +bcolors.BOLD + "Ethan Goodhart" + bcolors.ENDC + "\n")

networkFlag = ""
udid = subprocess.getoutput("idevice_id --list")

if udid == "":
    netudid = subprocess.getoutput("idevice_id -n --list")
    
    if netudid != "":
        udid = netudid.split(" ")[0]
        networkFlag = "-n "
    else:
        sys.exit("No device connected!")

dinfo = subprocess.getoutput("ideviceinfo {}{}".format(networkFlag, udid)).split("\n")
print("\n".join([k for k in dinfo if k.split(":")[0] in ["DeviceName", "ProductType", "ProductVersion"]]))
print("ConnectionType: {}\n".format('🌐 NETWORK' if networkFlag != "" else '〽️ WIRED'))
		
print("----------------------")
while True:
    a = input('Enter address to teleport to: ')

    if a.lower() in ['reset', 'real']:
        os.system("idevicesetlocation {}-u {} reset".format(networkFlag, udid))
        print("🔄 successfully reset location 🔄\n----------------------")
    else:
        lat, lon = requests.get("https://www.google.com/maps/search/" + a.replace(" ", "+"), headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}).text.split('<meta content="https://maps.google.com/maps/api/staticmap?center=')[1].split('&amp;')[0].split('%2C')
        os.system("idevicesetlocation {}-u {} -- {} {}".format(networkFlag, udid, lat, lon))
        print("✅ successfully changed location ✅\n----------------------")