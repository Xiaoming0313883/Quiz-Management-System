from ui.mainPage import mainPage
from database.core import core

if __name__ == '__main__':
    try:
        database = core() #make database connection
        mainPage(database) #show mainPage for user, everything begin here
    except KeyboardInterrupt as err:
        print("\nExit Successfully")