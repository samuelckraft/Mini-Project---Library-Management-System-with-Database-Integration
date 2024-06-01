#Task 1
import mysql.connector
from mysql.connector import Error

def connect_database():
    db_name = 'library'

    user = 'root' 

    password = '654U7jsv'

    host = 'localhost'

    try:
        conn = mysql.connector.connect(database = db_name, user = user, password = password, host = host)
        

        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None


#Book Operations

def add_book(title, author_id, genre_id, isbn, pub_date):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            new_book = (title, author_id, genre_id, isbn, pub_date, True)

            query = 'insert into books (title, author_id, genre_id, isbn, publication_date, availability) values (%s, %s, %s, %s, %s, %s)'
            cursor.execute(query, new_book)

            conn.commit()
            print(f"Book '{title}' added to library")



        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()


def borrow_book(user_id, book_id, borrow_date, return_date):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            availability_check = 'select * from books where id = %s and availability = 1'

            cursor.execute(availability_check, (book_id, ))
            test = cursor.fetchall()
            if test:
                borrow = (user_id, book_id, borrow_date, return_date)

                query = 'insert into borrowed_books (user_id, book_id, borrow_date, return_date) values (%s, %s, %s, %s)'
                
                cursor.execute(query, borrow)

                availability = 'update books set availability = 0 where id = %s'

                cursor.execute(availability, (book_id, ))

                conn.commit()
                print("Book borrowed")

            else:
                print('Book not available')
            

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def return_book(book_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check = 'select * from borrowed_books where book_id = %s'

            cursor.execute(check, (book_id, ))
            test = cursor.fetchall()

            if test:
                query = 'delete from borrowed_books where book_id = %s'
                
                cursor.execute(query, (book_id, ))

                availability = 'update books set availability = 1 where id = %s'

                cursor.execute(availability, (book_id, ))

                conn.commit()
                print("Book returned")
            else:
                print('Book either does not exist or was not checked out')

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def search_book(title):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from books where title = %s'

            cursor.execute(query, (title, ))

            exists = cursor.fetchall()

            if exists:
                for row in exists:
                    book_id, title, author, genre, isbn, pub_date, availability = row

                    author_query = 'select name from authors where id = %s'
                    cursor.execute(author_query, (author, ))
                    author_pull = cursor.fetchall()
                    for author in author_pull:
                        author_name, *blank = author


                    genre_query = 'select name from genres where id = %s'
                    cursor.execute(genre_query, (genre, ))
                    genre_pull = cursor.fetchall()
                    for genre in genre_pull:
                        genre_name, *blank = genre

                    if availability == 1:
                        availability = "Available"
                    elif availability == 2:
                        availability = "Not Available"
                    
                    print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author_name}\nGenre: {genre_name}\nISBN: {isbn}\nPublication Date: {pub_date}\nAvailability: {availability}")
            else:
                print(f"'{title}' not found please try again")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def display_books():
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from books'

            cursor.execute(query)

            books = cursor.fetchall()

            for book in books:
                book_id, title, author, genre, isbn, pub_date, availability = book

                author_query = 'select name from authors where id = %s'
                cursor.execute(author_query, (author, ))
                author_pull = cursor.fetchall()
                for author in author_pull:
                    author_name, *blank = author


                genre_query = 'select name from genres where id = %s'
                cursor.execute(genre_query, (genre, ))
                genre_pull = cursor.fetchall()
                for genre in genre_pull:
                    genre_name, *blank = genre

                if availability == 1:
                    availability = "Available"
                elif availability == 2:
                    availability = "Not Available"
                
                print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author_name}\nGenre: {genre_name}\nISBN: {isbn}\nPublication Date: {pub_date}\nAvailability: {availability}")


        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()


#User Operations

