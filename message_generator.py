import locale
from settings import DATA_FILE, INPUT_DATA
from data_updater import DataUpdater

total_population = 6.036e7 # 60.36 milion
locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class MessageGenerator:

    def __init__(self) -> None:
        self.du = DataUpdater(INPUT_DATA, DATA_FILE)
        self.message = "No data"

    # return the actual message
    def get_message(self) -> str:
        return self.message

    def generate(self) -> None:
        # retrive data from local file
        data = self.du.get_data()

        # compute values
        today = int(data[0])
        yesterday = int(data[1])
        increment = today - yesterday
        percent = today/total_population * 100
        percent = round(percent, 2)

        # generate the message
        message = f'Totale vaccinati fino ad oggi: *{today:n}*\n'
        message += f'Incremento giornaliero: *{increment:n}*\n'
        message += f'È stato vaccinato il *{percent:n}*% della popolazione\n'

        self.message = message

    def update(self) -> None:
        if self.du.update_data():
            self.generate()
