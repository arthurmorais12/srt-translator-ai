from typing import Generator, List

import srt
from rich import print


def parse_srt_file(filepath: str) -> Generator[srt.Subtitle, None, None]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            return srt.parse(content)
    except FileNotFoundError:
        print(f"[bold red]Erro:[/bold red]Arquivo não encontrado em {filepath}")
        raise
    except Exception as e:
        print(f"[bold red]Erro ao ler ou parsear o arquivo SRT[/bold red]: {e}")
        raise


def compose_srt_file(subtitles: List[srt.Subtitle], filepath: str):
    try:
        composed_content = srt.compose(subtitles)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(composed_content)
    except Exception as e:
        print(
            f"[bold red]Erro ao escrever o arquivo SRT em '{filepath}'[/bold red]: {e}"
        )
        raise
