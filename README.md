# 🚀 AstroNotes

### [🔗 Live Demo](https://www.example.com)

AstroNotes is a powerful Streamlit application designed to transform messy class notes into well-organized, polished documents. Using advanced AI technology, it helps students and professionals enhance their notes with smart formatting, content improvements, and customizable styling options.

## 🌟 Features

### Note Formatting
- **Multiple Format Options**:
  - Bullet Points (recommended)
  - Paragraphs
  - Original Format Preservation
- **Styling Choices**:
  - Understandable (casual)
  - Formal (professional)
- **Output Options**:
  - Markdown
  - Plain Text
- **Optional Emoji Enhancement** 🎯

### Content Enhancement
- ✅ Automatic factual error correction
- 📝 Smart example addition
- 🔄 Duplicate content removal
- 🎯 Irrelevant content filtering

### Personalization
- Custom name addition
- Date stamping
- PDF export capabilities (coming soon)

## 🛠 Technical Stack

### Core Dependencies
```bash
python>=3.7
streamlit
streamlit-lottie
streamlit-pdf-viewer
reportlab
openai
markdown2
```

### API Requirements
- OpenAI API key (GPT-40 mini access required)

## 📁 Project Structure

```
astronotes/
├── streamlit_app.py
├── static/
│   ├── images/
│   │   └── favicon.png
│   ├── lottie/
│   │   └── rocket_loader.json
│   └── prompt/
│       └── build_prompt.json
└── cache/
    └── [generated PDFs]
```

## 🚀 Getting Started

### Prerequisites
1. Python 3.7 or higher
2. OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/astronotes.git
cd astronotes
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create a .streamlit/secrets.toml file
[API_KEYS]
OPENAI_API_KEY = <your_openai_api_key-here>
```

4. Run the application:
```bash
streamlit run streamlit_app.py
```

## 💡 Usage

1. **Launch**: Click "Get Started" on the home screen
2. **Input**: 
   - Paste your notes (minimum 100 characters)
   - Configure formatting options
   - Add optional personalization
3. **Generate**: Click "Perfect My Notes"
4. **Review**: View your enhanced notes in the output screen

## 🔧 Configuration Options

### Note Types
- **Bullet Points**: Organizes content into clear, hierarchical bullet points
- **Paragraphs**: Structures content into flowing paragraphs
- **Preserve Original**: Maintains the original note format while enhancing content

### Style Options
- **Understandable**: Casual, easy-to-read format
- **Formal**: Professional, academic styling

### Content Enhancement Options
- **Correct Factual Errors**: AI-powered fact-checking
- **Add Examples**: Automatic example insertion
- **Remove Duplicates**: Redundancy elimination
- **Remove Irrelevant Content**: Focus maintenance

## 🔄 State Management

The application uses Streamlit's session state to manage four main screens:
- `home`: Welcome screen
- `input`: Note input and configuration
- `generate`: Processing screen with animation
- `output`: Results display

## 🚧 Future Enhancements

- See the [TODO.md](TODO.md) file for a list of upcoming features and improvements

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

* **beck-1888** - *Initial work*

## 🙏 Acknowledgments

* OpenAI for GPT-4o Mini API
* LottieFiles for the animated loader
* Streamlit team for the amazing framework
* Contributors and testers

## 📮 Contact

For support or queries, please open an issue in the GitHub repository.

---

Made with ❤️ by [Beck O.](https://github.com/beck1888)