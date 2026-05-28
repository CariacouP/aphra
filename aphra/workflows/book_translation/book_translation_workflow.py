"""
Book Translation workflow implementation.

This workflow implements the 5-step translation process, with an added
Lorebook management system to ensure continuity across chapters.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from ...core.context import TranslationContext
from ...core.workflow import AbstractWorkflow
from .aux.parsers import parse_analysis, parse_translation

class BookTranslationWorkflow(AbstractWorkflow):
    """
    Workflow for translating books chapter by chapter, maintaining a lorebook.
    """

    def get_workflow_name(self) -> str:
        return "book_translation"

    def is_suitable_for(self, text: str, **_kwargs) -> bool:
        # Default to false, users should explicitly choose this workflow with -w
        return False
        
    def _get_lorebook_path(self, context: TranslationContext) -> Path:
        input_file = context.metadata.get('input_file')
        if not input_file:
            return Path("workspace/lorebook.md")
            
        # Expecting path like: Livre_1/01_original/ch1.md
        # The workspace is at Livre_1/workspace/lorebook.md
        p = Path(input_file).resolve()
        workspace_dir = p.parent.parent / "workspace"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        return workspace_dir / "lorebook.md"

    def _read_lorebook(self, context: TranslationContext) -> str:
        lb_path = self._get_lorebook_path(context)
        if lb_path.exists():
            with open(lb_path, "r", encoding="utf-8") as f:
                return f.read()
        return "No existing lorebook. This is the first chapter."

    def _write_lorebook(self, context: TranslationContext, content: str) -> None:
        lb_path = self._get_lorebook_path(context)
        with open(lb_path, "w", encoding="utf-8") as f:
            f.write(content)

    def analyze(self, context: TranslationContext, text: str, lorebook: str) -> List[Dict[str, Any]]:
        writer_model = context.get_workflow_config('writer')
        analyzer_model = context.get_workflow_config('analyzer', writer_model)
        system_prompt = self.get_prompt(
            'step1_system.txt',
            post_content=text,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step1_user.txt',
            post_content=text,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        analysis_content = context.model_client.call_model(
            system_prompt, user_prompt, analyzer_model, log_call=context.log_calls, stream=True
        )
        return parse_analysis(analysis_content)

    def search(self, context: TranslationContext, parsed_items: List[Dict[str, Any]]) -> str:
        if not parsed_items:
            return ""
        searcher_model = context.get_workflow_config('searcher')
        glossary = []
        for item in parsed_items:
            term_explanation = self._generate_term_explanation(context, item, searcher_model)
            glossary_entry = (
                f"### {item['name']}\n\n**Keywords:** {', '.join(item['keywords'])}\n\n"
                f"**Explanation:**\n{term_explanation}\n"
            )
            glossary.append(glossary_entry)
        return "\n".join(glossary)

    def translate(self, context: TranslationContext, text: str, lorebook: str, glossary: str) -> str:
        writer_model = context.get_workflow_config('writer')
        system_prompt = self.get_prompt(
            'step3_system.txt',
            text=text,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step3_user.txt',
            text=text,
            lorebook=lorebook,
            glossary=glossary,
            source_language=context.source_language,
            target_language=context.target_language
        )
        raw_translation = context.model_client.call_model(
            system_prompt, user_prompt, writer_model, log_call=context.log_calls, stream=True
        )
        
        from ...core.parsers import parse_xml_tag
        parsed = parse_xml_tag(raw_translation, "translation")
        if parsed:
            return parsed
            
        # Fallback if the model forgot the tags
        logging.warning("No <translation> tag found. Returning raw content.")
        return raw_translation.strip()

    def critique(self, context: TranslationContext, text: str, translation: str, glossary: str, lorebook: str) -> str:
        critiquer_model = context.get_workflow_config('critiquer')
        system_prompt = self.get_prompt(
            'step4_system.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step4_user.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        return context.model_client.call_model(
            system_prompt, user_prompt, critiquer_model, log_call=context.log_calls, stream=True
        )

    def refine(self, context: TranslationContext, text: str, *, translation: str, glossary: str, critique: str, lorebook: str) -> str:
        writer_model = context.get_workflow_config('writer')
        system_prompt = self.get_prompt(
            'step5_system.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            critique=critique,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step5_user.txt',
            text=text,
            translation=translation,
            glossary=glossary,
            critique=critique,
            lorebook=lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        final_translation_content = context.model_client.call_model(
            system_prompt, user_prompt, writer_model, log_call=context.log_calls, stream=True
        )
        return parse_translation(final_translation_content)

    def update_lorebook(self, context: TranslationContext, text: str, translation: str, old_lorebook: str) -> str:
        writer_model = context.get_workflow_config('writer')
        system_prompt = self.get_prompt(
            'step6_system.txt',
            text=text,
            translation=translation,
            lorebook=old_lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step6_user.txt',
            text=text,
            translation=translation,
            lorebook=old_lorebook,
            source_language=context.source_language,
            target_language=context.target_language
        )
        new_lorebook = context.model_client.call_model(
            system_prompt, user_prompt, writer_model, log_call=context.log_calls, stream=True
        )
        # Extract markdown content if wrapped in backticks
        if "```markdown" in new_lorebook:
            new_lorebook = new_lorebook.split("```markdown")[1].split("```")[0].strip()
        elif "```" in new_lorebook:
            new_lorebook = new_lorebook.split("```")[1].split("```")[0].strip()
            
        return new_lorebook

    def _chunk_text(self, text: str, max_chars: int = 3000) -> List[str]:
        """Splits text into chunks by paragraphs to avoid cutting mid-sentence."""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
                
            if current_length + len(p) > max_chars and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [p]
                current_length = len(p)
            else:
                current_chunk.append(p)
                current_length += len(p)
                
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            
        return chunks

    def execute(self, context: TranslationContext, text: str) -> str:
        print("\n⏳ Lecture du Lorebook...")
        lorebook = self._read_lorebook(context)
        print("✅ Lorebook chargé.")
        
        chunks = self._chunk_text(text, max_chars=1500)
        total_chunks = len(chunks)
        print(f"\n📦 Texte découpé en {total_chunks} morceaux (chunks).")

        final_translated_text = ""

        for i, chunk in enumerate(chunks, 1):
            print("\n" + "="*50)
            print(f"🚀 TRAITEMENT DU CHUNK {i}/{total_chunks}")
            print("="*50)

            print(f"\n🧠 [1/6] Analyse du chunk {i}...")
            analysis = self.analyze(context, chunk, lorebook)
            print(f"✅ Analyse terminée. {len(analysis)} termes clés identifiés.")

            print(f"\n🔍 [2/6] Recherche du contexte pour le chunk {i}...")
            glossary = self.search(context, analysis)
            print("✅ Glossaire généré.")

            print(f"\n✍️  [3/4] Traduction (Fast-Track) en cours (Streaming)...")
            translation = self.translate(context, chunk, lorebook, glossary)
            print("✅ Traduction terminée.")

            print(f"\n📚 [4/4] Mise à jour du Lorebook (Streaming)...")
            new_lorebook = self.update_lorebook(context, chunk, translation, lorebook)
            
            # The lorebook becomes the new baseline for the next chunk
            lorebook = new_lorebook
            self._write_lorebook(context, lorebook)
            print("✅ Lorebook sauvegardé avec succès.")
            
            # Append to final text
            final_translated_text += translation + "\n\n"

        print("\n🎉 Traduction de l'intégralité du chapitre terminée !\n")
        return final_translated_text.strip()

    def _generate_term_explanation(self, context: TranslationContext, item: Dict[str, Any], model: str) -> str:
        system_prompt = self.get_prompt(
            'step2_system.txt',
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=context.source_language,
            target_language=context.target_language
        )
        user_prompt = self.get_prompt(
            'step2_user.txt',
            term=item['name'],
            keywords=", ".join(item['keywords']),
            source_language=context.source_language,
            target_language=context.target_language
        )
        return context.model_client.call_model(
            system_prompt, user_prompt, model, log_call=context.log_calls, enable_web_search=True, web_search_context="high"
        )
