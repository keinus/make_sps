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
    
    def load_ollama_config(self, config_path: str = "pyproject.toml") -> dict:
        """
        pyproject.toml에서 ollama 설정을 읽어오는 함수
        
        Args:
            config_path: pyproject.toml 파일 경로
            
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
    
    def read_file(self, file_path):
        """파일 내용을 읽어서 반환"""
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 200 * 1024:
                filename_with_ext = os.path.basename(file_path)
                filename, ext = os.path.splitext(filename_with_ext)

                # Get additional metadata
                creation_time = os.path.getctime(file_path)
                modification_time = os.path.getmtime(file_path)
                access_time = os.path.getatime(file_path)

                # Create result string with detailed file information
                result = (
                    f"Filename: {filename}\n"
                    f"Extension: {ext}\n"
                    f"Size: {file_size} bytes\n"
                    f"Creation Time: {creation_time}\n"
                    f"Modification Time: {modification_time}\n"
                    f"Access Time: {access_time}"
                )
                return result

            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # 바이너리 파일의 경우 파일 정보만 반환
            file_info = os.stat(file_path)
            return f"바이너리 파일 - 크기: {file_info.st_size} bytes, 확장자: {Path(file_path).suffix}"
        except Exception as e:
            return f"파일 읽기 오류: {str(e)}"
    
    def describe_file_with_requests(self, file_path: str) -> str:
        if self.base_url is None:
            return ""
        """requests 라이브러리를 사용하여 파일 설명 요청"""
        file_content = self.read_file(file_path)
        file_name = os.path.basename(file_path)
        
        prompt = f"""
다음 파일에 대해 간단하고 명확하게 15자 이내로 설명해주세요. 설명만 쓰세요. 개조식으로 쓰세요. 절대 15자를 넘지 않도록. 한글로 작성.:

파일명: {file_name}
파일 내용:
{file_content}
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
            return result.get('response', '응답을 받지 못했습니다.')
            
        except requests.RequestException as e:
            return ""
        except json.JSONDecodeError as e:
            return ""

descriptor = OllamaFileDescriptor()


def main():
    # 사용 예시
    descriptor = OllamaFileDescriptor()
    
    # 파일 경로 설정
    file_path = "app/util/ollama.py"
    
    if not os.path.exists(file_path):
        print(f"파일이 존재하지 않습니다: {file_path}")
        return
    
    print("파일 분석 중...")
    print("=" * 50)
    
    print("🔍 Ollama 파일 분석 결과:")
    print("-" * 30)
    description = descriptor.describe_file_with_requests(file_path)
    print(description)

if __name__ == "__main__":
    main()