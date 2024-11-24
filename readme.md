# Python Script Scheduler

자동화된 Python 스크립트 실행을 위한 웹 기반 스케줄러 애플리케이션입니다.

## 주요 기능

- 💻 웹 인터페이스를 통한 스크립트 스케줄링
- ⏰ 유연한 실행 간격 설정 (초/분/시간 단위)
- 📝 실시간 로그 모니터링
- 🔄 실행 중인 작업 관리 (조회/수정/삭제)
- 🗄️ SQLite 기반 작업 저장소

## 기술 스택

- **Backend**: FastAPI
- **Scheduler**: APScheduler
- **Database**: SQLite
- **Frontend**: Static HTML/JavaScript
- **Documentation**: OpenAPI (Swagger)

## 요구사항

- Python 3.8+
- pip (Python 패키지 관리자)
- 가상환경 (권장)

## 설치 방법

1. 저장소 클론
```bash
git clone [repository-url]
cd autorun
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

1. 애플리케이션 실행
```bash
./run_scheduler.sh
# or
python app.py
```

2. 웹 브라우저에서 접속
```
http://localhost:8000
```

## macOS 자동실행 설정

### LaunchAgent 설정

1. LaunchAgents 디렉토리 생성
```bash
mkdir -p ~/Library/LaunchAgents
```

2. plist 파일 생성
```bash
nano ~/Library/LaunchAgents/com.scheduler.plist
```

3. plist 파일 내용 작성
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

4. 실행 스크립트 설정
```bash
# 스크립트 생성
nano ~/workspace/autorun/run_scheduler.sh

# 스크립트 내용
#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
cd /Users/[username]/workspace/autorun
source venv/bin/activate
python3 app.py
```

5. 권한 설정
```bash
chmod +x ~/workspace/autorun/run_scheduler.sh
sudo chown [username]:staff ~/Library/LaunchAgents/com.scheduler.plist
sudo chmod 644 ~/Library/LaunchAgents/com.scheduler.plist
```

### 서비스 관리

서비스 시작:
```bash
launchctl load ~/Library/LaunchAgents/com.scheduler.plist
launchctl start com.scheduler
```

서비스 중지:
```bash
launchctl stop com.scheduler
launchctl unload ~/Library/LaunchAgents/com.scheduler.plist
```

서비스 상태 확인:
```bash
launchctl list | grep scheduler
```

### 로그 확인

```bash
# 실시간 출력 로그 확인
tail -f ~/workspace/autorun/logs/output.log

# 실시간 에러 로그 확인
tail -f ~/workspace/autorun/logs/error.log
```

## API 엔드포인트

| 엔드포인트 | 메소드 | 설명 |
|------------|--------|------|
| `/api/jobs` | GET | 모든 스케줄된 작업 조회 |
| `/api/jobs` | POST | 새로운 작업 생성 |
| `/api/jobs/{job_id}` | GET | 특정 작업 상세 정보 조회 |
| `/api/jobs/{job_id}` | PUT | 작업 설정 수정 |
| `/api/jobs/{job_id}` | DELETE | 작업 삭제 |
| `/api/logs` | GET | 시스템 로그 조회 |

## 프로젝트 구조

```
autorun/
├── app.py              # FastAPI 애플리케이션 메인
├── requirements.txt    # 프로젝트 의존성
├── run_scheduler.sh    # 실행 스크립트
├── scripts/           
│   ├── init.py
│   └── run_script.py   # 스크립트 실행 핸들러
├── static/
│   └── index.html      # 웹 인터페이스
└── logs/               # 로그 디렉토리
```

## 환경 변수

`.env` 파일을 생성하여 다음 환경 변수를 설정할 수 있습니다:

- `PORT`: 서버 포트 (기본값: 8000)
- `LOG_LEVEL`: 로깅 레벨 (기본값: INFO)
- `DATABASE_URL`: 데이터베이스 URL (기본값: sqlite:///jobs.sqlite)


## 로깅
- 로그 파일: `logs/output.log`
- 에러 로그 파일: `logs/error.log`
## 서비스 시작
- launchctl load ~/Library/LaunchAgents/com.scheduler.plist
## 서비스 중지
- launchctl unload ~/Library/LaunchAgents/com.scheduler.plist
## 서비스 상태 확인
- launchctl list | grep scheduler
## 로그 확인
- tail -f ~/workspace/autorun/logs/output.log
- tail -f ~/workspace/autorun/logs/error.log
