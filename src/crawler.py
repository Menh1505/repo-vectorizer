# src/crawler.py
import os
from git import Repo
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
import mimetypes

class CodeCrawler:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.ignored_dirs = {'.git', 'target', 'build', 'node_modules', '__pycache__'}
        self.ignored_files = {'.DS_Store', '*.pyc', '*.pyo', '*.pyd'}
        
    def crawl(self) -> List[Dict]:
        """Crawl all files from repository"""
        all_blocks = []
        
        # Walk through all files
        for root, dirs, files in os.walk(self.repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self._should_process_file(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        file_type = self._get_file_type(file_path)
                        all_blocks.append({
                            'path': str(file_path),
                            'content': content,
                            'type': file_type,
                            'language': self._detect_language(file_path),
                            'relative_path': str(file_path.relative_to(self.repo_path))
                        })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                        
        return all_blocks
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        try:
            # Skip ignored files
            if any(file_path.name.endswith(pattern.replace('*', '')) for pattern in self.ignored_files):
                return False
                
            # Skip binary files
            if file_path.suffix in {'.wasm', '.bin', '.exe', '.dll', '.so', '.dylib'}:
                return False
                
            # Skip large files
            if file_path.stat().st_size > 10 * 1024 * 1024:  # Skip files larger than 10MB
                return False
                
            return True
        except Exception as e:
            print(f"Error checking file {file_path}: {e}")
            return False
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        name = file_path.name.lower()
        
        # Documentation files
        if name in {'readme.md', 'readme', 'readme.txt'}:
            return 'readme'
        elif name.endswith('.md'):
            return 'markdown'
        elif name.endswith('.rst'):
            return 'restructuredtext'
            
        # Code files
        elif name.endswith('.rs'):
            return 'rust'
        elif name.endswith('.move'):
            return 'move'
        elif name.endswith('.py'):
            return 'python'
        elif name.endswith('.js'):
            return 'javascript'
        elif name.endswith('.ts'):
            return 'typescript'
        elif name.endswith('.java'):
            return 'java'
        elif name.endswith('.cpp'):
            return 'cpp'
        elif name.endswith('.c'):
            return 'c'
        elif name.endswith('.h'):
            return 'header'
        elif name.endswith('.hpp'):
            return 'cpp_header'
        elif name.endswith('.cs'):
            return 'csharp'
        elif name.endswith('.go'):
            return 'go'
        elif name.endswith('.rb'):
            return 'ruby'
        elif name.endswith('.php'):
            return 'php'
        elif name.endswith('.swift'):
            return 'swift'
        elif name.endswith('.kt'):
            return 'kotlin'
        elif name.endswith('.scala'):
            return 'scala'
            
        # Configuration files
        elif name in {'cargo.toml', 'package.json', 'requirements.txt', 'setup.py', 'pom.xml'}:
            return 'config'
            
        # Other text files
        else:
            return 'text'
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext_to_lang = {
            '.rs': 'rust',
            '.move': 'move',
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala'
        }
        return ext_to_lang.get(file_path.suffix, 'unknown')