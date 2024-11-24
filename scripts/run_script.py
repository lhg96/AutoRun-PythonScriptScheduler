import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_script(script_path):
    try:
        # 현재 작업 디렉토리의 상위 디렉토리로 이동
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspace_dir = os.path.dirname(current_dir)
        
        # 실제 스크립트 경로 구성
        absolute_script_path = os.path.join(workspace_dir, script_path.lstrip('/'))
        
        logger.info(f"Executing script: {absolute_script_path}")
        
        # 스크립트가 있는 디렉토리로 이동
        script_dir = os.path.dirname(absolute_script_path)
        
        # sh 파일 실행
        result = subprocess.run(['bash', absolute_script_path], 
                              capture_output=True, 
                              text=True, 
                              check=True,
                              cwd=script_dir)
                              
        logger.info(f"Script output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Script execution failed: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error running script: {str(e)}")
        return False
