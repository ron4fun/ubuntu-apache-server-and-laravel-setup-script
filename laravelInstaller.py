#!/usr/bin/python

import shutil, os, sys, getopt, subprocess, shlex, re


def command_line_query(question, default=None, validate=None, style="compact"):
    """Ask the user a question using raw_input() and looking something
    like this ("compact" style, the default, `_` is the cursor):

        QUESTION [DEFAULT]: _
        ...validation...

    or this ("verbose" style):

        QUESTION
        Hit <Enter> to use the default, DEFAULT.
        > _
        ...validation...

    @param question {str} The question to ask.
    @param default {str} Optional. The default value if non is given.
    @param validate {str|function} is either a string naming a stock
        validator

            not-empty       Ensure the user's answer is not empty.
            yes-or-no       Ensure the user's answer is 'yes' or 'no'.
                            ('y', 'n' and any capitalization are
                            also accepted)
            int             Answer is an integer.

        or a callback function with this signature:
            validate(answer) -> normalized-answer
        It should raise `ValueError` to indicate an invalid answer.
            
        By default no validation is done.
    @param style {str} is a name for the interaction style, either "compact"
        (the default) or "verbose". See the examples above.
    @returns {str} The normalized answer.
    """
    if isinstance(validate, (str, unicode)):
        if validate == "not-empty":
            def validate_not_empty(answer):
                if not answer:
                    raise ValueError("You must enter some non-empty value.")
                return answer
            validate = validate_not_empty
        elif validate == "yes-or-no":
            def validate_yes_or_no(answer):
                normalized = {"yes":"yes", "y":"yes", "ye":"yes",
                    "no":"no", "n":"no"}
                try:
                    return normalized[answer.lower()]
                except KeyError:
                    raise ValueError("Please enter 'yes' or 'no'.")
            validate = validate_yes_or_no
        elif validate == "int":
            def validate_int(answer):
                try:
                    int(answer)
                except ValueError:
                    raise ValueError("Please enter an integer.")
                else:
                    return answer
            validate = validate_int
        else:
            raise ValueError("unknown stock validator: '%s'" % validate)
    
    def indented(text, indent=' '*4):
        lines = text.splitlines(1)
        return indent + indent.join(lines)

    if style == "compact":
        prompt = question
        if default is not None:
            prompt += " [%s]" % (default or "<empty>")
        prompt += ": "
    elif style == "verbose":
        sys.stdout.write(question + '\n')
        if default:
            sys.stdout.write("Hit <Enter> to use the default, %r.\n" % default)
        elif default is not None:
            default_str = default and repr(default) or '<empty>'
            sys.stdout.write("Hit <Enter> to leave blank.\n")
        prompt = "> "
    else:
        raise ValueError("unknown query style: %r" % style)
    
    while True:
        if True:
            answer = raw_input(prompt)
        else:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            answer = sys.stdout.readline()
        if not answer and default:
            answer = default
        if validate is not None:
            orig_answer = answer
            try:
                norm_answer = validate(answer)
            except ValueError, ex:
                sys.stdout.write(str(ex) + '\n')
                continue
        else:
            norm_answer = answer
        break
    return norm_answer
   
# Validator
def validate_dir(answer):
    if os.path.isdir(answer):
    	return answer
    else:
    	raise ValueError("Please enter a correct directory.")

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url(answer):
    if regex.match(answer):
    	return answer
    else:
    	raise ValueError("Please enter a valid url.")

# Handle commands
def subProcess(command):
	args = shlex.split(command)
	
	if args[0] == "cd":
		os.chdir(args[1])
		return
	
	p = subprocess.Popen(args, stdout=subprocess.PIPE)
	print "[+] %s" % p.communicate()[0]

def processCommand(command):
	if isinstance(command, list):
		for cmd in command:
			subProcess(cmd)
			
	else:
		subProcess(command)

if __name__ == "__main__":
	# Get general path
	path_to_save_repo = command_line_query("Enter path location", validate=validate_dir, default="/var/www/")


	# Get git repo url
	url_git_repo = command_line_query("Enter url for the repo", validate=validate_url)
	repo_name = url_git_repo.rstrip('/').split('/')[-1].split('.')[0]
	app_path = os.path.join(path_to_save_repo, repo_name)
	

	# Change path to path_to_save_repo
	command = "cd %s" % path_to_save_repo
	processCommand(command)
	

	# Run git clone command
	command = "git clone " + url_git_repo
	print "[+] Cloning repo at %s to %s" % (url_git_repo, app_path)
	processCommand(command)
	

	# Update packages via composer
	command = "composer --working-dir=" + app_path + " update"
	print "[+] Updating repo package manager"
	processCommand(command)


	# Set Privilages to folders
	commands=[]
	
	commands.append("sudo chgrp -R www-data " + app_path)
	commands.append("sudo chmod -R 777 " + os.path.join(app_path, "storage"))
	commands.append("sudo chmod -R 777 " + os.path.join(app_path, "bootstrap/cache"))
	
	print "[+] Setting required privilages"
	processCommand(commands)


	# Set app config
	filename = "/etc/apache2/sites-available/%s.conf" % repo_name 

	with open(filename, 'w') as outfile:
		ServerName = command_line_query("Enter ServerName", default="localhost")
		ServerAdmin = command_line_query("Enter ServerAdmin", default="webmaster@localhost")
		ServerAlias = command_line_query("Enter ServerAlias", default="localhost")

		print "[+] Creating %s" % filename

		text = """\
		<VirtualHost *:80>
			ServerAlias %s
		    ServerName %s

		    ServerAdmin %s
		    DocumentRoot %s

		    <Directory %s>
		        Options Indexes FollowSymLinks MultiViews
		        AllowOverride all
		        Order allow,deny
		        allow from all
		        Require all granted
		    </Directory>

		    ErrorLog ${APACHE_LOG_DIR}/error.log
		    CustomLog ${APACHE_LOG_DIR}/access.log combined
		</VirtualHost>
		""" % (ServerAlias, ServerName, ServerAdmin, os.path.join(app_path, "public"), app_path)

		outfile.write(text)    

	

	# Finalize
	commands=[]
	apache2_path = "/etc/apache2/sites-available/"
	commands.append("cd %s" % apache2_path)
	commands.append("sudo a2dissite 000-default.conf")
	commands.append("sudo a2ensite %s.conf" % repo_name)
	commands.append("sudo a2enmod rewrite")
	commands.append("sudo service apache2 restart")

	print "[+] Finalizing..."
	processCommand(commands)
   
	# Finishing checks
	if not os.path.exists(os.path.join(app_path, ".env")):
		if os.path.exists(os.path.join(app_path, ".env.example")) :
			original_file = os.path.join(app_path, ".env.example")
			new_file_name = os.path.join(app_path, ".env")
			command = "mv %s %s" % (original_file, new_file_name)
			print "[+] Renaming repo '.env.example' to '.env'"
			processCommand(command)








