#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# CBuffalow, 2021-Feb-19, Added functions (process_cd_data, process_delete, write_file, 
#    get_cd_data), added uppercase functionality to menu for better readability, 
#    adjusted formatting, added program header
# Cbuffalow, 2021-Feb-20, Added calculcate_cd_id function, adjusted 
#    process_cd_data & get_cd_data functions, revised comments
#------------------------------------------#

# -- MODULES -- #
import os.path

# -- DATA -- #
#Global Variables
strChoice = '' # user input (string)
strYesNo = '' # user input for yes/no question (string)
indID = -1 # ID number of CD (integer)
strTitle = '' # user input (string)
strArtist = '' # user input (string)
lstTbl = []  # table to hold data (list of dictionaries)
dicRow = {}  # row of data (dictionary)
strFileName = 'CDInventory.txt'  # data storage file
intIDDel = '' # user selected ID to delete (integer)
intRowNr = '' # index of row to be deleted (integer)
blnCDRemoved = "False" # flag if desired CD found (Boolean)


# -- PROCESSING -- #
class DataProcessor:
    """Processing data within program's current runtime."""

    @staticmethod
    def process_cd_data(cd_id, cd_title, cd_artist):
        """Function that takes user input about CD and formats data into a dictionary.

        Keys are "ID", 'Title', and 'Artist' for each dictionary and the values are assigned
        from cd_id, cd_title, and cd_artist, respectively.

        Args:
            cd_id (int): ID of CD, generated by program
            cd_title (str): name of CD, provided by user
            cd_artist (str): name of artist, provided by user

        Returns:
            cd_info (dictionary): cd_id, cd_title, and cd_artist contained within a single dictionary
        """
        cd_info = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        return cd_info



    @staticmethod
    def process_delete(cd_to_delete, table):
        """Function that processes which row index needs to be deleted based upon input from user.

        For each dictionary, the function determines if the key:value pair in that row/dictionary 
        with the key of "ID" has the desired ID number for its value.  If yes, row_number stops counting
        at that row and CD_found is set to 'True'.

        Args:
            cd_to_delete (int): ID number of CD that user wants to delete
            table (list of dicts): 2D data structure (list of dicts) that holds data during runtime

        Returns:
            row_number (int): counter of rows (stops on row if desired CD found, otherwise returns index of last row)
            CD_found (Boolean): flag that states if desired CD found (True = yes, False = no)
        """
        row_number = -1
        CD_found = False
        for row in table:
            row_number += 1
            if row['ID'] == cd_to_delete:
                CD_found = True
                break
        return row_number, CD_found



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Function checks to make sure specified txt file exists.  If yes, continues by reading
        the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        if os.path.exists(file_name):
            objFile = None  # file object
            table.clear()  # this clears existing data and allows to load data from file
            objFile = open(file_name, 'r')
            for line in objFile:
                data = line.strip().split(',')
                cd_info = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(cd_info)
            objFile.close()
        else: pass



    @staticmethod
    def calculate_cd_id(file_name):
        """Function to determine last ID used in CDInventory.txt so that next ID number can be assigned

        The function finds the last row of data in CDInventory.txt and reports 
        the ID number used in that row.  This becomes the start point in which the rest of the ID numbers 
        are based upon.

        Args:
            file_name (str): name of file used to read data from

        Returns:
            cd_id (int): id number of last used CD_ID in the CDInventory.txt file
        """
        if os.path.exists(file_name):
            objFile = None  # file object
            objFile = open(file_name, 'r')
            objFile_content = objFile.read() #returns all content of file as a giant string
            objFile.close()
            objFile_rows = objFile_content.split(sep= '\n') #separates data into separate items based on location of \n
            indexFinalRow = len(objFile_rows) -2
            cd_id = int(objFile_rows[indexFinalRow].split(sep= ',')[0])
        else:
            cd_id = 0
        return cd_id



    @staticmethod
    def write_file(file_name, table):
        """Function to overwrite data from current runtime into a text file.

        For each row, the data is converted into a string with a comma separating
        each piece of data and then a new line is started.  The data is then saved
        out to the designated txt file.

        Args:
            file_name (string): name of file used to write data to
            table (list of dicts): 2D data structure (list of dicts) that holds data during runtime

        Returns:
            None.
        """
        objFile = None  # file object
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()



# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user.


        Args:
            None.

        Returns:
            None.
        """
        print('\n')
        print(' MENU '.center(30,'-'))
        print('[L] Load Inventory from file\n[A] Add CD\n[I] Display Current Inventory')
        print('[D] Delete CD from Inventory\n[S] Save Inventory to file\n[X] Exit')
        print('-'*30)
        print('\n')



    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.


        Args:
            None.

        Returns:
            choice (string): an upper case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['L', 'A', 'I', 'D', 'S', 'X', 'l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [L, A, I, D, S or X]: ').lower().strip()
        print()  # Add extra space for layout
        return choice



    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n')
        print(' The Current Inventory: '.center(60,'='))
        print('{:<10}{:<25}{:<25}'.format('ID', 'CD Title', 'Artist'))
        print('-'*60)
        for row in table:
            print('{:<10}{:<25}{:<25}'.format(*row.values()))
        print('='*60)



    @staticmethod
    def get_cd_data():
        """Collects information about CD from user.

        Asks user to input the name of the CD and the artist of the CD.

        Args:
            None

        Returns:
            cd_title (str): name of CD, provided by user
            cd_artist (str): name of artist, provided by user

        """
        cd_title = input('What is the CD\'s title? ').strip()
        cd_artist = input('What is the Artist\'s name? ').strip()
        return(cd_title, cd_artist)




# 1. When program starts, read in the currently saved inventory, print program header
FileProcessor.read_file(strFileName, lstTbl)
intID = FileProcessor.calculate_cd_id(strFileName)
print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
print('The Magic CD Inventory'.center(62))
print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory will be reloaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file - otherwise reload will be cancelled. ')
        if strYesNo.lower() == 'yes':
            print('Reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
            input('Inventory Loaded. Press \'Enter\' to return to Main Menu. ')
        else:
            input('Cancelling... Inventory data NOT reloaded. Press [ENTER] to return to the menu. ')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Generate ID and Ask user for CD Title and Artist
        intID += 1
        strTitle, strArtist = IO.get_cd_data()
        # 3.3.2 Add item to the table
        dicRow = DataProcessor.process_cd_data(intID, strTitle, strArtist)
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
        input('CD Added. Press \'Enter\' to return to Main Menu. ')
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        input('Press \'Enter\' to return to Main Menu. ')
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        intRowNr, blnCDRemoved = DataProcessor.process_delete(intIDDel, lstTbl)
        if blnCDRemoved:
            del lstTbl[intRowNr]
            input('CD #' + str(intIDDel) + ' deleted. Press \'Enter\' to view updated inventory.')
        else:
            input('CD #' + str(intIDDel) + ' not found.  Press \'Enter\' view inventory.')
        IO.show_inventory(lstTbl)
        input('Press \'Enter\' to return to Main Menu. ')
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
            input('The inventory was saved to file. Press \'Enter\' to return to Main Menu. ')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to Main Menu. ')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




