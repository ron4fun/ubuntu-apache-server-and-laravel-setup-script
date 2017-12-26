#!/usr/bin/python

import shutil, os, sys, getopt, subprocess, shlex
from cmd import processCommand, command_line_query

# Validator functions
def validate_db_name(answer):
    if answer and answer != "root":
        return answer
    else:
        raise ValueError("You cannot use the value 'root'.")

def validate_db_password(answer):
    if len(answer) > 3:
        return answer
    else:
        raise ValueError("Password too samll.")




if __name__ == "__main__":
    db_name = command_line_query("Enter database name", validate=validate_db_name)
    user = command_line_query("Enter MySQL user name", validate=validate_db_name)
    password = command_line_query("Enter MySQL password", validate=validate_db_password)


	# Finalize
    commands=[]
    commands.append("echo \"CREATE DATABASE %s\" | mysql -u root -p" % db_name)

    query = "echo \"GRANT ALL ON " + db_name
    query += (".* TO " + user + "@'%' IDENTIFIED BY '" + password + "'\" | mysql -u root -p")
    
    commands.append(query)

    print "[+] Creating db and applying config..."
    processCommand(commands)


