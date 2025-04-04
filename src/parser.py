# src/parser.py
from typing import Dict, List
import re

class CodeParser:
    def __init__(self):
        pass
    
    def parse(self, block: Dict) -> Dict:
        """Parse content based on file type"""
        content = block['content']
        file_type = block['type']
        
        if file_type in {'readme', 'markdown', 'restructuredtext'}:
            return self._parse_documentation(content, file_type)
        elif file_type in {'rust', 'move', 'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'go'}:
            return self._parse_code(content, file_type)
        elif file_type == 'config':
            return self._parse_config(content)
        else:
            return self._parse_text(content)
    
    def _parse_documentation(self, content: str, doc_type: str) -> Dict:
        """Parse documentation files"""
        sections = []
        current_section = {'title': '', 'content': []}
        
        # Split content into sections
        lines = content.split('\n')
        for line in lines:
            if doc_type == 'markdown':
                if line.startswith('#'):
                    if current_section['title']:
                        sections.append(current_section)
                    current_section = {'title': line.lstrip('#').strip(), 'content': []}
                else:
                    current_section['content'].append(line)
            elif doc_type == 'restructuredtext':
                if line.startswith('===') or line.startswith('---'):
                    if current_section['title']:
                        sections.append(current_section)
                    current_section = {'title': '', 'content': []}
                else:
                    current_section['content'].append(line)
        
        if current_section['title']:
            sections.append(current_section)
            
        return {
            'sections': sections,
            'code_blocks': self._extract_code_blocks(content),
            'links': self._extract_links(content),
            'images': self._extract_images(content)
        }
    
    def _parse_code(self, content: str, language: str) -> Dict:
        """Parse code files using regex patterns"""
        result = {
            'functions': [],
            'classes': [],
            'structs': [],
            'traits': [],
            'imports': [],
            'comments': []
        }
        
        # Extract imports
        if language == 'python':
            result['imports'] = re.findall(r'^(?:from\s+(\w+)\s+import|\s*import\s+(\w+))', content, re.MULTILINE)
        elif language in {'rust', 'move'}:
            result['imports'] = re.findall(r'use\s+([^;]+);', content)
            
        # Extract functions
        if language == 'python':
            result['functions'] = re.findall(r'def\s+(\w+)\s*\(', content)
        elif language == 'rust':
            result['functions'] = re.findall(r'fn\s+(\w+)\s*\(', content)
        elif language == 'move':
            result['functions'] = re.findall(r'public\s+fun\s+(\w+)\s*\(', content)
            
        # Extract classes
        if language == 'python':
            result['classes'] = re.findall(r'class\s+(\w+)', content)
        elif language in {'rust', 'move'}:
            result['structs'] = re.findall(r'struct\s+(\w+)', content)
            
        # Extract comments
        if language == 'python':
            # Single line comments
            result['comments'] = re.findall(r'#\s*(.+)$', content, re.MULTILINE)
        else:
            # Single line comments
            single_line_comments = re.findall(r'//\s*(.+)$', content, re.MULTILINE)
            # Multi-line comments
            multi_line_comments = re.findall(r'/\*([^*]*\*+([^*/][^*]*\*+)*/)', content, re.DOTALL)
            result['comments'] = single_line_comments + multi_line_comments
            
        return result
    
    def _parse_config(self, content: str) -> Dict:
        """Parse configuration files"""
        config = {}
        current_section = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                if current_section:
                    config[current_section][key.strip()] = value.strip()
                else:
                    config[key.strip()] = value.strip()
                    
        return {'config': config}
    
    def _parse_text(self, content: str) -> Dict:
        """Parse general text files"""
        return {
            'paragraphs': [p.strip() for p in content.split('\n\n') if p.strip()],
            'lines': [l.strip() for l in content.split('\n') if l.strip()]
        }
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract code blocks from documentation"""
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)\n```'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1)
            code = match.group(2)
            code_blocks.append({
                'language': language,
                'code': code
            })
            
        return code_blocks
    
    def _extract_links(self, content: str) -> List[Dict]:
        """Extract links from documentation"""
        links = []
        # Markdown links
        md_pattern = r'\[(.*?)\]\((.*?)\)'
        for match in re.finditer(md_pattern, content):
            links.append({
                'text': match.group(1),
                'url': match.group(2),
                'type': 'markdown'
            })
            
        # RST links
        rst_pattern = r'`(.*?) <(.*?)>`_'
        for match in re.finditer(rst_pattern, content):
            links.append({
                'text': match.group(1),
                'url': match.group(2),
                'type': 'rst'
            })
            
        return links
    
    def _extract_images(self, content: str) -> List[Dict]:
        """Extract images from documentation"""
        images = []
        # Markdown images
        md_pattern = r'!\[(.*?)\]\((.*?)\)'
        for match in re.finditer(md_pattern, content):
            images.append({
                'alt': match.group(1),
                'url': match.group(2),
                'type': 'markdown'
            })
            
        # RST images
        rst_pattern = r'\.\. image:: (.*?)\n\s+:alt: (.*?)\n'
        for match in re.finditer(rst_pattern, content):
            images.append({
                'url': match.group(1),
                'alt': match.group(2),
                'type': 'rst'
            })
            
        return images