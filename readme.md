# Python Script Scheduler

A web-based scheduler application for automated Python script execution.

## Key Features

- 💻 Script scheduling through web interface
- ⏰ Flexible execution intervals (seconds/minutes/hours)
- 📝 Real-time log monitoring
- 🔄 Running job management (view/modify/delete)
- 🗄️ SQLite-based job storage

## Technology Stack

- **Backend**: FastAPI
- **Scheduler**: APScheduler
- **Database**: SQLite
- **Frontend**: Static HTML/JavaScript
- **Documentation**: OpenAPI (Swagger)

## Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd autorun
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application
```bash
./run_scheduler.sh
# or
python app.py
```

2. Access via web browser
```
http://localhost:8000
```

## macOS Auto-start Configuration

### LaunchAgent Setup

1. Create LaunchAgents directory
```bash
mkdir -p ~/Library/LaunchAgents
```

2. Create plist file
```bash
nano ~/Library/LaunchAgents/com.scheduler.plist
```

3. Write plist file content
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.scheduler</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/[username]/workspace/autorun/run_scheduler.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/Users/[username]/workspace/autorun/logs/error.log</string>
    <key>StandardOutPath</key>
    <string>/Users/[username]/workspace/autorun/logs/output.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/[username]/workspace/autorun</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
```

4. Setup execution script
```bash
# Create script
nano ~/workspace/autorun/run_scheduler.sh

# Script content
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
cd /Users/[username]/workspace/autorun
source venv/bin/activate
python3 app.py
```

5. Set permissions
```bash
chmod +x ~/workspace/autorun/run_scheduler.sh
sudo chown [username]:staff ~/Library/LaunchAgents/com.scheduler.plist
sudo chmod 644 ~/Library/LaunchAgents/com.scheduler.plist
```

### Service Management

Start service:
```bash
launchctl load ~/Library/LaunchAgents/com.scheduler.plist
launchctl start com.scheduler
```

Stop service:
```bash
launchctl stop com.scheduler
launchctl unload ~/Library/LaunchAgents/com.scheduler.plist
```

Check service status:
```bash
launchctl list | grep scheduler
```

### Log Monitoring

```bash
# Check real-time output logs
tail -f ~/workspace/autorun/logs/output.log

# Check real-time error logs
tail -f ~/workspace/autorun/logs/error.log
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/jobs` | GET | Retrieve all scheduled jobs |
| `/api/jobs` | POST | Create a new job |
| `/api/jobs/{job_id}` | GET | Get specific job details |
| `/api/jobs/{job_id}` | PUT | Update job settings |
| `/api/jobs/{job_id}` | DELETE | Delete a job |
| `/api/logs` | GET | Retrieve system logs |

## Project Structure

```
autorun/
├── app.py              # FastAPI application main
├── requirements.txt    # Project dependencies
├── run_scheduler.sh    # Execution script
├── scripts/           
│   ├── init.py
│   └── run_script.py   # Script execution handler
├── static/
│   └── index.html      # Web interface
└── logs/               # Log directory
```

## Environment Variables

You can create a `.env` file to set the following environment variables:

- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)
- `DATABASE_URL`: Database URL (default: sqlite:///jobs.sqlite)


## Logging
- Log file: `logs/output.log`
- Error log file: `logs/error.log`
## Start Service
- launchctl load ~/Library/LaunchAgents/com.scheduler.plist
## Stop Service
- launchctl unload ~/Library/LaunchAgents/com.scheduler.plist
## Check Service Status
- launchctl list | grep scheduler
## Check Logs
- tail -f ~/workspace/autorun/logs/output.log
- tail -f ~/workspace/autorun/logs/error.log

---

## Git Usage Guide

### Initial Setup
Set up user information when using Git for the first time:
```bash
# Set Git user email
git config --global user.email "hyun.lim@okkorea.net"

# Set Git user name
git config --global user.name "lhg96"
```
---
### Initialize Git Repository
Initialize Git repository when starting a new project:
```bash
# 1. Initialize Git repository
git init

# 2. Create README.md file (if needed)
echo "# autorun" >> README.md

# 3. Add files to staging area
git add .                # Add all files
git add README.md       # Add specific file only

# 4. Commit changes
git commit -m "first commit"

# 5. Set default branch to main
git branch -M main

# 6. Connect to GitHub remote repository
git remote add origin https://github.com/lhg96/autorun.git

# 7. Push to GitHub
git push -u origin main
```
---
### Update Files in Git Repository
Update files in Git repository whenever the project is updated:
```bash
# 1. Check status of changed files
git status

# 2. Stage all changed files
git add .

# 3. Commit changes
git commit -m "Descriptive message about changes"

# 4. Push to GitHub
git push
```
---
### Download Files from Git Repository
Use when downloading files from GitHub:
```bash
# 1. Clone project from GitHub
git clone https://github.com/lhg96/autorun.git
# 2. Pull files from remote repository
git pull origin main
```
