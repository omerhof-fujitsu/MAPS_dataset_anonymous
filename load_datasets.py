#!/usr/bin/env python3
"""
Dataset Loader for MAPS benchmark - a multilingual benchmark suite designed to evaluate agentic AI systems across diverse languages and tasks.



This module provides functionality to load datasets from MAPS directories
containing different languages and tasks. It supports both JSON and JSONL formats
with flexible configuration options.


Date: 2025
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd


class DatasetLoader:
    """
    A class to handle loading of datasets from structured directories.
    """
    
    def __init__(self, base_path: str, verbose: bool = False):
        """
        Initialize the DatasetLoader.
        
        Args:
            base_path (str): Root path to the dataset directory
            verbose (bool): Enable verbose logging
        """
        self.base_path = Path(base_path)
        self.verbose = verbose
        
        if not self.base_path.exists():
            raise FileNotFoundError(f"Base path '{base_path}' does not exist")
        
        if not self.base_path.is_dir():
            raise NotADirectoryError(f"Base path '{base_path}' is not a directory")
    
    def _log(self, message: str, level: str = "INFO") -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{level}] {message}")
    
    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load a JSON file and return its contents as a list of dictionaries.
        
        Args:
            file_path (Path): Path to the JSON file
            
        Returns:
            List[Dict[str, Any]]: List of records from the JSON file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
            if isinstance(content, list):
                return content
            elif isinstance(content, dict):
                return [content]
            else:
                self._log(f"Unexpected JSON structure in {file_path}", "WARNING")
                return []
                
        except json.JSONDecodeError as e:
            self._log(f"Invalid JSON in {file_path}: {e}", "ERROR")
            return []
        except Exception as e:
            self._log(f"Failed to load {file_path}: {e}", "ERROR")
            return []
    
    def _load_jsonl_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load a JSONL file and return its contents as a list of dictionaries.
        
        Args:
            file_path (Path): Path to the JSONL file
            
        Returns:
            List[Dict[str, Any]]: List of records from the JSONL file
        """
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                        
                    try:
                        record = json.loads(line)
                        data.append(record)
                    except json.JSONDecodeError as e:
                        self._log(f"Invalid JSON on line {line_num} in {file_path}: {e}", "ERROR")
                        continue
                        
        except Exception as e:
            self._log(f"Failed to load {file_path}: {e}", "ERROR")
            
        return data
    
    def _load_task_data(self, task_path: Path, task: str, language: str) -> List[Dict[str, Any]]:
        """
        Load data for a specific task.
        
        Args:
            task_path (Path): Path to the task directory
            task (str): Task name
            language (str): Language name
            
        Returns:
            List[Dict[str, Any]]: List of records for the task
        """
        data = []
        
        if task == "asb":
            # Special handling for ASB task
            if str(self.base_path) == "datasets\\MAPS_verified":
                # Load all .json files in asb folder
                self._log(f"Loading all JSON files from {task_path}")
                for file_path in task_path.glob("*.json"):
                    records = self._load_json_file(file_path)
                    data.extend(records)
                    self._log(f"Loaded {len(records)} records from {file_path.name}")
            else:
                # Load only all_attack_tools.jsonl
                jsonl_file = task_path / "all_attack_tools.jsonl"
                if jsonl_file.exists():
                    self._log(f"Loading {jsonl_file}")
                    records = self._load_jsonl_file(jsonl_file)
                    data.extend(records)
                    self._log(f"Loaded {len(records)} records from {jsonl_file.name}")
                else:
                    self._log(f"File 'all_attack_tools.jsonl' not found in {task_path}", "WARNING")
        else:
            # For other tasks, load all .json files
            json_files = list(task_path.glob("*.json"))
            if not json_files:
                self._log(f"No JSON files found in {task_path}", "WARNING")
            else:
                self._log(f"Loading {len(json_files)} JSON files from {task_path}")
                for file_path in json_files:
                    records = self._load_json_file(file_path)
                    data.extend(records)
                    self._log(f"Loaded {len(records)} records from {file_path.name}")
        
        # Add metadata to each record
        for record in data:
            if isinstance(record, dict):
                record['_language'] = language
                record['_task'] = task
        
        return data
    
    def load_dataset(self, 
                    languages: List[str], 
                    tasks: List[str],
                    add_metadata: bool = True) -> pd.DataFrame:
        """
        Load dataset from specified languages and tasks.
        
        Args:
            languages (List[str]): List of language directories to process
            tasks (List[str]): List of task directories to process
            add_metadata (bool): Whether to add language and task metadata to records
            
        Returns:
            pd.DataFrame: DataFrame containing all loaded records
            
        Raises:
            ValueError: If no valid data is found
        """
        all_data = []
        
        self._log(f"Starting dataset loading from {self.base_path}")
        self._log(f"Languages: {languages}")
        self._log(f"Tasks: {tasks}")
        
        for language in languages:
            lang_path = self.base_path / language
            
            if not lang_path.exists():
                self._log(f"Language folder '{language}' not found", "WARNING")
                continue
                
            if not lang_path.is_dir():
                self._log(f"Language path '{language}' is not a directory", "WARNING")
                continue
            
            for task in tasks:
                task_path = lang_path / task
                
                if not task_path.exists():
                    self._log(f"Task folder '{task}' not found in language '{language}'", "WARNING")
                    continue
                    
                if not task_path.is_dir():
                    self._log(f"Task path '{task}' is not a directory in language '{language}'", "WARNING")
                    continue
                
                task_data = self._load_task_data(task_path, task, language)
                all_data.extend(task_data)
                self._log(f"Loaded {len(task_data)} records for {language}/{task}")
        
        if not all_data:
            raise ValueError("No valid data found for the specified languages and tasks")
        
        self._log(f"Total records loaded: {len(all_data)}")
        return pd.DataFrame(all_data)
    
    def list_available_languages(self) -> List[str]:
        """
        List all available language directories.
        
        Returns:
            List[str]: List of available language directory names
        """
        return [d.name for d in self.base_path.iterdir() if d.is_dir()]
    
    def list_available_tasks(self, language: str) -> List[str]:
        """
        List all available task directories for a given language.
        
        Args:
            language (str): Language directory name
            
        Returns:
            List[str]: List of available task directory names
        """
        lang_path = self.base_path / language
        if not lang_path.exists() or not lang_path.is_dir():
            return []
        return [d.name for d in lang_path.iterdir() if d.is_dir()]


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Load datasets from structured directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --base-path datasets/MAPS --languages english --tasks swe gaia
  %(prog)s -b dataset/MAPS_verified -l arabic english -t asb
  %(prog)s --base-path datasets/MAPS --list-languages
  %(prog)s --base-path datasets/MAPS --list-tasks english
        """
    )
    
    parser.add_argument(
        '-b', '--base-path',
        type=str,
        default='datasets/MAPS', # Options: datasets/MAPS or dataset/MAPS_verified
        help='Base path to the dataset directory (default: datasets/MAPS)'
    )
    
    parser.add_argument(
        '-l', '--languages',
        nargs='+',
        type=str,
        help='Languages to load (e.g., english arabic)' # Options: english, arabic, chinese, french, german, hindi, italian, japanese, korean, portuguese, russian, spanish
    )
    
    parser.add_argument(
        '-t', '--tasks',
        nargs='+',
        type=str,
        help='Tasks to load (e.g., swe gaia asb)' # Options: swe, gaia, asb, math.
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output CSV file path (optional)'
    )
    
    parser.add_argument(
        '--list-languages',
        action='store_true',
        help='List available languages and exit'
    )
    
    parser.add_argument(
        '--list-tasks',
        type=str,
        metavar='LANGUAGE',
        help='List available tasks for a language and exit'
    )
    
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Do not add language and task metadata to records'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--head',
        type=int,
        metavar='N',
        help='Display first N rows of the loaded dataset'
    )
    
    return parser.parse_args()


def main():
    """Main function to run the dataset loader."""
    args = parse_arguments()
    
    try:
        loader = DatasetLoader(args.base_path, verbose=args.verbose)
        
        # Handle list operations
        if args.list_languages:
            languages = loader.list_available_languages()
            print("Available languages:")
            for lang in sorted(languages):
                print(f"  - {lang}")
            return
        
        if args.list_tasks:
            tasks = loader.list_available_tasks(args.list_tasks)
            print(f"Available tasks for '{args.list_tasks}':")
            for task in sorted(tasks):
                print(f"  - {task}")
            return
        
        # Validate required arguments
        if not args.languages:
            print("Error: --languages is required when not using --list-* options")
            sys.exit(1)
            
        if not args.tasks:
            print("Error: --tasks is required when not using --list-* options")
            sys.exit(1)
        
        # Load dataset
        df = loader.load_dataset(
            languages=args.languages,
            tasks=args.tasks,
            add_metadata=not args.no_metadata
        )
        
        print(f"Successfully loaded {len(df)} records.")
        print(f"Dataset shape: {df.shape}")
        
        if args.head:
            print(f"\nFirst {args.head} rows:")
            print(df.head(args.head).to_string())
        
        # Save to CSV if requested
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"Dataset saved to: {args.output}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()