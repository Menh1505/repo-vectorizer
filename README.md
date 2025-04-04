# Code Vectorizer

Code Vectorizer is a tool designed to process source code repositories, extract code blocks, generate embeddings using pre-trained models, and store them in a FAISS index for efficient similarity search. It also provides metadata and detailed information about the processed code blocks.

## Features

- Extracts code blocks from source code repositories.
- Generates embeddings for code blocks using pre-trained models.
- Stores embeddings in a FAISS index for similarity search.
- Outputs metadata and detailed information about the processed code.

## Project Structure
.gitignore 
main.py 
requirements.txt 
run.sh 
src/ 
    crawler.py 
    embedding.py 
    parser.py 
    storage.py 
    pycache/


### Key Files and Directories

- **`main.py`**: The entry point of the application. Orchestrates the entire workflow.
- **`src/`**: Contains the core modules:
  - `crawler.py`: Handles crawling of source code files.
  - `parser.py`: Parses the content of code files.
  - `embedding.py`: Generates embeddings for code blocks.
  - `storage.py`: Manages storage and retrieval of embeddings and metadata using FAISS.
- **`output/`**: Stores the generated output files:
  - `blocks.json`: Contains detailed information about the processed code blocks.
  - `metadata.json`: Metadata associated with the embeddings.
  - `vectors.faiss`: FAISS index for similarity search.
- **`.gitignore`**: Specifies files and directories to exclude from version control.

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd code_vectorizer
   ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    `pip install -r requirements.txt`

## Usage

Run the tool using the main.py script:
`python main.py --repo-path <path_to_repository> --output-dir <output_directory>`

Arguments:
* --repo-path: Path to the source code repository to process.
* --output-dir: Directory to save the output files.
* --model-name (optional): Name of the embedding model (default: all-MiniLM-L6-v2).

## Workflow

1. **Crawling**: Extracts code blocks from the repository using [crawler.py](./src/crawler.py).
2. **Parsing**: Processes the extracted code blocks using [parser.py](./src/parser.py).
3. **Embedding**: Generates embeddings for the parsed code blocks using [embedding.py](./src/embedding.py).
4. **Storage**: Stores the embeddings and metadata in a FAISS index using [storage.py](./src/storage.py).

## Output Files

- **blocks.json**: Contains detailed information about the processed code blocks.
- **metadata.json**: Metadata for the embeddings, including file paths and programming languages.
- **vectors.faiss**: FAISS index containing the embeddings.

## Example

`python ./main.py --repo-path ../example-repo --output-dir ./output`
This command processes the example-repo directory and saves the results in the output directory.

## Development

**Adding New Features**
- Extend functionality by modifying or adding modules in the src/ directory.
- Ensure new features are tested and documented.

**Ignored Files**
The following files and directories are excluded from version control (as specified in .gitignore):
- **venv/**: Virtual environment directory.
- **output/**: Generated output files.
- **.env**: Environment configuration file.

## License
This project is licensed under the [MIT](./LICENSE.md).

---
If you got bug or need to help, please create new issue or contact via
telegram: [@Menhythien]
gmail: [dinhthienmenh1505@gmail.com]