import time
from pathlib import Path
from typing import Annotated, Generator, List

import srt
import typer
from rich import print as rprint
from tqdm import tqdm

from services.srt_parser import compose_srt_file, parse_srt_file
from services.translator import TranslationProvider, TranslatorService

BATCH_SIZE = 25
REQUESTS_PER_MINUTE = 30
SLEEP_BETWEEN_REQUESTS = 60 / REQUESTS_PER_MINUTE

app = typer.Typer(
    help="[bold cyan]SRT-Translate:[/bold cyan] CLI tool to translate subtitle files (.srt) using AI.",
    add_completion=False,
    rich_markup_mode="markdown",
)


def get_output_path(input_path: Path, target_lang: str) -> Path:
    original_stem = input_path.stem
    original_suffix = input_path.suffix
    base_name = original_stem.split(".")[0]
    return input_path.with_name(f"{base_name}.{target_lang}{original_suffix}")


def create_batches(items: List, batch_size: int) -> Generator[List, None, None]:
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


@app.command(
    name="translate", help="Translate a .srt file from one language to another."
)
def translate_srt(
    input_file: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Path to the source .srt file.",
        ),
    ],
    provider: Annotated[
        TranslationProvider,
        typer.Option(
            "--provider",
            "-p",
            case_sensitive=False,
            help="AI provider to use for translation",
        ),
    ] = TranslationProvider.GROQ,
    target_lang: Annotated[
        str,
        typer.Option(
            "--to",
            "-t",
            help="Target language code (e.g., 'pt-br', 'en', 'es').",
        ),
    ] = "pt-br",
    source_lang: Annotated[
        str,
        typer.Option("--from", "-f", help="Source language code (e.g., 'en', 'ja')."),
    ] = "en",
    output_file: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            help="Path to output .srt file. If not provided, will be automatically generated",
        ),
    ] = None,
):
    rprint("🚀 [bold cyan]Starting Translation[/bold cyan]")
    rprint(f"   - [b]Input File:[/b] {input_file.name}")
    rprint(f"   - [b]Provider:[/b] {provider.value}")
    rprint(f"   - [b]Translation:[/b] from '{source_lang}' to '{target_lang}'")

    if output_file is None:
        output_file = get_output_path(input_file, target_lang)

    rprint(f"   - [b]Output File:[/b] {output_file.name}")

    try:
        translator = TranslatorService(provider=provider)
        original_subtitles = list(parse_srt_file(str(input_file)))

        subtitle_batches = list(create_batches(original_subtitles, BATCH_SIZE))
        translated_subtitles = []

        rprint(
            f"\n[yellow]Translating {len(original_subtitles)} subtitles in {len(subtitle_batches)} batches...[/yellow]"
        )

        with tqdm(
            total=len(original_subtitles),
            unit=" subtitle",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
        ) as pbar:
            for i, batch in enumerate(subtitle_batches):
                texts_to_translate = [sub.content for sub in batch]

                translated_texts = translator.translate_batch(
                    texts=texts_to_translate,
                    source_lang=source_lang,
                    target_lang=target_lang,
                )

                for original_sub, translated_text in zip(batch, translated_texts):
                    translated_sub = srt.Subtitle(
                        index=original_sub.index,
                        start=original_sub.start,
                        end=original_sub.end,
                        content=translated_text,
                    )
                    translated_subtitles.append(translated_sub)

                pbar.update(len(batch))

                if i < len(subtitle_batches) - 1:
                    time.sleep(SLEEP_BETWEEN_REQUESTS)

        compose_srt_file(translated_subtitles, str(output_file))
        rprint("\n[bold green]✅ Translation completed successfully![/bold green]")
        rprint(f"   File saved to: [u]{output_file}[/u]")

    except (ValueError, FileNotFoundError) as e:
        rprint(f"\n[bold red]❌ Operation was interrupted: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"\n[bold red]❌ An unexpected error occurred: {e}[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
