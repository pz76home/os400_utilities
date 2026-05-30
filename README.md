# What is this, you may ask?

One thing I used to love about the AS400 (or IBMi) was the job management.
I have brought the basic functionality of QBATCH or running background BATCH jobs to Linux.

SBMJOB will allow you to submit a command, script or binary as a background job. 

WRKACTJOB will allow you view, list and end the "ACTIVE" running jobs.

WRKSBMJOB will allow you view, list and end the ALL submitted jobs.

Also WRKSBMJOB is a good way to also clean up your output (SPOOL) files and clean the jobs from the database.

This was vibe coded with Google Gemini with alot of prompting to get this to the now working functionality. 

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

# 4. Example usage
SBMJOB 'CMD(sleep 15) JOB(QUICKJOB)'

SBMJOB 'CMD(ping -c 30 127.0.0.1) JOB(NETPING)'

SBMJOB 'CMD(sha256sum /dev/zero) JOB(CPULOOP)'


# 4. Troubleshooting jobs submitted by SBMJOB 
python3 -c "import sqlite3; conn=sqlite3.connect('/var/lib/os400/qsys.db'); c=conn.cursor(); c.execute('SELECT * FROM active_jobs'); print(c.fetchall())"

# Things I would like to do

Create QCMD to have jobs run interactively, displaying as QINTER jobs in WRKACTJOB. (These would run at the OS default nice values)

Have SBMJOB run the BATCH jobs at a lower nice value, though able to change the priority to renice the jobs

The main challenge (I had with Ubuntu anyway) was the system limits on letting me renice my jobs. I will play with this when I have the time.

# Disclaimer 

This idea came to me and I did this when I was delirious with a bad cold/flu. So if you decide that you want to run this for anything mission critical or for serious production workloads. You do so at your own risk. 