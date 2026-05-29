"""
Command-line runner for Aphra translation system.

This module provides a command-line interface to the Aphra translation
functionality, allowing batch processing of text files.

Usage:
    # New style (flags):
    python aphra_runner.py -c config.toml -s Spanish -t English -i input.md -o output.md -w short_article

    # Legacy style (positional, backwards-compatible):
    python aphra_runner.py config.toml Spanish English input.md output.md [workflow]
"""
import sys
import argparse
import urllib.parse
from aphra import translate


def decode_path(path):
    """
    Decode URL-encoded file paths.

    Args:
        path: URL-encoded file path string

    Returns:
        str: Decoded file path
    """
    return urllib.parse.unquote(path)


def parse_args():
    """
    Parse command-line arguments supporting flag-based, legacy positional styles, and translate-book.

    Returns:
        tuple: (argparse.Namespace, bool indicating if it's the translate-book mode)
    """
    if len(sys.argv) > 1 and sys.argv[1] == 'translate-book':
        parser = argparse.ArgumentParser(description="Aphra book translation runner")
        parser.add_argument('command', help="Command name (translate-book)")
        parser.add_argument('-c', '--config', required=True, help="Path to config file")
        parser.add_argument('-s', '--source', required=True, help="Source language")
        parser.add_argument('-t', '--target', required=True, help="Target language")
        parser.add_argument('-i', '--input', required=True, help="Input file path (.epub or .md) or directory")
        parser.add_argument('-n', '--name', required=True, help="Name of the book (for output folder)")
        return parser.parse_args(), True

    # Legacy mode: first arg doesn't start with '-' → positional style
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        parser = argparse.ArgumentParser(
            description="Aphra translation runner (legacy positional mode)"
        )
        parser.add_argument('config', help="Path to config file (e.g. config.toml)")
        parser.add_argument('source', help="Source language (e.g. Spanish)")
        parser.add_argument('target', help="Target language (e.g. English)")
        parser.add_argument('input', help="Input file path")
        parser.add_argument('output', help="Output file path")
        parser.add_argument('workflow', nargs='?', default=None, help="Workflow name (optional)")
        return parser.parse_args(), False

    # New flag-based mode
    parser = argparse.ArgumentParser(
        description="Aphra translation runner"
    )
    parser.add_argument('-c', '--config', required=True, help="Path to config file (e.g. config.toml)")
    parser.add_argument('-s', '--source', required=True, help="Source language (e.g. Spanish)")
    parser.add_argument('-t', '--target', required=True, help="Target language (e.g. English)")
    parser.add_argument('-i', '--input', required=True, help="Input file path")
    parser.add_argument('-o', '--output', required=True, help="Output file path")
    parser.add_argument('-w', '--workflow', default=None, help="Workflow name (optional)")
    return parser.parse_args(), False


def main():
    """
    Main entry point for command-line translation.
    """
    args, is_book = parse_args()

    if is_book:
        import os
        from pathlib import Path
        from aphra.core.book_parser import parse_epub, parse_markdown

        config_file = decode_path(args.config)
        input_path = decode_path(args.input)
        book_name = args.name

        base_dir = Path("Traduction_Livres") / book_name
        original_dir = base_dir / "01_original"
        translated_dir = base_dir / "02_traduit"
        original_dir.mkdir(parents=True, exist_ok=True)
        translated_dir.mkdir(parents=True, exist_ok=True)

        input_p = Path(input_path)
        saved_files = []

        if input_p.is_file():
            print(f"📦 Extraction des chapitres de {input_path}...")
            if input_p.suffix.lower() == '.epub':
                chapters = parse_epub(input_p)
            else:
                chapters = parse_markdown(input_p)

            for i, chap in enumerate(chapters, 1):
                chap_filename = f"chap_{i}.md"
                chap_path = original_dir / chap_filename
                with open(chap_path, "w", encoding="utf-8") as f:
                    f.write(f"# {chap['title']}\n\n{chap['content']}")
                saved_files.append(chap_path)
            print(f"✅ {len(saved_files)} chapitres extraits et sauvegardés dans {original_dir}")
        elif input_p.is_dir():
            saved_files = sorted(input_p.glob("*.md"))
            print(f"📦 {len(saved_files)} fichiers Markdown trouvés dans le dossier {input_path}.")
        else:
            print("Erreur: L'entrée doit être un fichier ou un dossier valide.")
            sys.exit(1)

        for chap_path in saved_files:
            print(f"\n🚀 Lancement de la traduction pour : {chap_path.name}")
            with open(chap_path, 'r', encoding='utf-8') as f:
                text = f.read()

            translated_text = translate(
                source_language=args.source,
                target_language=args.target,
                text=text,
                config_file=config_file,
                workflow="book_translation",
                input_file=str(chap_path)
            )

            out_path = translated_dir / chap_path.name
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)

            print(f"✅ Chapitre traduit sauvegardé sous : {out_path}")

        return

    config_file = decode_path(args.config)
    input_file = decode_path(args.input)
    output_file = decode_path(args.output)

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    translated_text = translate(
        source_language=args.source,
        target_language=args.target,
        text=text,
        config_file=config_file,
        workflow=args.workflow,
        input_file=input_file
    )

    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)


if __name__ == "__main__":
    main()
