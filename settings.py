import datetime
import pytz

# input data link
INPUT_DATA = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/anagrafica-vaccini-summary-latest.json"
IMG_INPUT_DATA = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv"

# bot name
NAME = "Vaccini Covid-19"

# italy timezone
italy_tz = pytz.timezone("Europe/Rome")

# update time 
HOUR = 18
MINUTE = 00
SECOND = 00
DAILY_TIME = datetime.time(hour=HOUR, minute=MINUTE, second=SECOND, tzinfo=italy_tz)

# file locations
TOKEN_FILE = "bot_token"
SQLITE_FILE = "sqlite/users"
DATA_FILE = "today_data"
IMG_FILE = "summary_chart.png"

# utility function to get the bot token
def get_token() -> str:
    file_handler = open(TOKEN_FILE, 'r')
    token = file_handler.readline()
    file_handler.close()
    return token

