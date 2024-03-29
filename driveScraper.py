# Copyright 2023 Daniel Ragusa

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import psutil
import platform
import errno
import inquirer
import os
from rich.console import Console
import platform
from art import *
import time
from rich.table import Table
import math
import sys
import shutil
from rich.progress import track
from blessed import Terminal
from inquirer.themes import Default
import datetime
import subprocess
import threading

term = Terminal()
console = Console()
searchLogList = []
scrapeBotArt = text2art('driveScraper', font='small')


error_messages = {
    errno.ENOENT: "OSError FILE NOT FOUND",
    errno.EACCES: "OSError PERMISSION DENIED",
    errno.EEXIST: "OSError FILE ALREADY EXISTS",
    errno.ENOTDIR: "OSError NOT A DIRECTORY",
    errno.EINVAL: "OSError INVALID ARGUMENT",
    errno.ENOTEMPTY: "OSError DIRECTORY NOT EMPTY"
}

class CyberTheme(Default):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.purple
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.cyan
        self.Checkbox.selection_icon = ">"
        self.Checkbox.selected_icon = "[X]"
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "[ ]"
        self.List.selection_color = term.cyan
        self.List.selection_cursor = ">"
        self.List.unselected_color = term.normal


class SearchResult:
    def __init__(self, drive, ext, filesFoundNum, filesFoundSize, timeTaken):
        self.drive = drive
        self.ext = ext
        self.filesFoundNum = filesFoundNum
        self.filesFoundSize = filesFoundSize
        self.timeTaken = timeTaken



def get_linux_trash_path():
    # Use xdg-user-dir to retrieve the trash directory path
    try:
        output = subprocess.check_output(['xdg-user-dir', 'TRASH'], universal_newlines=True)
        trash_path = output.strip()
        return trash_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


if platform.system() == 'Windows':
    
    clear = 'cls'

elif platform.system() == 'Linux':
    
    clear = 'clear'


def printScreen():
    os.system(clear)
    console.print(scrapeBotArt, style='cyan', justify='left')


def getEndOption():
    options = [
    inquirer.List('choice',
                    message="Choose an option",
                    choices=["Add To Search","Copy Found Files"],
                    carousel=True,
                ), 
    ]
    return inquirer.prompt(options, theme = CyberTheme())



def getDrive(drives):

    try:
    
        drives = [
            inquirer.List(
                'drive',
                message='Choose a drive',
                choices=drives,
                carousel=True
            )
        ]

        return inquirer.prompt(drives, theme=CyberTheme())


    except inquirer.errors.ValidationError:
        print('Invalid drive')
        # return getDrive(drives)
    
    
def getExtension():

    options = [
    inquirer.List('ext',
                    message="Choose an extension",
                    choices=['.mp3','.mp4','.jpeg','.png','.wav','.txt','.py','.sql','[custom]'],
                    carousel=True,
                ),
    ]

    answer = inquirer.prompt(options, theme=CyberTheme())

    if answer == None:
        return None
    
    if answer['ext'] == '[custom]':
        printScreen()
        
        question = [
        inquirer.Text('ext', message='Enter extension with dot [.ext]'),
        ]

        return inquirer.prompt(question, theme=CyberTheme())

    return answer

def getOptions():

    options = [
    inquirer.List('choice',
                    message='Choose an option',
                    choices=[f'GO', 'Change Search'],
                    carousel=True,
                ),
    ]

    return inquirer.prompt(options, theme=CyberTheme())


def log_error(errLog, error_type, file_path):
    console.print(f'{error_type}: {file_path}', style='bold reverse red')
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    errLog.write(f'{current_time}\t{error_type}: {file_path}\n')
    
      


def printSearchInfo(drive, ext):
    console.print(f"[white]Drive: [cyan]{drive['drive']} [white]Extension: [cyan]{ext['ext']}\n", style = ' bold reverse green')

   
def scanDrive(drive_mountpoint, drive, ext, matchList):
    logFolder = os.path.join(os.getcwd(),'logs')
    if not os.path.exists(logFolder):
        os.mkdir(logFolder)
    foundFilesLog = open(f"{logFolder}/foundFiles.log","a")
    errLog = open(f"{logFolder}/scanErr.log","a")

    startTime = time.perf_counter()
    foundFileSize = 0
    foundFiles = 0
    exclusionDir = os.path.dirname(__file__)
    exclusionDir = os.path.abspath(exclusionDir)

    try:
        for root, dirs, files in os.walk(drive_mountpoint, topdown=True):    

            # get current search directory
            if os.path.samefile(exclusionDir, os.path.abspath(root)):
                console.print('Excluding script directory: ' + root, style='bold reverse green')
                dirs[:] = []
                continue

            # also skip recycle bin 
            if os.path.basename(root) == '$Recycle.Bin':
                console.print('Excluding recycle bin: ' + root, style='bold reverse green')
                dirs[:] = []
                continue

            for file in files:
                try:
                    if os.path.splitext(file)[1] == ext['ext']:
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        foundFilesLog.write(f'{current_time}\t{os.path.join(root, file)}\n')
                        matchList.append(os.path.join(root, file))
                        foundFiles += 1
                        foundFileSize += os.path.getsize(os.path.join(root, file))
                except UnicodeEncodeError:
                    log_error(errLog, 'UnicodeEncodeError', os.path.join(root, file))
                except FileNotFoundError:
                    log_error(errLog, 'FileNotFoundError', os.path.join(root, file))

    except KeyboardInterrupt:
        os.system(clear)
        console.print(scrapeBotArt, style='bold red', justify='left')
        print('exiting . . .')
        sys.exit()

    errLog.close()
    foundFilesLog.close()
    searchResult = SearchResult(drive['drive'], ext['ext'], foundFiles, convert_size(foundFileSize), round(time.perf_counter() - startTime, 2))
    return searchResult

    




