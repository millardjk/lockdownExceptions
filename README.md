# lockdown.py
python script that allows admins to bulk-update the user exception list for host lockdowns

## Setup
Download and populate config.py with your vCenter details </br>
Update the "users" variable in lockdown.py with the usernames to be added or removed from the exceptions list.

## Adding exceptions
All the usernames being added to the exceptions list must already exist as local users on each host. This script doesn't have the facility for adding users "from scratch".</br>
Uncomment (look for the '#' character) the line that calls <i>append_exception_user()</i>

## Removing exceptions
Remove a matching username from the exceptions list; if the username isn't found in the host's exception list, nothing happens.</br>
Uncomment (look for the '#' character) the line that calls <i>remove_exception_user()</i>

## Important considerations
Because both "add" and "remove" are present in the same script--but the remove operation is after--leaving both script lines un-commented will have the net result 
of removing the list of users. You should always re-comment the operation you don't want to perform; ideally, you comment both operations when you're done for the moment.
