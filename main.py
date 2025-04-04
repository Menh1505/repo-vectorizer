# main.py
import argparse
from pathlib import Path
from src.crawler import CodeCrawler
from src.parser import CodeParser
from src.embedding import CodeEmbedder
from src.storage import FaissStorage
from tqdm import tqdm
import json

def main():
    parser = argparse.ArgumentParser(description='Code and Documentation Vectorizer')
    parser.add_argument('--repo-path', required=True, help='Path to repository')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--model-name', default='all-MiniLM-L6-v2', help='Name of the embedding model')
    args = parser.parse_args()
    
    # Initialize components
    crawler = CodeCrawler(args.repo_path)
    code_parser = CodeParser()
    embedder = CodeEmbedder(args.model_name)
    storage = FaissStorage(dimension=384)  # Dimension depends on the model
    
    # Crawl all files
    print("Crawling files...")
    blocks = crawler.crawl()
    
    # Parse content
    print("Parsing content...")
    for block in tqdm(blocks):
        block['parsed'] = code_parser.parse(block)
    
    # Create embeddings
    print("Creating embeddings...")
    embeddings = embedder.embed(blocks)
    
    # Store in FAISS
    print("Storing in FAISS...")
    storage.add(embeddings, blocks)
    
    # Save results
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    storage.save(
        str(output_dir / 'vectors.faiss'),
        str(output_dir / 'metadata.json')
    )
    
    # Save detailed information
    with open(output_dir / 'blocks.json', 'w') as f:
        json.dump(blocks, f, indent=2)
    
    print("Done!")

if __name__ == '__main__':
    main()