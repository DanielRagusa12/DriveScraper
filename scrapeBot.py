import win32api
import inquirer
import os
from rich.console import Console
import platform
from art import *
import time
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
import math
import sys
import shutil
from rich.progress import track


class SearchResult:
    def __init__(self, drive, ext, filesFoundNum, filesFoundSize, timeTaken):
        self.drive = drive
        self.ext = ext
        self.filesFoundNum = filesFoundNum
        self.filesFoundSize = filesFoundSize
        self.timeTaken = timeTaken
        





console = Console()

searchLogList = []




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
    return inquirer.prompt(options)



def getDrive(drives):

    try:

        drives = [
        inquirer.List('drive',
                        message='Choose a drive',
                        choices=drives,
                        carousel=True,
                    ),
        ]


        return inquirer.prompt(drives)


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

    answer = inquirer.prompt(options)

    if answer == None:
        return None
    
    if answer['ext'] == '[custom]':
        printScreen()
        
        question = [
        inquirer.Text('ext', message='Enter extension with dot [.ext]'),
        ]

        return inquirer.prompt(question)

    return answer

def getOptions():

    options = [
    inquirer.List('choice',
                    message='Choose an option',
                    choices=[f'GO', 'Change Search'],
                    carousel=True,
                ),
    ]

    return inquirer.prompt(options)
    
      



def printSearchInfo(drive, ext):
    console.print(f"[white]Drive: [cyan]{drive['drive']} [white]Extension: [cyan]{ext['ext']}\n", style = ' bold reverse green')


    





def scanDrive(drive, ext, matchList):
    logFolder = os.path.join(os.getcwd(), '..' '/logs')
    if not os.path.exists(logFolder):
        os.mkdir(logFolder)

    # create logs file
    foundFilesLog = open(f"{logFolder}/foundFiles.log","a")
    errLog = open(f"{logFolder}/scanErr.log","a")






    
    # scan drive for files with extension

    startTime = time.perf_counter()
    

    foundFileSize = 0


    

    # Get the directory that contains the script
    script_dir = os.path.dirname(__file__)
    

    # Get the name of the directory to exclude
    exclusionDir = os.path.abspath(os.path.basename(script_dir))

    try:
        for root, dirs, files in os.walk(drive['drive'], topdown=True):
            
            # get current search directory
            if os.path.abspath(root) == exclusionDir:
                console.print('Excluding directory: ' + root, style='bold reverse green')
                dirs[:] = []
                continue
                



            

            for file in files:
                
                

                try:

                    if file.endswith(ext['ext']):
                        foundFilesLog.write(os.path.join(root, file) + '\n')
                        matchList.append(os.path.join(root, file))
                        foundFileSize += os.path.getsize(os.path.join(root, file))
        
                except UnicodeEncodeError:
                    console.print('[red]UnicodeEncodeError: ' + os.path.join(root, file), style='bold reverse red')

                    # write the parent dir of the file that caused the error
                    errLog.write('UnicodeEncodeError: ' + os.path.abspath(root) + '\n')

                    

                except FileNotFoundError:
                    console.print('FileNotFoundError: ' + os.path.join(root, file), style='bold reverse red')
                    errLog.write('FileNotFoundError: ' + os.path.join(root, file) + '\n')

                except PermissionError:
                    console.print('PermissionDeniedFor: ' + os.path.join(root, file), style='bold reverse red')
                    errLog.write('PermissionDeniedFor: ' + os.path.join(root, file) + '\n')

                except OSError:
                    console.print('OSError: ' + os.path.join(root, file), style='reverse red')
                    errLog.write('OSError: ' + os.path.join(root, file) + '\n')
                

                

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

    logFolder = os.path.join(os.getcwd(), '..' '/logs')

    errLog = open(f"{logFolder}/copyErr.log","a")

    



    scrapedPath = os.path.join(os.getcwd(), '../scraped')
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
            errLog.write('PermissionDeniedFor: ' + i + '\n')

        except OSError:
            isErrorThrown = True
            errorCount += 1
            errLog.write('OSError: ' + i + '\n')


        

    if isErrorThrown:
        console.print(f'[bold red]({errorCount}) Errors Occured. Check logs for details.', style='reverse bold red')
    
    errLog.close()
    return count
    
    
    
   








def main():

    matchList = []


    while(True):

        
        
        printScreen()

        drives = []
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        


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

















