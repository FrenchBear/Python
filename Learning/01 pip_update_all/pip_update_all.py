# https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip?page=1&tab=votes#tab-top

# Works on Windows. Should be good for others too. ($ is whatever directory you're in, in command prompt. eg.
# C:/Users/Username>)
# Do:

# $ pip freeze > requirements.txt

# Open the text file, replace the == with >=
# Then do:

# $ pip install -r requirements.txt --upgrade

# If you have a problem with a certain package stalling the upgrade (numpy sometimes), just go to the directory ($),
# comment out the name (add a # before it) and run the upgrade again. You can later uncomment that section back. This is
# also great for copying python global environments.



# Extra
# pip list --outdated
# pip check
