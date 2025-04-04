# src/embedding.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import json

class CodeEmbedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        
    def embed(self, blocks: List[Dict]) -> np.ndarray:
        """Create embeddings for all blocks"""
        texts = []
        for block in blocks:
            # Convert block to meaningful text
            text = self._block_to_text(block)
            texts.append(text)
            
        # Create embeddings
        embeddings = self.model.encode(texts)
        return embeddings
    
    def _block_to_text(self, block: Dict) -> str:
        """Convert block to meaningful text"""
        parsed = block.get('parsed', {})
        file_type = block['type']
        
        parts = []
        
        # Add file information
        parts.append(f"File: {block['relative_path']}")
        parts.append(f"Type: {file_type}")
        parts.append(f"Language: {block['language']}")
        
        if file_type in {'readme', 'markdown', 'restructuredtext'}:
            # Documentation
            for section in parsed.get('sections', []):
                parts.append(f"Section: {section['title']}")
                parts.extend(section['content'])
                
            # Code blocks
            for code_block in parsed.get('code_blocks', []):
                parts.append(f"Code block ({code_block['language']}):")
                parts.append(code_block['code'])
                
            # Links
            for link in parsed.get('links', []):
                parts.append(f"Link: {link['text']} -> {link['url']}")
                
            # Images
            for img in parsed.get('images', []):
                parts.append(f"Image: {img['alt']} -> {img['url']}")
                
        elif file_type in {'rust', 'move', 'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'go'}:
            # Code files
            for func in parsed.get('functions', []):
                parts.append(f"Function: {func}")
                
            for cls in parsed.get('classes', []):
                parts.append(f"Class: {cls}")
                
            for struct in parsed.get('structs', []):
                parts.append(f"Struct: {struct}")
                
            for trait in parsed.get('traits', []):
                parts.append(f"Trait: {trait}")
                
            for imp in parsed.get('imports', []):
                parts.append(f"Import: {imp}")
                
        elif file_type == 'config':
            # Configuration files
            config = parsed.get('config', {})
            if isinstance(config, dict):
                for section, values in config.items():
                    parts.append(f"Section [{section}]:")
                    if isinstance(values, dict):
                        for key, value in values.items():
                            parts.append(f"  {key} = {value}")
                    else:
                        parts.append(f"  {values}")
            else:
                parts.append(f"Config: {config}")
                    
        else:
            # Text files
            parts.extend(parsed.get('paragraphs', []))
            
        return "\n".join(parts)