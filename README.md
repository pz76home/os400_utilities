The additional ABL Ansible commands are highly experimental at this point in time.

# What is this, you may ask?

One thing I used to love about the AS400 (or IBMi) was the job management.
I have brought the basic functionality of QBATCH or running background BATCH jobs to Linux.

QCMD will allow you to run interactive commands at a higher priority (Development Branch clone only, you will need all other commands from the same branch for this to work properly)

SBMJOB will allow you to submit a command, script or binary as a background job. 

WRKACTJOB will allow you view, list and end the "ACTIVE" running jobs.

WRKSBMJOB will allow you view, list and end ALL submitted jobs.

Also WRKSBMJOB is a good way to also clean up your output (SPOOL) files and clean the jobs from the database.

(Experimental Ansible Command) QCMDABL "PLAYBOOK('../ansible/test.yaml') INV('../ansible/hosts.ini') HOSTS('localserver') EXTVARS('ansible_connection=local') CHECK(N)"

(Experimental Ansible Command) SBMABLJOB with no parameters/arguments will provide some examples.

(Experimental C64sys) RUN bash scripts and python in the current directory, commands include DIR, LOAD, LIST, RUN and NEW. Also included games INVADERS and NIBBLES.

This was vibe coded with Google Gemini with alot of prompting and testing to get this to the now working functionality. 

# 1. Create the system-wide framework directories
sudo mkdir -p /var/lib/os400/splf

# 2. Assign ownership to a shared access group (e.g., 'os400' or 'users')
sudo chown -R root:users /var/lib/os400  (Ubuntu)

sudo groupadd os400 (RHEL)

sudo chown -R root:os400 /var/lib/os400  (RHEL)

sudo usermod -G os400 -a "insert_username_here" (RHEL to add non-root users you want to run these commands) 

# 3. Apply SGID and group read/write privileges
sudo chmod -R 775 /var/lib/os400 

sudo chmod g+s /var/lib/os400 /var/lib/os400/splf


# 4. Place python scripts in /usr/local/bin and chmod them to be executable

Clone the this git repo or manually copy and paste the python code of the commands.

Make it executable with chmod +x SBMJOB, and place it in a shared directory E.g. /usr/local/bin/ so all users can invoke it.

Make it executable with chmod +x WRKACTJOB, and place it in a shared directory like /usr/local/bin/ so all users can invoke it.

Make it executable with chmod +x WRKSBMJOB, and place it in a shared directory like /usr/local/bin/ so all users can invoke it.

YOU WILL NEED TO RUN A SBMJOB FIRST TO CREATE THE SQLITE DB TABLE THAT THE OTHER COMMANDS RELY ON

# 5. Example usage
SBMJOB 'CMD(sleep 15) JOB(QUICKJOB)'

SBMJOB 'CMD(ping -c 30 127.0.0.1) JOB(NETPING)'

SBMJOB 'CMD(sha256sum /dev/zero) JOB(CPULOOP)'


# Troubleshooting jobs submitted by SBMJOB 
python3 -c "import sqlite3; conn=sqlite3.connect('/var/lib/os400/qsys.db'); c=conn.cursor(); c.execute('SELECT * FROM active_jobs'); print(c.fetchall())"

# Permission issues with multiple concurrent users (Ignore, now addressed in commit 07c2556)
If you want to run this with multiple concurrent users, you will have to run the below commands again after the first SBMJOB. As the sqlite database is not created until the first SBMJOB.

sudo chmod -R 775 /var/lib/os400 

sudo chmod g+s /var/lib/os400 /var/lib/os400/splf

# Disclaimer 

This idea came to me and I did this when I was delirious with a bad cold/flu. So if you decide that you want to run this for anything mission critical or for serious production workloads. You do so at your own risk. 