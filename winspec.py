import os, platform, datetime

from colorama import init, Style, Fore
from wmi import WMI
from win32com.client import GetObject

def Memory():
    w = WMI('.')
    result = w.query("SELECT FreePhysicalMemory FROM Win32_OperatingSystem")
    Free = int(result[0].FreePhysicalMemory) / 1024
    result = w.query("SELECT TotalVisibleMemorySize FROM Win32_OperatingSystem")
    Total = int(result[0].TotalVisibleMemorySize) / 1024
    Percent = Free / float(Total)
    returnVal = ""
    if Percent <= .1:
		returnVal = Fore.RED
    elif Percent <= .5:
		returnVal = Fore.YELLOW
    else:
		returnVal = Fore.GREEN

    returnVal += str(Free) + Fore.WHITE + "MB/"
    returnVal += str(Total) + "MB"
    return returnVal

def Resolution():
    w = WMI('.')
    result = w.query("SELECT ScreenWidth FROM Win32_DesktopMonitor")
    returnVal = str(result[0].ScreenWidth) + 'x'
    result = w.query("SELECT ScreenHeight FROM Win32_DesktopMonitor")
    returnVal += str(result[0].ScreenHeight)
    return returnVal

def Harddrive():
    w = WMI('.')
    result = w.query("SELECT DeviceID FROM Win32_LogicalDisk")

    result = w.query("SELECT FreeSpace FROM Win32_LogicalDisk")
    Free = int(result[0].FreeSpace) / 1024**3
    result = w.query("SELECT Size FROM Win32_LogicalDisk")
    Size = int(result[0].Size) / 1024**3
    Percent = Free / float(Size)
    returnVal = Fore.CYAN + 'Disk: '
    if Percent <= .1:
		returnVal += Fore.RED
    elif Percent <= .5:
		returnVal += Fore.YELLOW
    else:
		returnVal += Fore.GREEN

    returnVal += str(Free) + Fore.WHITE + "GB/" + str(Size) + "GB"
    return returnVal

def CPU():
    w = WMI('.')
    result = w.query("SELECT Name FROM Win32_Processor")
    returnVal = str(result[0].Name).replace("(TM)", "")
    returnVal = returnVal.replace("CPU ", "")
    return returnVal

def GPU():
    w = WMI('.')
    result = w.query("SELECT Name FROM Win32_VideoController")
    returnVal = str(result[0].Name)
    return returnVal
    
def UpTime():
    w = WMI('.')
    result = w.query("SELECT LastBootUpTime FROM Win32_OperatingSystem")
    lastBoot = str(result[0].LastBootUpTime)
    returnVal = datetime.datetime.now() - datetime.datetime.strptime(lastBoot[0:13],'%Y%m%d%H%M%S')
    return str(returnVal).split('.')[0]

def Processes():
    w = GetObject('winmgmts:')
    procs = w.InstancesOf('Win32_Process')
    return str(len(procs))
    
def SetPosition(width, height):
	return '\033[' + str(height) + ';' + str(width) + 'H'

init(autoreset=True)

winLogo = "\n\n\033[31m          ,,,,,,,,,\n\
        \033[31mII?++?II7$$$:,                 \n\
       \033[31m$I??++?I77$ZZOO                  \n\
       \033[31m7I?++??I77$ZZO8 \033[32m &,           ,, \n\
      \033[31m=I??++?II7$$ZZO \033[32m $8OOZ$:,  ,I77$O \n\
      \033[31m7I?++??I7$$ZZOO \033[32m 8OOZZ$$7III77$ZD \n\
     \033[31m+I??++?II7$$ZOO~\033[32m $8OOZZ$77III7$$Z  \n\
     \033[31m7I?++??I77$ZZOO \033[32m 8OOZZ$$7IIII7$ZD  \n\
     \033[31mII?++?II7$$ZZO8\033[32m Z8OOZZ$77III77$Z   \n\
    \033[31m7IO        O7OO \033[32m 8OOZZ$$77III7$ZD   \n\
      \033[34m,:===++?+    \033[32m O8OOZZ$77III77$Z    \n\
   \033[34m :+=~===+??I7$$ \033[32m ?OOZZ$$77III7$ZD    \n\
   \033[34m?+=~~==++?I77$Z   \033[32m :8$$7IIIO8O`      \n\
  \033[34mI?+=~~==+??I7$Z \033[33m 7Z$,         ,:Z     \n\
  \033[34m?+=~~==++?I77$Z\033[33m 7ZZ$$77I??++??II?     \n\
 \033[34m7?+=~~==++?I7$Z \033[33m 7Z$$77II?+++??I$      \n\
 \033[34m?+=~~==++?II7$Z\033[33m ,ZZ$$77II?++??IIO      \n\
\033[34m+?+=~~==++?I7$Z \033[33m ?Z$$77II??++??I$       \n\
\033[34mI?=:OOZZO$I77$Z \033[33m ZZ$$77II?++??IIO       \n\
\033[34m,``          +I \033[33mI7Z$$77II??++??II       \n\
               \033[33m ZZ$$77II?+++??IO        \n\
                 \033[33m Z777I??++?IZZ         \n\
                    \033[33m ```````       "

print Style.BRIGHT + winLogo

Username = Style.BRIGHT + Fore.CYAN + os.environ['USERNAME']
Computername = Style.BRIGHT + Fore.CYAN + os.environ['COMPUTERNAME']

output = SetPosition(41, 4) + Username
output += Fore.WHITE + '@'
output += Computername
output += SetPosition(41, 6) + 'OS: ' + Fore.WHITE + platform.system() + ' ' + platform.release();
output += SetPosition(41, 7) + Fore.CYAN + "Memory: " + Fore.WHITE + Memory()
output += SetPosition(41, 8) + Fore.CYAN + "Resolution: " + Fore.WHITE + Resolution()
output += SetPosition(41, 9) + Harddrive();
output += SetPosition(41, 10) + Fore.CYAN + "CPU: " + Fore.WHITE + CPU();
output += SetPosition(41, 11) + Fore.CYAN + "GPU: " + Fore.WHITE + GPU();
output += SetPosition(41, 12) + Fore.CYAN + "Uptime: " + Fore.WHITE + UpTime();
output += SetPosition(41, 13) + Fore.CYAN + "Processes: " + Fore.WHITE + Processes();
output += SetPosition(79, 24)

print output
raw_input()

os.system('cls')
