from mysql.connector import connect, Error
import pandas as pd

connection = connect(
        host='astronaut.snu.ac.kr', 
        port=7000, 
        user='DB2023_11225', 
        password='DB2023_11225', 
        database='DB2023_11225',
        charset='utf8'
)


if connection.is_connected():
    print("connected")

cursor = connection.cursor()


table_def = {
    "create_dvd_table" : """
    CREATE TABLE DVDS (
        id                  INT             AUTO_INCREMENT  PRIMARY KEY,
        title               VARCHAR(100)    NOT NULL,
        director            VARCHAR(40)     NOT NULL,
        available_copies    INT             DEFAULT 2,
        total_rentals       INT             DEFAULT 0,
        total_ratings       INT             DEFAULT 0
    );
    """,
    
    "create_user_table" : """
    CREATE TABLE USERS (
        id                  INT             AUTO_INCREMENT  PRIMARY KEY,
        name                VARCHAR(50)     NOT NULL,
        age                 INT             NOT NULL,
        available_rentals   INT             DEFAULT 3,
        total_ratings       INT             DEFAULT 0,
        total_rentals       INT             DEFAULT 0
    );
    """,

    "create_activerentals_table" : """
    CREATE TABLE ACTIVERENTALS (
        rental_id           INT AUTO_INCREMENT PRIMARY KEY,
        u_id                INT NOT NULL,                    
        d_id                INT NOT NULL,
        FOREIGN KEY (u_id)  REFERENCES USERS(id)    ON DELETE CASCADE,
        FOREIGN KEY (d_id)  REFERENCES DVDS(id)     ON DELETE CASCADE
    ); 
    """,
    
    "create_completedrentals_table" : """
    CREATE TABLE COMPLETEDRENTALS (
        rental_id           INT AUTO_INCREMENT PRIMARY KEY,  
        u_id                INT NOT NULL,  
        d_id                INT NOT NULL,               
        rating              INT NOT NULL,
        FOREIGN KEY (u_id)  REFERENCES USERS(id)    ON DELETE CASCADE,
        FOREIGN KEY (d_id)  REFERENCES DVDS(id)     ON DELETE CASCADE
    );
    """
}



def check_existence(table_name, data):
    if isinstance(data, int):
        pass
    elif not data.isdigit():
        return False

    # Fetch the object
    cursor.execute(f'SELECT id FROM {table_name} WHERE id = {data};')

    # Error: Non-existing object
    if not cursor.fetchall():
        return False

    return True

def insert(table_name: str, data: list):
    """
    Inserts a row into a specified table.
    
    :param table_name: DVDS | USERS.
    :param data:    list(title, director) |
                    list(name, age)
    """
    
    if (table_name == "DVDS"):
        columns = "TITLE, DIRECTOR"
        values  = ",".join(data)
    
    elif (table_name == "USERS"):
        columns = "NAME, AGE"
        values  = ",".join(data)
    
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    
    try:
        cursor.execute(query)
        connection.commit()
        print(f"Inserted into {table_name}: {data}")
    except Error as e:
        raise e


def delete(table_name, condition):
    """
    Deletes rows from a specified table.
    :param table_name: DVDS | USERS.
    :param condition:  ID | ID.
    """
    
    query = f"DELETE FROM {table_name} WHERE ID = {condition}"

    try:
        cursor.execute(query)
        connection.commit()
        print(query)
    except Error as e:
        raise e
    
    
    