def printSearchLog(result, searchLogList):
    table = Table()
    table.add_column("Drive", justify="right", style="bold red", no_wrap=True)
    table.add_column("Extension", style="bold magenta")
    table.add_column("FoundFiles", style="bold white")
    table.add_column("Size", justify="right", style="bold green")
    table.add_column("Time(s)", justify="right", style="bold white")

    searchLogList.append(result)

    for i in searchLogList:
        table.add_row(str(i.drive), str(i.ext), str(i.filesFoundNum), str(i.filesFoundSize), str(i.timeTaken))
    console.print(table)


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"

   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)

   return "%s %s" % (s, size_name[i])
      

                           
def copyFiles(matchList):

    logFolder = os.path.join(os.getcwd(),'logs')
    errLog = open(f"{logFolder}/copyErr.log","a")
    scrapedPath = os.path.join(os.getcwd(), 'scraped')
    if not os.path.exists(scrapedPath):
        os.mkdir(scrapedPath)

    count = 0
    isErrorThrown = False
    errorCount = 0

    for i in track(matchList, description='Copying Files'):
        try:
            # get ext of file to create folder
            ext = os.path.splitext(i)[1]
            # make subfolder in scraped folder
            subFolder = os.path.join(scrapedPath, ext)

            # for linux file paths
            if ext.startswith('.') and platform.system() == 'Linux':
                subFolder = os.path.join(scrapedPath, ext[1:])

            if not os.path.exists(subFolder):
                os.mkdir(subFolder)

            # get destination path
            destPath = os.path.join(subFolder, os.path.basename(i))
            
            # check if file already exists if so add a timestamp to the end of the file before the extension
            if os.path.exists(destPath):
                current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # Use a timestamp format with alphanumeric characters only
                file_name, extension = os.path.splitext(os.path.basename(i))
                destPath = os.path.join(subFolder, f'{file_name}_{current_time}{count}{extension}')            
        
            shutil.copy2(i, destPath)
            count += 1
        
        except UnicodeEncodeError:
            log_error(errLog, 'UnicodeEncodeError', i)
            isErrorThrown = True
            errorCount += 1

        except FileNotFoundError:
            log_error(errLog, 'FileNotFoundError', i)
            isErrorThrown = True
            errorCount += 1

    if isErrorThrown:
        console.print(f'[bold red]({errorCount}) Errors Occured. Check logs for details.', style='reverse bold red')
    
    errLog.close()
    return count
    
    
def main():

    matchList = []

    currentSearches = []


    while(True):

        printScreen()
            
        # for windows the mountpoint and device are the same
        # for linux the mountpoint and device are different so we need to get the mountpoint and name of the selected drive

        drives = psutil.disk_partitions()
        drive_names = [i.device for i in drives]

        drive = getDrive(drive_names)
   
        # get mountpoint of selected drive
        if (drive):
            for i in drives:
                if i.device == drive['drive']:
                    drive_mountpoint = i.mountpoint
                    break

        
        if drive == None:
            os.system(clear)
            break

        printScreen()

        # get extension
        ext = getExtension()
        if ext == None:
            os.system(clear)
            break
        
        

        # show search info
        printScreen()

        
        printSearchInfo(drive, ext)

        # get options
        
        userConfirmSearch = getOptions()
        
        if userConfirmSearch == None:
            os.system(clear)
            break
        elif userConfirmSearch['choice'] == 'Change Search':
            continue

        printScreen()

        
        printSearchInfo(drive, ext)

        if (drive, ext) in currentSearches:
            console.print(f'[bold red]This search has already been performed in this session!', style='reverse bold red')
            time.sleep(2)
            continue


        # an array to hold search results for session
        
        with console.status("[bold white]Searching drive . . . ") as status:
                currentSearches.append((drive, ext))
                
                
                searchResult = scanDrive(drive_mountpoint, drive, ext, matchList)

                printScreen()
                printSearchLog(searchResult, searchLogList)

        print()
        userEndOption = getEndOption()
        
        if userEndOption == None:
            break
        elif userEndOption['choice'] == "Add To Search":
            continue
               
        printScreen()

        beforeCount = len(matchList)

        afterCount = copyFiles(matchList)

        console.print(f'{afterCount} out of {beforeCount} Files copied to scraped folder', style=' reverse bold green')


        print('Press Enter to exit . . .')
        input()
        sys.exit()
        
        
if __name__ == "__main__":
    main()
    # exit program
    os.system(clear)
    console.print(scrapeBotArt, style='bold red', justify='left')
    print('exiting . . .')
    sys.exit()

















