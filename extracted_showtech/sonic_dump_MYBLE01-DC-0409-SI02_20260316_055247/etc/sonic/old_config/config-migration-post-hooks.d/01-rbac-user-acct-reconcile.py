#!/usr/bin/env python

import dbus
import syslog
import time

HAMD_DBUS_OPATH = "/org/SONiC/HostAccountManagement"
HAMD_DBUS_SERVICE = "org.SONiC.HostAccountManagement"
MAX_RETRY_COUNT = 5
WAIT_DELAY = 1

#Overview: This script is to reconcile the user account from etc/passwd to stateDB while image migration.
# If the user accnt reconcile failed, retry after 1 second. maximum number of retry is 5. 

#Description:
#The script - installer-migration-hooks/01-local-users-pre - takes a backup of user accounts before image upgrade
#Post upgrade, the script - migration-hooks-post/01-local-users-post.j2 - restores the user accounts directly into the files like /etc/passwd, /etc/group and etc.
#The user account information (username to role mapping) must be stored in the State DB for the proper functioning of RBAC feature.
#The user accounts restored by the post upgrade script must be stored in the State DB.
#This script stores such user account info in the state DB.

def runmain():
    ntries = MAX_RETRY_COUNT
    waitdelay = WAIT_DELAY
    while ntries >= 1:
        try:
            bus = dbus.SystemBus()
            ham_obj = bus.get_object(HAMD_DBUS_SERVICE, HAMD_DBUS_OPATH)
            ham_acc_int = dbus.Interface(ham_obj, dbus_interface="ham.accounts")
            ret_val = ham_acc_int.userAcctReconcile()
            #if the return value from hamd is false, retry the user reconcile again. 
            if ret_val[0] == 0:
                msg = "User Accnt Reconcile failed. Remaining retry count {}.  Retrying in {} second...".format(ntries, waitdelay)
                syslog.syslog(syslog.LOG_ERR, msg)
            else:
                return

        except Exception as e:
            msg = "({}), Remaining retry count {}.  Retrying in {} second...".format(str(e),ntries, waitdelay)
            syslog.syslog(syslog.LOG_ERR, msg)
        #If the user accnt reconcile failed, retry after 1 second.
        time.sleep(waitdelay)
        ntries -= 1

if __name__ == "__main__":
    runmain()

