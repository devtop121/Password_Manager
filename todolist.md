1: started working on initializing folders and databases Folder structure proposed... 
1.1 UPDATE: Decided to make a static place for a path to database which the user chooses its installation location.
            This allows the program to always find the correct path to database.
                                        pwmanager1.0 (main folder)
                                        /           |             \
                                      /             |               \
                                    /               |                 \
                               path.txt          main.py            database(sqlite)
                              Static location of path.txt which contains path to database: C:/pwpath/path.txt
                              
2: Make a interface for simpler navigation. I think using Tkinter should be good enough and it seems good. Update: started working on allowing users to edit and delete existing data. yet to work on displaying this in the "passwords" window. // DONE
3. Login interface with Tkinter. // DONE
4. Figure out a way to protect inserted data. Suggesting AES but it needs some thinking and implementation // DONE
5. Add something to about us tab and the main tab unless we decide on making the insert/delete tab the "main" tab. //DONE
6. Complete implementing NIST password guidelines 2024 // https://www.auditboard.com/blog/nist-password-guidelines/ // DONE
7. Register interface with Tkinter // DONE
8. Install interface with Tkinter // DONE
9. 