def prompt_out(headers, data):
    """
    Print header and data to prompt
    """
    
    # for i in range(len(data)):
    #     for j in range(len(data[i])):
    #         if not data[i][j]:
    #             data[i][j] = ""
                
    L = len(data)
    if headers:
        widths = [len(header) for header in headers]
    else:
        widths = [20]
        
    for row in data:
        widths = [max(width, len(str(cell))) for width, cell in zip(widths, row)]
    widths = [(width + 4) // 5 * 5 for width in widths]
    
    separator = "-" * (sum(widths) + 10)
    format_string = " | ".join(f"{{:<{width}}}" for width in widths)
    
    print(separator)
    if headers:
        print(format_string.format(*headers))
    for row in data:
        print(format_string.format(*row))
    print(separator)
    


def initialize_database():
    
    cursor.execute("DROP TABLE IF EXISTS ACTIVERENTALS;")
    cursor.execute("DROP TABLE IF EXISTS COMPLETEDRENTALS;")
    cursor.execute("DROP TABLE IF EXISTS USERS;")
    cursor.execute("DROP TABLE IF EXISTS DVDS;")
    
    cursor.execute(table_def["create_dvd_table"])
    cursor.execute(table_def["create_user_table"])
    cursor.execute(table_def["create_activerentals_table"])
    cursor.execute(table_def["create_completedrentals_table"])
    
    
    dvd = {}
    users = {}
    completed = {}
    
    # read data.csv file and fill the table
    df = pd.read_csv('data.csv', index_col=0)
    for index, row in df.iterrows():
        # Extract the attribute values
        d_id, d_title, d_name, u_id, u_name, u_age, rating = row
        if d_id not in dvd:
            dvd[d_id] = [d_id, d_title, d_name, 2, 0, 0]

        if u_id not in users:
            users[u_id] = [u_id, u_name, u_age, 3, 0, 0]
        
        completed[index] = [u_id, d_id, rating]
        
        dvd[d_id][4] += 1
        dvd[d_id][5] += rating
        users[u_id][4] += rating
        users[u_id][5] += 1
    
    dvd_data = list(dvd.values())
    users_data = list(users.values())
    completed_data = list(completed.values())
    
    cursor.executemany(
        "INSERT INTO DVDS VALUES (%s, %s, %s, %s, %s, %s)", dvd_data
    )
    
    cursor.executemany(
       "INSERT INTO USERS VALUES (%s, %s, %s, %s, %s, %s)", users_data
    )
    
    cursor.executemany(
       "INSERT INTO COMPLETEDRENTALS (u_id, d_id, rating) VALUES (%s, %s, %s)", completed_data
    )

    connection.commit()
    print('Database successfully initialized')
    
    return



def reset():
    # YOUR CODE GOES HERE
    pass



def print_DVDs():
    cursor.execute('''
        SELECT id, title, director, 
        CASE WHEN total_rentals = 0 THEN NULL ELSE total_ratings / total_rentals END,
        total_rentals, available_copies 
        FROM DVDS
        ORDER BY id;
    ''')
    DVDs = cursor.fetchall()

    # Print all movies
    prompt_out(['id', 'title', 'director', 'avg.rating', 'cumul_rent_cnt', 'quantity'], DVDs)
    return



def print_users():
    cursor.execute('SELECT id, name, age, total_ratings/total_rentals, total_rentals FROM USERS ORDER BY id;')
    users = cursor.fetchall()

    # Print all users
    prompt_out(['id', 'name', 'age', 'avg.rating', 'cumul_rent_cnt'], users)
    return



def insert_DVD():
    title = input('DVD title: ')
    director = input('DVD director: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def remove_DVD():
    DVD_id = input('DVD ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def insert_user():
    name = input('User name: ')
    age = input('User age: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def remove_user():
    user_id = input('User ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def checkout_DVD():
    DVD_id = input('DVD ID: ')
    user_id = input('User ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def return_and_rate_DVD():
    DVD_id = input('DVD ID: ')
    user_id = input('User ID: ')
    rating = input('Ratings (1~5): ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def print_borrowing_status_for_user():
    user_id = input('User ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def search():
    query = input('Query: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def recommend_popularity():
    # YOUR CODE GOES HERE
    user_id = input('User ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass

def recommend_user_based():
    user_id = input('User ID: ')
    # YOUR CODE GOES HERE
    # print msg
    pass


def main():
    while True:
        print('============================================================')
        print('1. initialize database')
        print('2. print all DVDs')
        print('3. print all users')
        print('4. insert a new DVD')
        print('5. remove a DVD')
        print('6. insert a new user')
        print('7. remove a user')
        print('8. check out a DVD')
        print('9. return and rate a DVD')
        print('10. print borrowing status of a user')
        print('11. search DVDs')
        print('12. search directors')
        print('13. recommend a DVD for a user using popularity-based method')
        print('14. recommend a DVD for a user using user-based collaborative filtering')
        print('15. exit')
        print('16. reset database')
        print('============================================================')
        menu = int(input('Select your action: '))

        if menu == 1:
            initialize_database()
        elif menu == 2:
            print_DVDs()
        elif menu == 3:
            print_users()
        elif menu == 4:
            insert_DVD()
        elif menu == 5:
            remove_DVD()
        elif menu == 6:
            insert_user()
        elif menu == 7:
            remove_user()
        elif menu == 8:
            checkout_DVD()
        elif menu == 9:
            return_and_rate_DVD()
        elif menu == 10:
            print_borrowing_status_for_user()
        elif menu == 11:
            search()
        elif menu == 12:
            search()
        elif menu == 13:
            recommend_popularity()
        elif menu == 14:
            recommend_user_based()
        elif menu == 15:
            print('Bye!')
            break
        elif menu == 16:
            reset()
        # debug
        elif menu == 99:
            while True:
                query = input()
                if query == "EXIT":
                    break
                cursor.execute(query)
                d = cursor.fetchall()
                print(d)
        else:
            print('Invalid action')


if __name__ == "__main__":
    main()
