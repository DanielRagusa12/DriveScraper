# Copyright 2023 Daniel Ragusa

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import psutil
import platform




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


term = Terminal()
console = Console()
searchLogList = []


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





scrapeBotArt = text2art('driveScraper', font='small')

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
        if platform.system() == 'Linux':
            drives = [os.path.basename(d.rstrip('/')) + '/' for d in drives]

        drives = [
        inquirer.List('drive',
                        message='Choose a drive',
                        choices=drives,
                        carousel=True,
                        
                        
                    ),
        ]


        return inquirer.prompt(drives, theme=CyberTheme())


    except inquirer.errors.ValidationError:
        print('Invalid drive')
        return getDrive(drives)
    
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
    
      



def printSearchInfo(drive, ext):
    console.print(f"[white]Drive: [cyan]{drive['drive']} [white]Extension: [cyan]{ext['ext']}\n", style = ' bold reverse green')


    





def scanDrive(drive, ext, matchList):

    
    logFolder = os.path.join(os.getcwd(),'logs')
    
    if not os.path.exists(logFolder):
        os.mkdir(logFolder)

    # create logs file
    foundFilesLog = open(f"{logFolder}/foundFiles.log","a")
    errLog = open(f"{logFolder}/scanErr.log","a")






    
    # scan drive for files with extension

    startTime = time.perf_counter()
    

    foundFileSize = 0


    

    # Get the directory that contains the script
    exclusionDir = os.path.dirname(__file__)
    exclusionDir = os.path.abspath(exclusionDir)
    

    
    

    try:
        for root, dirs, files in os.walk(drive['drive'], topdown=True):
            
            
            # get current search directory
            if os.path.samefile(exclusionDir, os.path.abspath(root)):
            
                console.print('Excluding script directory: ' + root, style='bold reverse green')
                dirs[:] = []
                continue
                



            

            for file in files:
                
                

                try:

                    if os.path.splitext(file)[1] == ext['ext']:
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        foundFilesLog.write(f'{current_time}\t{os.path.join(root, file)}\n')
                        matchList.append(os.path.join(root, file))
                        foundFileSize += os.path.getsize(os.path.join(root, file))
        
                except UnicodeEncodeError:
                    console.print('[red]UnicodeEncodeError: ' + os.path.join(root, file), style='bold reverse red')

                    # write the parent dir of the file that caused the error
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    errLog.write(f'{current_time}\tUnicodeEncodeError: {os.path.abspath(root)}\n')

                    

                except FileNotFoundError:
                    console.print('FileNotFoundError: ' + os.path.join(root, file), style='bold reverse red')
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    errLog.write(f'{current_time}\tFileNotFoundError: {os.path.join(root, file)}\n')

                except PermissionError:
                    console.print('PermissionDeniedFor: ' + os.path.join(root, file), style='bold reverse red')
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    errLog.write(f'{current_time}\tPermissionDeniedFor: {os.path.join(root, file)}\n')

                except OSError:
                    console.print('OSError: ' + os.path.join(root, file), style='reverse red')
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    errLog.write(f'{current_time}\tOSError: {os.path.join(root, file)}\n')
                

                

    except KeyboardInterrupt:
        os.system(clear)
        console.print(scrapeBotArt, style='bold red', justify='left')
        print('exiting . . .')
        sys.exit()

    errLog.close()
    foundFilesLog.close()

    searchResult = SearchResult(drive['drive'], ext['ext'], len(matchList), convert_size(foundFileSize), round(time.perf_counter() - startTime, 2))
    return searchResult

    




def printSearchLog(result, searchLogList):

    

    


    table = Table()
    table.add_column("Drive", justify="right", style="bold red", no_wrap=True)
    table.add_column("Extension", style="bold magenta")
    table.add_column("FoundFiles", style="bold white")
    table.add_column("Size", justify="right", style="bold green")
    table.add_column("Time(s)", justify="right", style="bold white")

    # searchLogTupleList.append((ext,count,drive,time))

    searchLogList.append(result)
    

    for i in searchLogList:
        # table.add_row(i.ext, i.count, i.drive, i.time, i.size)

        table.add_row(str(i.drive), str(i.ext), str(i.filesFoundNum), str(i.filesFoundSize), str(i.timeTaken))
        




        # table.add_row(i[0],i[1],i[2],i[3])


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
            # print(i)
            # print(count)
            
            
            
            # get ext of file to create folder
            ext = os.path.splitext(i)[1]
            # make subfolder in scraped folder
            subFolder = os.path.join(scrapedPath, ext)
            if not os.path.exists(subFolder):
                os.mkdir(subFolder)

            # get destination path
            destPath = os.path.join(subFolder, os.path.basename(i))
            
            
            
            # copy file to destination
            
            

            shutil.copy(i, destPath)
            count += 1
        
        except PermissionError:
            isErrorThrown = True
            errorCount += 1
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            errLog.write(f'{current_time}\tPermissionDeniedFor: {i}\n')

        except OSError:
            isErrorThrown = True
            errorCount += 1
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            errLog.write(f'{current_time}\tOSError: {i}\n')

        


        

    if isErrorThrown:
        console.print(f'[bold red]({errorCount}) Errors Occured. Check logs for details.', style='reverse bold red')
    
    errLog.close()
    return count
    
    
    
   








def main():

    matchList = []


    while(True):

        
        
        printScreen()

        # drives = []
        # drives = win32api.GetLogicalDriveStrings()
        # drives = drives.split('\000')[:-1]

        if platform.system() == 'Windows':
            drives = psutil.disk_partitions()
            drives = [i.device for i in drives]

        elif platform.system() == 'Linux':
            drives = psutil.disk_partitions()
            drives = [i.mountpoint for i in drives]

        

        

        


        # get drive
        drive = getDrive(drives)
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

        # an array to hold search results for session
        
        with console.status("[bold white]Searching drive . . . ") as status:
                
                
                searchResult = scanDrive(drive, ext, matchList)

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

















