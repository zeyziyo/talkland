import os
import zipfile
import datetime
import shutil

def backup_project():
    # 프로젝트 루트 디렉토리 (현재 스크립트가 있는 위치)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 백업 폴더 생성
    backup_dir = os.path.join(project_root, "backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 백업 파일명 생성 (타임스탬프 포함)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"backup_{timestamp}.zip"
    zip_filepath = os.path.join(backup_dir, zip_filename)
    
    # 제외할 디렉토리 및 파일 목록
    excluded_dirs = {
        '.git', '.venv', 'venv', '__pycache__', '.idea', '.vscode', 
        'backups', 'build', 'dist', '.flet', 'flet'
    }
    excluded_extensions = {'.pyc', '.pyd', '.pyo'}
    
    print(f"Backing up project to: {zip_filepath}")
    
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_root):
                # 제외할 디렉토리 필터링
                dirs[:] = [d for d in dirs if d not in excluded_dirs]
                
                for file in files:
                    # 제외할 확장자 필터링
                    _, ext = os.path.splitext(file)
                    if ext in excluded_extensions:
                        continue
                        
                    # 백업 파일 자체는 제외
                    if file == zip_filename:
                        continue
                        
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_root)
                    
                    zipf.write(file_path, arcname)
                    
        print("Backup completed successfully!")
        
    except Exception as e:
        print(f"Backup failed: {e}")
        # 실패 시 불완전한 파일 삭제
        if os.path.exists(zip_filepath):
            os.remove(zip_filepath)

if __name__ == "__main__":
    backup_project()
