import requests
import json
import os
from pathlib import Path
import tomli as tomllib


class OllamaFileDescriptor:
    def __init__(self) -> None:
        config = self.load_ollama_config()
        self.base_url = config.get("apiBase")
        self.model = config.get("model")
        self.api_url = f"{self.base_url}/api/generate"
        self.is_connectable = self.check_server_connectivity()
    
    def load_ollama_config(self, config_path: str = "ollama.toml") -> dict:
        """
        ollama.toml에서 ollama 설정을 읽어오는 함수
        
        Args:
            config_path: ollama.toml 파일 경로
            
        Returns:
            ollama 설정 딕셔너리
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")
        
        # Python 3.11+에서는 'rb' 모드로 읽기
        with open(config_file, 'rb') as f:
            config = tomllib.load(f)
        
        # ollama 설정 추출
        ollama_config = config.get('ollama', {})
        
        if not ollama_config:
            raise ValueError("pyproject.toml에서 ollama 설정을 찾을 수 없습니다")
        
        return ollama_config

    def check_server_connectivity(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}", timeout=5)
            return response.status_code == 200
        except (requests.RequestException, AttributeError):
            return False
    
    def read_file(self, file_path):
        """파일 내용을 읽어서 반환"""
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 300 * 1024:
                raise ValueError("")

            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception | UnicodeDecodeError:
            filename_with_ext = os.path.basename(file_path)
            filename, ext = os.path.splitext(filename_with_ext)

            creation_time = os.path.getctime(file_path)
            modification_time = os.path.getmtime(file_path)
            access_time = os.path.getatime(file_path)

            result = (
                f"Filename: {filename}\n"
                f"Extension: {ext}\n"
                f"Size: {file_size} bytes\n"
                f"Creation Time: {creation_time}\n"
                f"Modification Time: {modification_time}\n"
                f"Access Time: {access_time}"
            )
            return str(result)
    
    def describe_file_with_requests(self, file_path: str) -> str:
        if not self.is_connectable:
            return ""
        """requests 라이브러리를 사용하여 파일 설명 요청"""
        file_content = self.read_file(file_path)
        file_name = os.path.basename(file_path)
        
        prompt = f"""
파일명: {file_name}
파일 내용:
'''
{file_content}
'''

이 파일이 어떤 파일인지 한글 15자 이내로 설명만 작성. 개조식으로 작성.
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if len(result.get('response')) > 100:
                return ''
            return result.get('response', '응답을 받지 못했습니다.')
            
        except requests.RequestException as e:
            return ""
        except json.JSONDecodeError as e:
            return ""

descriptor = OllamaFileDescriptor()
