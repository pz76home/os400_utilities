
# 1. Create the system-wide framework directories
sudo mkdir -p /var/lib/os400/splf

# 2. Assign ownership to a shared access group (e.g., 'os400' or 'users')
sudo chown -R root:users /var/lib/os400

# 3. Apply SGID and group read/write privileges
sudo chmod -R 775 /var/lib/os400
sudo chmod g+s /var/lib/os400 /var/lib/os400/splf


# 4. Place python scripts in /usr/local/bin and chmod them to be executable
Make it executable with chmod +x SBMJOB, and place it in a shared directory like /usr/local/bin/SBMJOB so all users can invoke it.

Make it executable with chmod +x WRKACTJOB, and place it in a shared directory like /usr/local/bin/WRKACTJOB so all users can invoke it.


# 4. Example usage
SBMJOB 'CMD(sleep 15) JOB(QUICKJOB)'


# 4. Troubleshooting jobs submitted by SBMJOB 
python3 -c "import sqlite3; conn=sqlite3.connect('/var/lib/os400/qsys.db'); c=conn.cursor(); c.execute('SELECT * FROM active_jobs'); print(c.fetchall())"