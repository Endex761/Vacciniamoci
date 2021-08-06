import locale
from datetime import datetime
from settings import DATA_FILE, INPUT_DATA
from data_updater import DataUpdater

total_population = 6.036e7 # 60.36 milion
# total_population = 54006504 # platea updated 21-06-2021
locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class MessageGenerator:

    def __init__(self) -> None:
        self.du = DataUpdater(INPUT_DATA, DATA_FILE)
        self.message = "No data"

    # return the actual message
    def get_message(self) -> str:
        if self.message == "No data":
            self.generate()
        return self.message

    # generate the message
    def generate(self) -> None:
        # retrive data from local file
        data = self.du.get_data()

        # compute values
        today_first_dose = int(data[0])
        today_second_dose = int(data[1])
        yesterday_first_dose = int(data[2])
        yesterday_second_dose = int(data[3])

        increment_first_dose = today_first_dose - yesterday_first_dose
        increment_second_dose = today_second_dose - yesterday_second_dose
        percent_first_dose = round(today_first_dose/total_population * 100, 2)
        percent_second_dose = round(today_second_dose/total_population * 100, 2)

        total_doses = today_first_dose + today_second_dose
        total_daily_doses = increment_first_dose + increment_second_dose

        
        # generate the message
        
        message =  f'*Report Vaccini {self.parse_date()}*\n'
        message += f'\n'
        message += f'*Prima Dose*\n'
        message += f'Totale vaccinati fino ad oggi: *{today_first_dose:n}*\n'
        message += f'Incremento giornaliero: *{increment_first_dose:n}*\n'
        message += f'È stato vaccinato il *{percent_first_dose:n}*% della popolazione\n'
        message += f'\n'
        message += f'*Seconda Dose*\n'
        message += f'Totale vaccinati fino ad oggi: *{today_second_dose:n}*\n'
        message += f'Incremento giornaliero: *{increment_second_dose:n}*\n'
        message += f'È stato vaccinato il *{percent_second_dose:n}*% della popolazione\n'
        message += f'\n'
        message += f'Totale dosi: *{total_doses:n}* \n'
        message += f'Totale dosi giornaliere: *{total_daily_doses:n}*'
        
        self.message = message

    # update the message
    def update(self) -> None:
        if self.du.update_data():
            self.generate()

    # parse the date in italian format
    def parse_date(self) -> str:
        months = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day

        return f'{day} {months[month]} {year}'