def add_user(name, lib_id):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'insert into users (name, library_id) values (%s, %s)'

            new_user = (name, lib_id)

            cursor.execute(query, new_user)

            conn.commit()

            print(f"User '{name}' added to system")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def view_user(name):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from users where name = %s'

            cursor.execute(query, (name, ))
            
            exists = cursor.fetchall()

            if exists:
                for row in exists:
                    user_id, name, lib_id = row
                    print(f"\nUser ID: {user_id}\nName: {name}\nLibrary ID: {lib_id}")
            else:
                print(f"\nUser '{name}' not found")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def display_users():
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from users'

            cursor.execute(query)

            for row in cursor.fetchall():
                user_id, name, lib_id = row
                print(f"\nUser ID: {user_id}\nName: {name}\nLibrary ID: {lib_id}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()


#Author Operations

def add_author(name, bio):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'insert into authors (name, biography) values (%s, %s)'

            new_author = (name, bio)

            cursor.execute(query, new_author)

            conn.commit()

            print(f"Author '{name}' added to system")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def view_author(name):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from authors where name = %s'

            cursor.execute(query, (name, ))
            
            exists = cursor.fetchall()

            if exists:
                for row in exists:
                    author_id, name, bio = row
                    if bio:
                        bio = bio
                    else:
                        bio = 'N/A'
                    print(f"\nAuthor ID: {author_id}\nName: {name}\nBiography: {bio}")
            else:
                print(f"\nAuthor '{name}' not found")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def display_authors():
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from authors'

            cursor.execute(query)

            for row in cursor.fetchall():
                author_id, name, bio = row
                if bio:
                    bio = bio
                else:
                    bio = 'N/A'
                print(f"\nAuthor ID: {author_id}\nName: {name}\nBiography: {bio}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

#Genre Operations

def add_genre(name, description, category):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'insert into genres (name, description, category) values (%s, %s, %s)'

            new_genre = (name, description, category)

            cursor.execute(query, new_genre)

            conn.commit()

            print(f"Genre '{name}' added to system")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def view_genre(name):
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from genres where name = %s'

            cursor.execute(query, (name, ))
            
            exists = cursor.fetchall()

            if exists:
                for row in exists:
                    genre_id, name, description, category = row
                    if description:
                        description = description
                    else:
                        description = 'N/A'

                    print(f"\nGenre ID: {genre_id}\nName: {name}\nDescription: {description}\nCategory: {category}")
            else:
                print(f"\nGenre '{name}' not found")

            
        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

def display_genres():
    conn = connect_database()
    if conn is not None:
        try:
            cursor = conn.cursor()

            query = 'select * from genres'

            cursor.execute(query)

            for row in cursor.fetchall():
                genre_id, name, description, category = row
                if description:
                    description = description
                else:
                    description = 'N/A'

                print(f"\nGenre ID: {genre_id}\nName: {name}\nDescription: {description}\nCategory: {category}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

while True:
    print('\nLibrary Management System')
    print('1. Book Operations')
    print('2. User Operations')
    print('3. Author Operations')
    print('4. Genre Operations')
    print('5. Exit')
    choice = input('\nSelect one of the above choices: ')

    if choice == '1':
        print('Book Operations')
        print('1. Add a new book')
        print('2. Borrow a book')
        print('3. Return a book')
        print('4. Search for a book')
        print('5. Display all books')
        book_choice = input('\nSelect one of the above choices: ')

        if book_choice == '1':
            title = input("Enter title of book to add: ")
            author_id = input("Enter ID of the author: ")
            genre_id = input("Enter ID of the genre: ")
            isbn = input("Enter the ISBN: ")
            pub_date = input('Enter publication date (YYYY-MM-DD): ')
            add_book(title, author_id, genre_id, isbn, pub_date)

        elif book_choice == '2':
            user_id = input("Enter ID of the borrowing user: ")
            book_id = input("Enter ID of the book to checkout: ")
            borrow_date = input("Enter borrowing date (YYYY-MM-DD): ")
            return_date = input("Enter return date (YYYY-MM-DD): ")
            borrow_book(user_id, book_id, borrow_date, return_date)

        elif book_choice == '3':
            book_id = input("Enter ID of the book to return: ")
            return_book(book_id)

        elif book_choice == '4':
            title = input("Enter title of book to search: ")
            search_book(title)

        elif book_choice == '5':
            display_books()
        else:
            print('Invalid option please try again')


    elif choice == '2':
        print('User Operations')
        print('1. Add a new user')
        print('2. View user details')
        print('3. Display all users')
        user_choice = input('\nSelect one of the above choices: ')
        if user_choice == '1':
            name = input("Enter name of user to add: ")
            lib_id = input("Enter library ID for new user: ")
            add_user(name, lib_id)

        elif user_choice == '2':
            name = input("Enter full name of user: ")
            view_user(name)

        elif user_choice == '3':
            display_users()

        else:
            print('Invalid option please try again')

        
    elif choice == '3':
        print('Author Operations')
        print('1. Add a new author')
        print('2. View author details')
        print('3. Display all authors')
        author_choice = input('\nSelect one of the above choices: ')
        if author_choice == '1':
            name = input("Enter name of author to add: ")
            bio = input("Enter a short biography (optional): ")
            add_author(name, bio)

        elif author_choice == '2':
            name = input("Enter name of author to view: ")
            view_author(name)

        elif author_choice == '3':
            display_authors()

        else:
            print('Invalid option please try again')


    elif choice == '4':
        print('Genre Operations')
        print('1. Add a new genre')
        print('2. View genre details')
        print('3. Display all genres')
        genre_choice = input('\nSelect one of the above choices: ')

        if genre_choice == '1':
            name = input("Enter name of genre to add: ")
            description = input("Enter a short description (optional): ")
            category = input("Enter category (Fiction/Non-Fiction): ")
            add_genre(name, description, category)

        elif genre_choice == '2':
            name = input("Enter name of author to view: ")
            view_genre(name)

        elif genre_choice == '3':
            display_genres()
        else:
            print('Invalid option please try again')

    elif choice == '5':
        print('\nClosing Library Management System')
        break
    else:
        print('Invalid option please try again')