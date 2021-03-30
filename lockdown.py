from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import config
 
# Exception Users we want to be sure each host has added. *Must* be an array of strings
users = ["root","nsx-user", "pdxroot"]

# Connect to vCenter
tls=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
tls.verify_mode=ssl.CERT_NONE

# config variables set in an external file (to save me from myself doing something stupid, like publishing credentials on github)
vcsa= SmartConnect(host=config.vcFqdn, user=config.vcUser, pwd=config.vcPwd,sslContext=tls)
content=vcsa.content

 
# Function that populates objects of type vimtype
def get_all_objs(content, vimtype):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
        obj.update({managed_object_ref: managed_object_ref.name})
    return obj
 
# Function that adds a username to the exception list for a host
def append_exception_user(host, username):
    try:
        assert host.configManager != None, "No handle to ConfigManager MOB"
        assert host.configManager.hostAccessManager != None, "No handle to AccessManager MOB"
        exceptions=host.configManager.hostAccessManager.QueryLockdownExceptions()
        
        try:
            if exceptions.index(username):
                # the user was found; no need to change this host
                return "no change"
        except ValueError as notFound:
            # user not in list, so append & update host
            exceptions.append(username)
            try:
                host.configManager.hostAccessManager.UpdateLockdownExceptions(exceptions)
            except vim.fault.UserNotFound as e:
                return "not a local system user"
            return "added"
    except AssertionError:
        return -1
   
# Function that removes a username from the exception list for a host
def remove_exception_user(host, username):
    try:
        assert host.configManager != None, "No handle to ConfigManager MOB"
        assert host.configManager.hostAccessManager != None, "No handle to AccessManager MOB"
        exceptions=host.configManager.hostAccessManager.QueryLockdownExceptions()
        
        try:
            if exceptions.index(username):
                # user not in list, so delete & update host
                exceptions.remove(username)
                host.configManager.hostAccessManager.UpdateLockdownExceptions(exceptions)
                return "removed"
        except ValueError as notFound:
            # the user was found; no need to change this host
            return "not present"
    except AssertionError:
        return -1

hosts=get_all_objs(content, [vim.HostSystem])
for host in hosts:
    print (host.name)
    for usr in users:
        print("  "+usr, end=", ")
        #print (append_exception_user(host,usr))
        print (remove_exception_user(host,usr))
