# Dataset Loader for MAPS benchmark 

MAPS benchmark - a multilingual benchmark suite designed to evaluate agentic AI systems across diverse languages and tasks.

This module provides functionality to load datasets from MAPS directories
containing different languages and tasks. It supports both JSON and JSONL formats
with flexible configuration options.


## Features

- **Multi-language support**: Load datasets from multiple language directories (options: english, arabic, chinese, french, german, hebrew, hindi, italian, japanese, korean, portuguese, russian, spanish)
- **Multi-task support**: Process multiple task types simultaneously (options: swe, gaia, asb, math.)
- **Metadata enrichment**: Automatically adds language and task information to records
- **Command-line interface**: Easy-to-use CLI with comprehensive options
- **Discovery tools**: List available languages and tasks


## Installation

### Requirements

- Python 3.7+
- pandas
- Standard library modules (os, json, argparse, pathlib)

### Setup

1. Clone or download the `load_datasets.py` file
2. Install required dependencies:

```bash
pip install pandas
```


## Usage

### Command Line Interface

#### Basic Usage

```bash
# Load English datasets for SWE and GAIA tasks
python load_datasets.py --base-path datasets/MAPS --languages english --tasks swe gaia

# Load multiple languages and tasks
python load_datasets.py -b datasets/MAPS -l english arabic -t swe gaia asb

# Load with verbose output
python load_datasets.py -b datasets/MAPS -l english -t swe --verbose
```

#### Discovery Commands

```bash
# List all available languages
python load_datasets.py --base-path datasets/MAPS --list-languages

# List available tasks for a specific language
python load_datasets.py --base-path datasets/MAPS --list-tasks english
```

#### Output Options

```bash
# Save results to CSV
python load_datasets.py -b datasets/MAPS -l english -t swe --output results.csv

# Display first 5 rows
python load_datasets.py -b datasets/MAPS -l english -t swe --head 5

# Load without metadata columns
python load_datasets.py -b datasets/MAPS -l english -t swe --no-metadata
```


## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--base-path` | `-b` | Base path to dataset directory | `datasets/MAPS` |
| `--languages` | `-l` | Languages to load (space-separated) | Required |
| `--tasks` | `-t` | Tasks to load (space-separated) | Required |
| `--output` | `-o` | Output CSV file path | None |
| `--list-languages` | | List available languages | False |
| `--list-tasks` | | List tasks for specified language | None |
| `--no-metadata` | | Don't add language/task metadata | False |
| `--verbose` | `-v` | Enable verbose output | False |
| `--head` | | Display first N rows | None |

## Examples

### Example 1: Basic Dataset Loading

```bash
python load_datasets.py --base-path datasets/MAPS --languages english --tasks swe gaia
```

**Output:**
```
Successfully loaded 265 records.
Dataset shape: (265, 21)
```

### Example 2: Multiple Languages with Verbose Output

```bash
python load_datasets.py -b datasets/MAPS -l english arabic -t swe --verbose
```

**Output:**
```
[INFO] Starting dataset loading from datasets\MAPS
[INFO] Languages: ['english', 'arabic']
[INFO] Tasks: ['swe']
[INFO] Loading 1 JSON files from datasets\MAPS\english\swe
[INFO] Loaded 100 records from english.json
[INFO] Loaded 100 records for english/swe
[INFO] Loading 1 JSON files from datasets\MAPS\arabic\swe
[INFO] Loaded 100 records from arabic.json
[INFO] Loaded 100 records for arabic/swe
[INFO] Total records loaded: 200
Successfully loaded 200 records.
Dataset shape: (200, 15)
```

### Example 3: ASB Task with Special Handling

```bash
python load_datasets.py -b datasets/MAPS_verified -l english -t asb --verbose
```

**Output:**
```
[INFO] Starting dataset loading from datasets\MAPS_verified
[INFO] Languages: ['english']
[INFO] Tasks: ['asb']
[INFO] Loading all JSON files from datasets\MAPS_verified\english\asb
[INFO] Loaded 60 records from asb_en.json
[INFO] Loaded 60 records for english/asb
[INFO] Total records loaded: 60
Successfully loaded 60 records.
Dataset shape: (60, 9)
```

### Example 4: Discovery and Export

```bash
# Discover available languages
python load_datasets.py --base-path datasets/MAPS --list-languages
```

**Output:**
```
Available languages:
  - arabic
  - arabic
  - chinese
  - english
  - german
  - hebrew
  - hindi
  - italian
  - japanese
  - korean
  - portugese
  - russian
  - spanish
```

```bash
# Discover tasks for English
python load_datasets.py --base-path datasets/MAPS --list-tasks english
```

**Output:**
```
Available tasks for 'english':
  - asb
  - gaia
  - math
  - swe
```

```bash
# Load and export to CSV
python load_datasets.py -b datasets/MAPS -l english -t swe gaia --output english_datasets.csv --head 3
```

**Output:**
```
Successfully loaded 265 records.
Dataset shape: (265, 21)

First 3 rows:
   id                    question  answer  _language _task
0   1  What is the capital of France?   Paris    english   swe
1   2      How do you reverse a list?  [::-1]   english   swe
2   3         What is machine learning?     ML   english  gaia

Dataset saved to: english_datasets.csv
```

## Special Cases

### ASB Task Handling

The tool includes special logic for the "asb" task:

- **For `dataset/MAPS_verified`**: Loads all `.json` files in the asb directory
- **For other paths**: Loads only the `all_attack_tools.jsonl` file


## Metadata

By default, the tool adds two metadata columns to each record:

- `_language`: The language directory name
- `_task`: The task directory name

Use `--no-metadata` to disable this feature.

## Troubleshooting


### Debug Tips

- Use `--verbose` to see detailed loading information
- Use `--list-languages` and `--list-tasks` to verify directory structure
- Start with a small subset using `--head` option

### GAIA-Agent Careful Consideration

- When running the GAIA benchmark on the GAIA Agent, ensure that the agent (and its tools) can successfully load and read support files such as Excel files, ZIP archives, PowerPoint presentations, etc., from the support file folder.

- This is a requirement explicitly stated in the benchmark questions.

- You may need to update the file path in the GAIA Agent implementation to ensure the agent (or its tools) can correctly access and read these files.

- A good way to verify that the support files are being read correctly is to check if the agent outputs or displays the content it has read.

- This helps confirm that the agent is using the correct file path and reading the correct files.

- There is a seperate folder named "gaia_support_files" inside dataset.