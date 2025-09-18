# Contributing to Smart Email Reply System

Thank you for your interest in contributing to the Smart Email Reply System! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features and improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Improve documentation and examples
- **Testing**: Help with testing and quality assurance

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/smart-mail-reply-Using-AI-Agents.git
   cd smart-mail-reply-Using-AI-Agents
   ```
3. **Set up the development environment**:
   ```bash
   ./setup.sh
   ```
4. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Ollama with llama3.1:8b model
- Gmail account with app-specific password
- AWS account with Textract access

### Installation
Follow the setup instructions in the README.md file.

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate

### Code Example
```python
def process_email(email_content: str) -> dict:
    """
    Process an email and return classification result.
    
    Args:
        email_content (str): The content of the email to process
        
    Returns:
        dict: Classification result with category and confidence
    """
    # Implementation here
    pass
```

### File Organization
- Keep related functionality in separate modules
- Use clear, descriptive filenames
- Follow the existing project structure

## 🧪 Testing

- Write tests for new features
- Ensure existing tests pass
- Test with different email formats and attachments
- Verify AI agent responses are appropriate

### Running Tests
```bash
cd src
python -m pytest tests/
```

## 📖 Documentation

- Update README.md for new features
- Add docstrings to all new functions
- Include examples in your documentation
- Update configuration templates if needed

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the bug
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, dependencies
6. **Logs**: Relevant error messages or logs

### Bug Report Template
```markdown
**Bug Description**
A clear and concise description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.9.0]
- Dependencies: [relevant package versions]

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

For feature requests, please include:

1. **Problem**: What problem does this solve?
2. **Solution**: Describe your proposed solution
3. **Alternatives**: Alternative solutions you've considered
4. **Impact**: Who would benefit from this feature?

## 🔀 Pull Request Process

1. **Update your fork** with the latest changes:
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following the coding standards

4. **Test your changes** thoroughly

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes
- **Breaking Changes**: Note any breaking changes

### Commit Message Format
```
Type: Brief description

Detailed explanation of changes if necessary.

- Use imperative mood ("Add feature" not "Added feature")
- Capitalize the first letter
- No period at the end of the subject line
- Types: Add, Fix, Update, Remove, Refactor, Test, Doc
```

## 🔍 Code Review Process

1. All pull requests require review
2. Address feedback promptly
3. Keep discussions constructive and respectful
4. Be open to suggestions and improvements

## 🚫 What Not to Include

- Sensitive credentials or API keys
- Large binary files
- Generated files (logs, compiled code)
- Personal configuration files
- Temporary or test files

## 📋 Development Checklist

Before submitting a pull request:

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added for new features
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No sensitive information included
- [ ] Commit messages are clear
- [ ] Feature tested manually

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks in documentation

## 📞 Getting Help

If you need help:

1. Check existing issues and documentation
2. Ask questions in GitHub Discussions
3. Join our community chat (if available)
4. Tag maintainers in issues (@sarjil77)

## 📜 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone.

### Expected Behavior
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior
- Harassment, discrimination, or offensive comments
- Trolling or insulting behavior
- Personal or political attacks
- Publishing private information without permission

Thank you for contributing to the Smart Email Reply System! 🎉