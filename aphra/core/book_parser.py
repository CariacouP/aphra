import re
from pathlib import Path
from typing import List, Dict, Union

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def parse_epub(file_path: Union[str, Path]) -> List[Dict[str, str]]:
    """
    Parses an EPUB file and extracts its chapters.
    
    Args:
        file_path: The path to the EPUB file.
        
    Returns:
        A list of dictionaries, each containing 'title' and 'content' for a chapter.
    """
    try:
        # Ignore ebooklib warnings about missing titles/navigation by overriding the warnings or capturing them
        # ebooklib is known to be very verbose
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            book = epub.read_epub(str(file_path))
    except Exception as e:
        raise ValueError(f"Failed to parse EPUB file: {e}")

    chapters = []
    
    chapter_count = 1
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Extract HTML content
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Try to find a title
            title_tag = soup.find(['h1', 'h2', 'title'])
            if title_tag:
                title = title_tag.get_text().strip()
            else:
                title = f"Chapter {chapter_count}"
                
            # Extract plain text content
            content = soup.get_text(separator='\n\n', strip=True)
            
            # Skip empty documents or those with very little substantial text
            if len(content) > 10:
                chapters.append({
                    'title': title,
                    'content': content
                })
                chapter_count += 1
                
    return chapters


def parse_markdown(file_path_or_content: Union[str, Path]) -> List[Dict[str, str]]:
    """
    Parses a Markdown file or content string and splits it into logical chapters
    based on ATX headings (# or ##).
    
    Args:
        file_path_or_content: Path to the Markdown file, or the raw Markdown string.
        
    Returns:
        A list of dictionaries, each containing 'title' and 'content' for a chapter.
    """
    # Check if it's an existing file
    try:
        path = Path(file_path_or_content)
        if path.is_file():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = str(file_path_or_content)
    except OSError:
        # If path creation or reading fails, assume it's just raw content
        content = str(file_path_or_content)

    chapters = []
    
    # Regex to match Markdown headings level 1 or 2
    # e.g., "# Title" or "## Title"
    heading_pattern = re.compile(r'^(#{1,2})\s+(.*)$', re.MULTILINE)
    
    matches = list(heading_pattern.finditer(content))
    
    if not matches:
        # No headings found, treat the whole content as a single chapter
        if content.strip():
            chapters.append({
                'title': 'Chapter 1',
                'content': content.strip()
            })
        return chapters

    # Split the content based on the matches
    for i, match in enumerate(matches):
        title = match.group(2).strip()
        
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        chapter_content = content[start_idx:end_idx].strip()
        
        # Avoid appending empty chapters if there are consecutive headings
        if chapter_content:
            chapters.append({
                'title': title,
                'content': chapter_content
            })
            
    return chapters
