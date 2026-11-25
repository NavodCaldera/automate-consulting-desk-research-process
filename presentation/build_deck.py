#!/usr/bin/env python3
"""Finish a Canva-exported MTI ResearchOS deck for the repository.

Canva is the authoritative editable design. Download it as PPTX, then run:

    python presentation/build_deck.py presentation/MTI-ResearchOS.pptx

The script restores the full presenter notes from the repo specification,
adds footer slide numbers, and writes a validated PowerPoint to the requested
output path. It does not recreate Canva's visual design from scratch.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt


NOTES = [
    "This is a concept and architecture proposal for automating MTI's desk research, from receiving a brief to delivering a validated research pack, targeting 90–95% automation without giving up accuracy.",
    "MTI's work depends on desk research across 56 countries, often in frontier markets where data is thin. Today a brief takes 2–3 analyst days. The goal isn't just speed: it's speed with every number traceable.",
    "I define automation as the share of analyst time removed, not as a vague claim. It always comes with a guardrail: audited accuracy. A system that auto-approves everything would score 100% automation and be useless. This definition makes that impossible.",
    "Walk the flow once. Stress that everything between the gates is automatic and that gates are short and focused.",
    "Agents never pass free text to each other. They read and write typed ledger records. LangGraph keeps state, so a failed run resumes from its checkpoint and pauses at each gate for a human. The judge is deliberately a different vendor.",
    "This is the heart of the design. The report is generated from these cards, so the model can't invent a number. If it isn't in the ledger, it can't appear in the deck.",
    "This is why I don't recommend just buying a deep-research tool. The best one still gets about 1 in 10 citations wrong, and for consulting that's unacceptable. Validation is the core of the system, not an add-on.",
    "Cheap checks run on everything; expensive checks run only where needed. That's how we get accuracy without the cost of checking every claim with every method.",
    "Every claim carries a label, so the consultant sees at a glance what's solid and what needs judgement. Nothing is silently deleted.",
    "This is the biggest gap in generic AI research tools. They either invent a number or say 'not found'. A consultant triangulates. So does this system, transparently.",
    "Walk the timeline. Point out the three flags the system caught on its own, and that the human only saw 12 of 150 claims.",
    "This is the human-in-the-loop experience. The consultant doesn't reread a report. They clear a short queue of cards, each with the evidence on one screen.",
    "One unlucky error doesn't collapse automation, but real drift is caught within weeks. Automation can never be bought with silent accuracy loss.",
    "This is where most AI pilots fail in consulting: confidentiality. The rule is simple and enforced by architecture. The data class decides which model may see it.",
    "Mention that the full 17-risk register is in the appendix, including prompt injection, key-person risk and analyst adoption.",
    "I tested the question of free models seriously. Free and local models are in the design, but only where accuracy risk and data sensitivity are low. Cost is driven by the research model, not by the checking models.",
    "Every layer has a free alternative, which is exactly how the prototype runs at zero cost.",
    "Even at a conservative $10 an hour and only 10 briefs a month, it pays back within months. At 30 briefs, it frees about 550 analyst hours a month.",
    "Each phase has an objective exit criterion. If a bought tool meets the targets in Phase 0, we buy it. That decision is made on evidence.",
    "My ask is a two-week Phase 0 with 20–30 past briefs. That alone proves or disproves the numbers on MTI's own work.",
]

INK = RGBColor(0x47, 0x55, 0x69)


def add_page_number(slide, number: int, slide_width: int, slide_height: int) -> None:
    """Add or replace a small right-aligned page number, excluding cover/close."""
    for shape in list(slide.shapes):
        if shape.name == "MTI slide number":
            shape._element.getparent().remove(shape._element)

    box = slide.shapes.add_textbox(
        Inches(19.0), Inches(10.65), Inches(0.5), Inches(0.25)
    )
    box.name = "MTI slide number"
    paragraph = box.text_frame.paragraphs[0]
    paragraph.alignment = PP_ALIGN.RIGHT
    run = paragraph.add_run()
    run.text = str(number)
    run.font.name = "Calibri"
    run.font.size = Pt(9)
    run.font.color.rgb = INK


def build(source: Path, output: Path) -> None:
    presentation = Presentation(str(source))
    if len(presentation.slides) != 24:
        raise ValueError(f"Expected 24 slides (20 numbered + 4 appendix), found {len(presentation.slides)}")

    for index, slide in enumerate(presentation.slides, start=1):
        if index <= len(NOTES):
            slide.notes_slide.notes_text_frame.text = NOTES[index - 1]
        if index not in (1, 20):
            add_page_number(slide, index, presentation.slide_width, presentation.slide_height)

    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(suffix=".pptx", dir=output.parent, delete=False) as temp:
        temp_path = Path(temp.name)
    try:
        presentation.save(str(temp_path))
        checked = Presentation(str(temp_path))
        if len(checked.slides) != 24:
            raise ValueError("Saved presentation failed the slide-count check")
        missing_notes = [i for i, slide in enumerate(checked.slides, 1)
                         if not slide.has_notes_slide or not slide.notes_slide.notes_text_frame.text.strip()]
        if missing_notes:
            raise ValueError(f"Slides missing speaker notes: {missing_notes}")
        temp_path.replace(output)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> None:
    default_output = Path(__file__).with_name("MTI-ResearchOS.pptx")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=default_output,
                        help="Canva-exported PPTX (defaults to the deliverable itself)")
    parser.add_argument("output", nargs="?", type=Path, default=default_output,
                        help="final PPTX path")
    args = parser.parse_args()
    build(args.source, args.output)
    print(f"Prepared {args.output}")


if __name__ == "__main__":
    main()
