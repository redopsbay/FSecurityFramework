# About the Framework #
    The FSecurityFramework is highly based on qt5 and pymetasploit3.
    It is use for penetration and testing. Most created malware will be undetectable in old AV's or new AV's. Because the shellcode instruction is encrypted and iterated.
    You can add script by meeting the requirements. by having a dynamic function name like 'commandlistener', 'setupParam' and also 'run' function names.
    Just study the built-in dynamic modules in able to understand how to interact with the command listener. I didn't follow any python standard syntax. Coz this is just my thesis and i have to do the work done in just 2 weeks. Below is the installation instruction.

## TESTED? ##
    This was only tested on Linux Mint 19. If you are having a trouble for installing metasploit-framework


# INSTALLATION INSTRUCTION #
    go to the FSecurity directory and find the install.sh. then open the terminal and type the following:

        user# ./install.sh

    After you install the necessary packages. You need to type the following into the terminal.

   
        user# mysql -u root -p 
        mysql > CREATE USER 'fsecurity'@'localhost' IDENTIFIED BY '@dm!n!$tr@t0R_F$3cur!tyFr@mw0rk';
        mysql > GRANT ALL ON *.* 'fsecurity'@'localhost';
   

    The database configuration can be found at FSecurityFramework/etc/fsecurity/DatabaseServer.json.
    
    {
        "host": "127.0.0.1",
        "user": "fsecurity",  /* you can change the user if there is no registered user in the database. like "root". */
        "password": "QGRtIW4hJHRyQHQwUl9GJDNjdXIhdHlGckBtdzByaw==", /* change this value with your encrypted mysql database password. The unencrypted password will be @dm!n!$tr@t0R_F$3cur!tyFr@mw0rk */
        "database": "FSecurityFramework",
        "port": 3306,
        "pool_size": 10
    }


## Starting Up ##
    To start the FSecurityFramework just type the following commands.
        root:/home/user/Desktop/FSecurity# ./launch_msf_daemon.sh
        root:/home/user/Desktop/FSecurity# cd FSecurityFramework
        root:/home/user/Desktop/FSecurity/FSecurityFramework# python3 main.py -style plastique
