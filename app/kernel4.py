import ujson as json
import requests
import sqlite3
import multiprocessing

class IDSearcher:
    URL = "https://farabiran.ir/Estelam?handler=Search&id={}"
    SESSION = requests.Session()
    def search_ids(self, search_type, f1, f2=False):
        if search_type == 1:
            start_id = int(f1)
            end_id = int(f1) + 1
            file_name = f"{f1}"
        elif search_type == 2:
            start_id = int(f1)
            end_id = int(f2)
            file_name = f"{f1}-{f2}"
        else:
            return "Invalid input"

        conn = sqlite3.connect('mooshyab7.db')
        c = conn.cursor()
        success_ids = []
        with multiprocessing.Pool() as pool, \
            self.SESSION as session:
            # Set session object for each worker process
            pool.map_async(session.mount, [self.URL]*len(pool._pool))
            # Use imap_unordered to process results as soon as they become available
            for id_num in range(start_id, end_id):
                response = self.SESSION.get(self.URL.format(id_num))
                if response.status_code == 200:
                    data = json.loads(response.content)
                    # Insert data into database
                    id_num = data['Id']
                    name = data['Name']
                    madrak_id = data['MadrakId']
                    id_number = data['IdNumber']
                    title = data['Title']
                    number = data['Number']
                    date = data['Date']

                    success_ids.append(data['MadrakId'])

                    # Check if data already exists in database
                    c.execute("SELECT * FROM data WHERE Id=?", (id_num,))
                    existing_data = c.fetchone()

                    if existing_data is None:
                        c.execute("INSERT INTO data (Id, Name, MadrakId, IdNumber, Title, Number, Date) VALUES (?, ?, ?, ?, ?, ?, ?)", (id_num, name, madrak_id, id_number, title, number, date))
                    # else:
                    #     c.execute("UPDATE data SET Name=?, MadrakId=?, IdNumber=?, Title=?, Number=?, Date=? WHERE Id=?", (name, madrak_id, id_number, title, number, date, id_num))
                    
                    # success_ids.append(id_num)
                    # print(f"ID {id_num} found")
        conn.commit()
        conn.close()
        return success_ids
    