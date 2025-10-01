# LLM Profile Agent 🤖

> An AI-powered professional profile assistant built with Mistral AI and Streamlit

This agent serves as an interactive representation of **Julien Vaughan's** professional profile, providing dynamic responses to career-related inquiries in both English and French. Built with deterministic response generation and strict profile adherence.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Mistral](https://img.shields.io/badge/Mistral%20AI-API-purple.svg)
![License](https://img.shields.io/badge/License-Custom-green.svg)

## ✨ Features

- **Bilingual Interaction**
  - Automatic language detection (🇬🇧 English / 🇫🇷 French)
  - Context-aware responses in the detected language
  - Language-specific conversation style

- **Smart Response System**
  - Profile-driven answers (no hallucination)
  - Short/Long response modes
  - Deterministic output with profile enforcement

- **Professional UI**
  - Interactive Streamlit interface
  - Curated example questions
  - Real-time conversation history
  - Downloadable chat transcripts

- **Enterprise-Ready**
  - Rate limiting with exponential backoff
  - Environment-aware configuration
  - Production-ready deployment options

## 🚀 Quick Start

1. **Clone & Install:**
   ```bash
   git clone https://github.com/username/llm-profile-agent.git
   cd llm-profile-agent
   pip install -e .
   ```

2. **Configure API:**
   ```bash
   # Create .env file in project root
   echo MISTRAL_API_KEY=your_api_key_here > .env
   ```

3. **Launch:**
   ```bash
   streamlit run web/app.py
   ```

## 🏗️ Project Structure

```
llm-profile-agent/
├── data/                          # Data files
│   └── profile.json               # Professional profile
├── src/                          # Core logic
│   ├── agent.py                  # Main agent implementation
│   ├── llm_wrapper.py           # Mistral API interface
│   ├── profile_loader.py        # Configuration management
│   └── utils.py                 # Helper functions
├── web/                          # Web interface
│   ├── app.py                   # Streamlit application
│   └── components.py            # UI components
└── pyproject.toml               # Project configuration
```

## 💻 Development

### Requirements
- Python 3.8+
- Mistral AI API key
- Dependencies listed in `pyproject.toml`

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -e ".[dev]"
```

### Code Style
The project follows:
- Black formatter (88 char line length)
- PEP 8 guidelines
- Type hints for core functions

## 🚀 Deployment

The application supports multiple deployment options:

- **Local Development:**
  - Uses `.env` for configuration
  - Direct Streamlit launch

- **Streamlit Cloud:**
  - Configure secrets in dashboard
  - Automatic deployment from GitHub

- **Custom Server:**
  - Environment variable configuration
  - Supports reverse proxy setup

## 🔒 Security

- Profile enforcement prevents unauthorized modifications
- Rate limiting protects against API abuse
- No sensitive data stored in session state
- Environment-aware configuration loading

## 📜 License

This project is for educational and demonstration purposes.  
Contact [Julien Vaughan](https://www.linkedin.com/in/julien-vaughan/) for professional use or collaboration.

## 🤝 Contributing

While this is a personal profile project, suggestions for improvements are welcome:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

Built with ❤️ using Streamlit and Mistral AI
