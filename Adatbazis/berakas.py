import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(vidId, videoFile, nev):
    try:
        sqliteConnection = sqlite3.connect('diplomamunka.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO videok
                                  (id,video,videoNeve) VALUES (?, ?, ?)"""

        video_binaris = convertToBinaryData(videoFile)
        # Convert data into tuple format
        data_tuple = (vidId, video_binaris, nev)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Video and Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

insertBLOB(1,r"C:\Users\dolfi\Documents\diplomamunkaVideok\_elobe.mp4","_elobe")
insertBLOB(2,r"C:\Users\dolfi\Documents\diplomamunkaVideok\video60s.mp4","video60s")
