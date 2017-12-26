#!/usr/bin/python

import shutil, os, sys, getopt, subprocess, shlex, re, fileSearchReplace


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
    commands=[]
    
    commands.append("sudo apt-get update")
    commands.append("sudo apt-get dist-upgrade -y")
    commands.append("sudo apt-get autoremove -y")
    commands.append("sudo apt-get install -y build-essential python-software-properties python g++ make fail2ban curl git htop ntp ntpdate zip unzip nano")
	
    commands.append("sudo dpkg-reconfigure tzdata")

    commands.append("sudo apt-get install apache2")
    commands.append("sudo ufw app list")
    commands.append("sudo ufw allow in \"Apache Full\"")
    commands.append("sudo ufw allow in \"OpenSSH\"")
    commands.append("sudo ufw enable")
    commands.append("sudo ufw status verbose")

    commands.append("sudo apache2ctl configtest")
    commands.append("sudo systemctl restart apache2")

    commands.append("sudo a2enmod rewrite")
    commands.append("sudo systemctl restart apache2")

    commands.append("sudo apt-get install mysql-server")
    commands.append("sudo mysql_secure_installation")

    commands.append("sudo apt-get install php libapache2-mod-php php-mcrypt php-mysql")

    commands.append("sudo systemctl restart apache2")
    commands.append("sudo systemctl status apache2")

    commands.append("sudo apt-get install php-cli")

    commands.append("curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer")

	commands.append("sudo apt-get update sudo apt-get install mcrypt php7.0-mcrypt sudo apt-get upgrade sudo apt-get install php-mbstring sudo apt-get install phpunit")

    commands.append("sudo apt-get install mysql-server")
    commands.append("sudo mysql_secure_installation")
 

    # Apache config file
    filename = "/etc/apache2/apache2.conf" 

    ServerName = command_line_query("Enter server_domain_or_IP", default="localhost")

    print "[+] Configuring server name..."

    text = "ServerName %s" % ServerName
    fileSearchReplace.SearchReplace(filename, "ServerName", text, True)
 

    # Customizing dir.conf file
    filename = "/etc/apache2/mods-enabled/dir.conf" 

    with open(filename, 'w') as outfile:

        print "[+] Customizing %s" % filename

        text = """\
<IfModule mod_dir.c>
    DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
</IfModule>
        """

        outfile.write(text) 


    # Customizing Apache default file
    filename = "/etc/apache2/sites-available/default" 

    with open(filename, 'w') as outfile:

        print "[+] Customizing %s" % filename

        text = """\
<Directory /var/www/>
    Options Indexes FollowSymLinks
    AllowOverride All
    Order allow,deny
    allow from all
</Directory>
        """

        outfile.write(text)    


    # Start processing commands
    processCommand(commands)

