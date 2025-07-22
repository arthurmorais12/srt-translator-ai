# 🎬 SRT Translator AI

A powerful CLI tool for translating subtitle files (.srt) using artificial intelligence. Supports multiple AI providers, including OpenAI, Google Gemini, and Groq.

## ✨ Features

- 🤖 **Multiple AI Providers**: Support for OpenAI, Google Gemini, and Groq.
- 🎯 **Format Preservation**: Maintains the original SRT file timing and structure.
- 🌍 **Multiple Languages**: Support for various language codes.
- 🚀 **Command-Line Interface**: Easy to use and integrate into scripts.

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- `uv` or `pip`

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd srt-translator-ai
   ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    # Option A: Using uv
    uv sync

    # Option B: Using Python's native venv module
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the project:**
    This step will install all necessary dependencies and add the `srt-translate` command to your terminal.

    **Option A: Using `uv` (recommended)**
    ```bash
    uv pip install -e .
    ```

    **Option B: Using `pip`**
    ```bash
    pip install -e .
    ```
    *(The `-e` flag installs the project in "editable" mode, which means changes to the source code are applied instantly without reinstalling.)*

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root and add your API keys:
    ```env
    # Choose at least one AI provider
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key
    GROQ_API_KEY=your_groq_api_key
    ```

## 🔑 API Configuration

### OpenAI
1. Visit the [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add the key to the `.env` file

### Google Gemini
1. Visit the [Google AI Studio](https://aistudio.google.com/)
2. Create an API key for Gemini
3. Add the key to the `.env` file

### Groq
1. Visit the [Groq Console](https://console.groq.com/)
2. Create an account and get your API key
3. Add the key to the `.env` file

## 📖 How to Use

After installation, the `srt-translate` command will be available in your terminal (as long as the virtual environment is active).

### Main Command
```bash
srt-translate [FILE] [OPTIONS]
```

#### Arguments:
- `FILE`: Path to the input .srt file (required).

#### Options:
- `--provider, -p`: AI provider to use (openai, google, groq) [default: groq].
- `--to, -t`: Target language [default: pt-br].
- `--from, -f`: Source language [default: en].
- `--output, -o`: Path to the output file (optional, auto-generated if not provided).
- `--help`: Show the help message and exit.

### Usage Examples

#### 1. Basic Translation (Default: English → Portuguese with Groq)
```bash
srt-translate my_movie.srt
```

#### 2. Translating to a Specific Language
From English to Spanish:
```bash
srt-translate subtitles.srt --to es
```

#### 3. Using a Specific Provider
Using Google Gemini for the translation:
```bash
srt-translate subtitles.srt --provider google
```

#### 4. Specifying an Output File
```bash
srt-translate subtitles.srt --output subtitles_translated.srt
```

#### 5. Complete Example with All Options
```bash
srt-translate original_subs.srt \
  --provider openai \
  --from en \
  --to fr \
  --output final_subs.fr.srt
```
## 🌍 Supported Language Codes

The project supports standard ISO 639-1 language codes. Some examples:

- `en` - English
- `pt-br` - Portuguese (Brazil)
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese
- `ru` - Russian

## ⚙️ Advanced Configuration

### Rate Limiting
The project includes automatic request rate control to avoid API errors:

- **30 requests per minute** by default
- **25 subtitles per batch** for optimization

### Project Structure
```
srt-translator-ai/
├── src/
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Configuration and environment variables
│   └── services/
│       ├── srt_parser.py # SRT file parser
│       └── translator.py # Translation service
├── pyproject.toml        # Project dependencies and configuration
└── .env                  # Environment variables (create this file)
```
## 🐛 Troubleshooting

### Error: "API key not configured"
**Solution**: Check if the .env file exists in the project root and contains the correct keys for the selected provider.

### Error: "File not found"
**Solution**: Verify that the path to the input .srt file is correct.

### Encoding Issues
**Solution**: Ensure the input .srt file is saved with UTF-8 encoding.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - AI application framework
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [srt](https://github.com/cdown/srt) - SRT file manipulation library

## 📞 Support

If you encounter issues or have questions, please open an issue in the project repository.