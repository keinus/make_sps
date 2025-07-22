import json
import os
import re
from pathlib import Path

import requests
import tomli as tomllib


class OllamaFileDescriptor:
    def __init__(self) -> None:
        config = self.load_ollama_config()
        self.base_url = config.get("apiBase")
        self.model = config.get("model")
        self.api_url = f"{self.base_url}/api/generate"
        self.is_connectable = self.check_server_connectivity()
        self.size = self._parse_file_size(config.get('fileSize'))

    def _parse_file_size(self, s):
        match = re.match(r'(\d+)(\w+)', s)
        if not match:
            raise ValueError(f"Invalid file size format: {s}")
        number, unit = match.groups()
        number = int(number)
        unit = unit.upper()

        unit_map = {
            'B': 1,
            'KB': 1024,
            'MB': 1024**2,
            'GB': 1024**3,
            'TB': 1024**4
        }

        if unit not in unit_map:
            raise ValueError(f"Unknown unit: {unit}")

        return number * unit_map[unit]

    def load_ollama_config(self, config_path: str = "ollama.toml") -> dict:
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
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.size:
                raise ValueError("")

            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
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
        file_content = self.read_file(file_path)

        prompt = f"""
파일 내용:
'''
{file_content}
'''

이 파일이 어떤 파일인지 한글 15자 이내로 설명만 작성. 개조식 문장으로 작성. 마지막에 "입니다" 빼.
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

        except requests.RequestException:
            return ""
        except json.JSONDecodeError:
            return ""


descriptor = OllamaFileDescriptor()
