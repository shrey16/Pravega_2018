import os
import shutil
from registrations import dbscraper as dbs


def save_as_xlsx(database, path):
    tempTSV_path = os.path.splitext(path)[0] + '.tsv'
    with open(tempTSV_path, 'w') as tempTSV:
        database.save_all_data(file=tempTSV)
    dbs.csvtoxlsx(tempTSV_path, path)
    os.remove(tempTSV_path)

if os.path.exists('./registration_data'):
    shutil.rmtree('./registration_data')
os.mkdir('./registration_data')
save_as_xlsx(dbs.ProsceniumTheatreRegistrationData(),
             './registration_data/proscenium_theatre.xlsx')
save_as_xlsx(dbs.ProsceniumStreetPlayRegistrationData(),
             './registration_data/proscenium_streetplay.xlsx')
save_as_xlsx(dbs.BoBRegistrationData(), './registration_data/bob.xlsx')
save_as_xlsx(dbs.LasyaRegistrationData(), './registration_data/lasya.xlsx')
save_as_xlsx(dbs.SInECRegistrationData(), './registration_data/pis.xlsx')
