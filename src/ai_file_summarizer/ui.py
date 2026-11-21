from collections.abc import Iterator

import gradio as gr

from ai_file_summarizer.llm import LENGTH_INSTRUCTIONS, SummaryError, stream_summary
from ai_file_summarizer.readers import SUPPORTED_TYPES, ReadError, read_document


def summarize(file_path: str | None, length: str) -> Iterator[str]:
    if file_path is None:
        yield "**Error:** Upload a Markdown, text or PDF file first."
        return

    yield "_Reading the document and writing your summary..._"

    try:
        text = read_document(file_path)
    except ReadError as error:
        yield f"**Error:** {error}"
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
            "Upload a Markdown, text or PDF file, choose a length, and get a summary."
        )
        file = gr.File(
            label="Document",
            file_types=SUPPORTED_TYPES,
            file_count="single",
        )
        length = gr.Radio(
            choices=list(LENGTH_INSTRUCTIONS),
            value="Medium",
            label="Summary length",
        )
        button = gr.Button("Summarize", variant="primary")
        output = gr.Markdown()

        button.click(
            summarize,
            inputs=[file, length],
            outputs=output,
            trigger_mode="once",
        )

    return app