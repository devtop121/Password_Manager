1: started working on initializing folders and databases Folder structure proposed... 
1.1 UPDATE: Decided to make a static place for a path to database which the user chooses its installation location.
            This allows the program to always find the correct path to database.
                                        pwmanager1.0 (main folder)
                                        /           |             \
                                      /             |               \
                                    /               |                 \
                               path.txt          main.py            database(sqlite)
                              Static location of path.txt which contains path to database: C:/pwpath/path.txt
                              
2: Make a interface for simpler navigation. I think using Tkinter should be good enough and it seems good.
3: Think about securing information and movement of data. Update: Managed to make secure password storing in database and login checks this.
4. Login interface with Tkinter.
