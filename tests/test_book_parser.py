import pytest
from pathlib import Path
from aphra.core.book_parser import parse_markdown, parse_epub

def test_parse_markdown_with_headings():
    content = """# Chapter 1
This is the first chapter.
## Chapter 2
This is the second chapter."""
    chapters = parse_markdown(content)
    assert len(chapters) == 2
    assert chapters[0]['title'] == "Chapter 1"
    assert "first chapter" in chapters[0]['content']
    assert chapters[1]['title'] == "Chapter 2"
    assert "second chapter" in chapters[1]['content']

def test_parse_markdown_without_headings():
    content = """This is a short story with no headings.
It just has text."""
    chapters = parse_markdown(content)
    assert len(chapters) == 1
    assert chapters[0]['title'] == "Chapter 1"
    assert "short story" in chapters[0]['content']

def test_parse_markdown_file(tmp_path):
    file_path = tmp_path / "test.md"
    file_path.write_text("# Intro\nHello world.", encoding="utf-8")
    chapters = parse_markdown(file_path)
    assert len(chapters) == 1
    assert chapters[0]['title'] == "Intro"
    assert "Hello world" in chapters[0]['content']

def test_parse_epub_empty(tmp_path):
    # This is a bit tricky without a real epub file, but we can verify the function 
    # handles invalid paths properly
    with pytest.raises(ValueError):
        parse_epub(tmp_path / "nonexistent.epub")
