import sqlite3
import os
from dotenv import load_dotenv 

load_dotenv() 


def init_db():
    if os.path.exists(os.getenv("DATABASE_NAME")):
        return
    conn = sqlite3.connect(os.getenv("DATABASE_NAME"))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY AUTOINCREMENT , name VARCHAR(100) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS investores (id INTEGER PRIMARY KEY AUTOINCREMENT , company_id int NOT NULL, investor_name VARCHAR(100) NOT NULL ,investor_phone VARCHAR(100) NOT NULL , investor_number VARCHAR(100) NOT NULL, FOREIGN KEY (company_id) REFERENCES companies(id))")
    
    companies = cursor.execute("SEECT * FROM companies")
    if(len(companies.fetchall) == 0):
     cursor.execute("INSERT INTO companies (name) VALUES ('Muscat Clearing & Depository'),('Muscat Stock Exchange'),('Omantel')")
    
    investores = cursor.execute("SEECT * FROM investores")
    if(len(investores.fetchall) == 0):
     cursor.execute("""
                   INSERT INTO investores (company_id,investor_name,investor_phone,investor_number) VALUES
                    (1,'Hamed AL Hasani','99309485','123434'),
                    (1,'AL Harith AL Maawali','92349999','222234'),
                    (1,'Mohammed AL Zidgali','98702234','123678'),
                    (1,'Muna AL Rashdi','92349898','879346'),
                    (2,'Salma AL Wahaibi','90001234','019283'),
                    (2,'Faris AL Busaidi','97778797','234876'),
                    (2,'Maryam AL Baloushi','90901234','154679'),
                    (3,'Haitham AL Hanaii','90089904','236574'),
                    (3,'Arwaa AL Joulandani','92220000','907896'),
                    (3,'Ibrahim AL Hasani','90992345','111444')
                   
                  """)               
    conn.commit()
    conn.close()
