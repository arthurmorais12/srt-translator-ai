# 🎬 SRT Translator AI

A powerful CLI tool for translating subtitle files (.srt) using artificial intelligence. Supports multiple AI providers including OpenAI, Google Gemini, and Groq.

## ✨ Features

- 🤖 **Multiple AI Providers**: Support for OpenAI GPT-4, Google Gemini, and Groq
- 🎯 **Format Preservation**: Maintains the original SRT file structure
- 🌍 **Multiple Languages**: Support for various language codes

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- `uv` (Python package manager)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd srt-translator-ai
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   # Choose at least one AI provider
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## 🔑 API Configuration

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add the key to the `.env` file

### Google Gemini
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an API key for Gemini
3. Add the key to the `.env` file

### Groq
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and get your API key
3. Add the key to the `.env` file

## 📖 How to Use

### Basic Command

```bash
python -m src.cli file.srt
```

### Available Options

```bash
python -m src.cli [FILE] [OPTIONS]
```

#### Arguments:
- `FILE`: Path to the input .srt file (required)

#### Options:
- `--provider, -p`: AI provider (openai, google, groq) [default: groq]
- `--to, -t`: Target language [default: pt-br]
- `--from, -f`: Source language [default: en]
- `--output, -o`: Output file path (optional)

### Usage Examples

#### 1. Basic Translation (English → Portuguese)
```bash
python -m src.cli movie.srt
```

#### 2. Translation with Specific Language
```bash
python -m src.cli movie.srt --from en --to es
```

#### 3. Using Specific Provider
```bash
python -m src.cli movie.srt --provider openai
```

#### 4. Custom Output File
```bash
python -m src.cli movie.srt --output movie_translated.srt
```

#### 5. Complete Translation with All Options
```bash
python -m src.cli movie.srt \
  --provider groq \
  --from en \
  --to pt-br \
  --output movie_pt_br.srt
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
The project includes automatic request rate control:
- **30 requests per minute** by default
- **25 subtitles per batch** for optimization

### Project Structure
```
srt-translator-ai/
├── src/
│   ├── cli.py              # Command line interface
│   ├── config.py           # Configuration and environment variables
│   └── services/
│       ├── srt_parser.py   # SRT file parser
│       └── translator.py   # Translation service
├── pyproject.toml          # Project dependencies and configuration
└── .env                    # Environment variables (create)
```


### Code Structure
- **CLI**: User interface with Typer
- **Parser**: SRT file manipulation
- **Translator**: AI provider integration
- **Config**: Configuration management

## 🐛 Troubleshooting

### Error: "API key not configured"
**Solution**: Check if the `.env` file exists and contains the correct keys.

### Error: "File not found"
**Solution**: Verify that the .srt file path is correct.

### Slow Translation
**Solution**: The project already includes rate limiting. 

### Encoding Issues
**Solution**: Make sure the .srt file is in UTF-8 encoding.

## 📝 .env File Example

```env
# AI API Configuration
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
GROQ_API_KEY=gsk-your-groq-key-here
```

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
