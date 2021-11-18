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
            first_dose  = 0
            second_dose = 0
            third_dose  = 0
            for cat in data:
                first_dose  += cat['prima_dose']
                second_dose += cat['seconda_dose']
                third_dose  += cat['dose_booster']

            # read yesterday data
            file_handler = open(self.outputFile, 'r')

            yesterday_first_dose  = file_handler.readline()
            yesterday_second_dose = file_handler.readline()
            yesterday_third_dose  = file_handler.readline()

            file_handler.close()
            
            # if data has increased then update the data
            if first_dose > int(yesterday_first_dose):
                today_first_dose  = str(first_dose) + "\n"
                today_second_dose = str(second_dose) + "\n"
                today_third_dose  = str(third_dose) + "\n"

                # write data in the file
                file_handler = open(self.outputFile, 'w')
                file_handler.writelines([today_first_dose, today_second_dose, today_third_dose, yesterday_first_dose, yesterday_second_dose, yesterday_third_dose])
                file_handler.close()
                return True
            else:
                return False
                
    # return today and yesterday data
    def get_data(self) -> list:
        file_handler = open(self.outputFile, 'r')

        today_first_dose  = file_handler.readline()
        today_second_dose = file_handler.readline()
        today_third_dose  = file_handler.readline()
        yesterday_first_dose  = file_handler.readline()
        yesterday_second_dose = file_handler.readline()
        yesterday_third_dose  = file_handler.readline()
        
        file_handler.close()

        return [today_first_dose, today_second_dose, today_third_dose, yesterday_first_dose, yesterday_second_dose, yesterday_third_dose]
