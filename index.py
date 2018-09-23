from inverted_index_funcs import *

'''
    Analytics
~~~~~~~~~~~~~~~~~~
Num Unique Tokens: 1642046
Num Documents: 37497
'''
def main():
    input = ''

    bookDict = openJSON('bookkeeping.json') 

    client = MongoClient('localhost', 27017)
    db = client["db"]
    collection = db["col"]

    while input != 'quit':
        input = raw_input("Please choose an option: drop | populate | updateTFIDF | print | query | quit\n")
        if input == 'drop':
            dropDatabase("db", client)
        elif input == 'populate':
            populateDB(bookDict, collection)
        elif input == 'print':
            printDatabase(collection)
        elif input == 'query':
            search = raw_input("Please enter a query: ")
            search_list = search.split(' ')
            print
            query(search_list, collection, bookDict)
        elif input == 'updateTFIDF':
            updateIDF(collection)

if __name__ == "__main__":
    main()
'''
Possible way to traverse the directories: Glob module?
ex:
glob.glob( [0 - 75] ) stores all the files into a list, and then loop through
each file number to do parsing/tokenizing?

OR 

Navigating all the subdirectories in WEBPAGES_RAW folder should need os.walk()
Documentation: https://www.pythoncentral.io/how-to-traverse-a-directory-tree-in-python-guide-to-os-walk/
'''