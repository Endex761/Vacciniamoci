import urllib.request
import json

class DataUpdater:
    def __init__(self, inputData, outputFile) -> None:
        self.inputData = inputData
        self.outputFile = outputFile
        
    # vaccine data updating
    def update_data(self) -> bool:

        with urllib.request.urlopen(self.inputData) as remote:
            
            # read remote data and decode it from json
            data = json.loads(remote.read().decode())

            # read the data attribute
            data = data['data']

            # sum up all vaccine of the day
            total = 0
            for cat in data:
                #total += cat['totale']
                total += cat['seconda_dose']

            # read yesterday data
            file_handler = open(self.outputFile, 'r')
            yesterday = file_handler.readline()
            file_handler.close()

            # if data has increased then update the data
            if total > int(yesterday):
                today = str(total) + "\n"

                # write data in the file
                file_handler = open(self.outputFile, 'w')
                file_handler.writelines([today, yesterday])
                file_handler.close()
                return True
            else:
                return False
                
    # return today and yesterday data
    def get_data(self) -> list:
        file_handler = open(self.outputFile, 'r')
        today = file_handler.readline()
        yesterday = file_handler.readline()

        return [today, yesterday]
