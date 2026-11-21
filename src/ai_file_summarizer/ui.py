from collections.abc import Iterator
from pathlib import Path

import gradio as gr

from ai_file_summarizer.llm import LENGTH_INSTRUCTIONS, SummaryError, stream_summary


def summarize(file_path: str | None, length: str) -> Iterator[str]:
    if file_path is None:
        yield "**Error:** Upload a Markdown (.md) file first."
        return

    yield "_Reading the document and writing your summary..._"

    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        yield "**Error:** The file is not valid UTF-8 text."
        return

    summary = ""
    try:
        for piece in stream_summary(text, length):
            summary += piece
            yield summary
    except SummaryError as error:
        note = f"**Error:** {error}"
        yield f"{summary}\n\n{note}" if summary else note


def build_app() -> gr.Blocks:
    with gr.Blocks(title="AI File Summarizer") as app:
        gr.Markdown(
            "# AI File Summarizer\n"
            "Upload a Markdown file, choose a length, and get a summary."
        )
        file = gr.File(
            label="Markdown file",
            file_types=[".md"],
            file_count="single",
        )
        length = gr.Radio(
            choices=list(LENGTH_INSTRUCTIONS),
            value="Medium",
            label="Summary length",
        )
        button = gr.Button("Summarize", variant="primary")
        output = gr.Markdown()

        button.click(summarize, inputs=[file, length], outputs=output, trigger_mode="once",)

    return app