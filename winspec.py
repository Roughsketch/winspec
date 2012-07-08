import os
import platform
import datetime

from colorama import init, Style, Fore
from wmi import WMI
from win32com.client import GetObject

def WMIQuery(value, mgmtclass):
	w = WMI('.')
	result = w.query('SELECT ' + value + ' FROM Win32_' + mgmtclass)
	return eval('result[0].' + value)

def Memory():
	Free = int(WMIQuery('FreePhysicalMemory', 'OperatingSystem')) / 1024
	Total = int(WMIQuery('TotalVisibleMemorySize', 'OperatingSystem')) / 1024
	Percent = Free / float(Total)

	returnVal = ''
	if Percent <= .1:
		returnVal = Fore.RED
	elif Percent <= .5:
		returnVal = Fore.YELLOW
	else:
		returnVal = Fore.GREEN

	returnVal += str(Total - Free) + Fore.WHITE + 'MB/'
	returnVal += str(Total) + 'MB'
	return returnVal

def Resolution():
	returnVal = str(WMIQuery('ScreenWidth', 'DesktopMonitor')) + 'x'
	returnVal += str(WMIQuery('ScreenHeight', 'DesktopMonitor'))
	return returnVal

def Harddrive():
	Free = int(WMIQuery('FreeSpace', 'LogicalDisk')) / 1024**3
	Size = int(WMIQuery('Size', 'LogicalDisk')) / 1024**3
	Percent = Free / float(Size)

	returnVal = ''
	if Percent <= .1:
		returnVal += Fore.RED
	elif Percent <= .5:
		returnVal += Fore.YELLOW
	else:
		returnVal += Fore.GREEN

	returnVal += str(Size - Free) + Fore.WHITE + 'GB/' + str(Size) + 'GB'
	return returnVal

def Motherboard():
	returnVal = str(WMIQuery('Manufacturer', 'BaseBoard')) + ' '
	returnVal += str(WMIQuery('Product', 'BaseBoard'))
	return returnVal

def Kernel():
  return str(WMIQuery('Version', 'OperatingSystem'))

def Processors():
	return str(WMIQuery('NumberOfCores', 'Processor'))

def CPU():
	returnVal = str(WMIQuery('Name', 'Processor'))
	returnVal = returnVal.replace('(TM)', '')
	returnVal = returnVal.replace('CPU ', '')
	return returnVal

def GPU():
	return str(WMIQuery('Name', 'VideoController'))
	
def UpTime():
	lastBoot = str(WMIQuery('LastBootUpTime', 'OperatingSystem'))
	returnVal = datetime.datetime.now() - datetime.datetime.strptime(lastBoot[0:13],'%Y%m%d%H%M%S')
	return str(returnVal).split('.')[0]

def Processes():
	w = GetObject('winmgmts:')
	procs = w.InstancesOf('Win32_Process')
	return str(len(procs))

def Programs():
	w = GetObject('winmgmts:')
	progs = w.InstancesOf('Win32_Product')
	return str(len(progs))

def SetPosition(width, height):
	return '\033[' + str(height) + ';' + str(width) + 'H'

init(autoreset=True)

winLogo = '\n\n\033[31m          ,,,,,,,,,\n\
        \033[31mII?++?II7$$$:,                 \n\
       \033[31m$I??++?I77$ZZOO                  \n\
       \033[31m7I?++??I77$ZZO8 \033[32m &,           ,: \n\
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
                    \033[33m ```````       '

print Style.BRIGHT + winLogo

print SetPosition(41, 4) + 'Getting computer information...' + SetPosition(79, 24)

Username = Style.BRIGHT + Fore.CYAN + os.environ['USERNAME']
Computername = Style.BRIGHT + Fore.CYAN + os.environ['COMPUTERNAME']

output = SetPosition(41, 4) + Username
output += Fore.WHITE + '@'
output += Computername
output += SetPosition(41, 6) + 'OS: ' + Fore.WHITE + platform.system() + ' ' + platform.release();
output += SetPosition(41, 7) + Fore.CYAN + 'Resolution: ' + Fore.WHITE + Resolution()
output += SetPosition(41, 8) + Fore.CYAN + 'Memory: ' + Fore.WHITE + Memory()
output += SetPosition(41, 9) + Fore.CYAN + 'Disk: ' + Fore.WHITE + Harddrive();
output += SetPosition(41, 10) + Fore.CYAN + 'CPU Cores: ' + Fore.WHITE + Processors();
output += SetPosition(41, 11) + Fore.CYAN + 'CPU: ' + Fore.WHITE + CPU();
output += SetPosition(41, 12) + Fore.CYAN + 'GPU: ' + Fore.WHITE + GPU();
output += SetPosition(41, 13) + Fore.CYAN + 'Kernel: ' + Fore.WHITE + Kernel();
output += SetPosition(41, 14) + Fore.CYAN + 'MoBo: ' + Fore.WHITE + Motherboard();
output += SetPosition(41, 15) + Fore.CYAN + 'Uptime: ' + Fore.WHITE + UpTime();
output += SetPosition(41, 16) + Fore.CYAN + 'Processes: ' + Fore.WHITE + Processes();
output += SetPosition(41, 17) + Fore.CYAN + 'Programs: ' + Fore.WHITE + Programs();
output += SetPosition(79, 24)

print SetPosition(41, 4) + ' ' * 35
print output
raw_input()

os.system('cls')
