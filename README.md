# 🤖 Smart Email Reply System Using AI Agents

An intelligent email processing system that automatically classifies, processes, and responds to emails using AI agents. Built specifically for insurance tech companies to streamline customer communication and improve response times.

## 🌟 Features

- **Automated Email Processing**: Fetches unseen emails from Gmail automatically
- **AI-Powered Classification**: Categorizes emails into predefined categories using LLM agents
- **OCR Support**: Extracts and processes text from image and PDF attachments using AWS Textract
- **Intelligent Responses**: Generates contextual replies using AI agents based on email classification
- **Web Dashboard**: Real-time monitoring and management interface
- **Automated Replies**: Sends responses with category-specific attachments
- **Multi-Agent Architecture**: Uses CrewAI framework with specialized agents for different tasks

## 📋 Email Categories

The system classifies emails into the following categories:

- **Policy Inquiries** - New policies, existing policy questions, updates
- **Claims** - Filing claims, status updates, documentation
- **Billing and Payments** - Payment inquiries, billing disputes, confirmations
- **Customer Support** - General inquiries, technical support, complaints
- **Renewals** - Policy renewals, renewal terms, confirmations
- **Documentation** - Document requests, submissions, copies
- **Quotes** - Insurance quotes, follow-ups, quote details
- **Cancellations** - Policy cancellations, cancellation process
- **Compliance and Legal** - Legal correspondence, regulatory updates
- **Marketing and Promotions** - Promotional offers, newsletters
- **Internal Communications** - Internal emails, departmental updates

## 🏗️ System Architecture

```
Smart Email Reply System
├── Email Fetcher (Gmail IMAP)
├── AI Agents (CrewAI)
│   ├── Email Classifier Agent
│   ├── Email Responder Agent
│   ├── Image OCR Summarizer Agent
│   └── PDF Summarizer Agent
├── OCR Processing (AWS Textract)
├── Response Generator
├── Email Sender (SMTP)
└── Web Dashboard (Flask)
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **AI Framework**: CrewAI, LangChain
- **LLM**: Ollama (llama3.1:8b)
- **OCR**: AWS Textract
- **Email**: IMAP/SMTP (Gmail)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: JSON storage

## 📁 Project Structure

```
smart-mail-reply-Using-AI-Agents/
├── src/                          # Source code
│   ├── ai_agents.py             # AI agent definitions
│   ├── app.py                   # Flask web application
│   ├── main.py                  # Main workflow orchestrator
│   ├── email_handler_aug20_1.py # Email processing logic
│   ├── email_sender_with_specific_attach.py # Email sending
│   ├── unseen_count_Info.py     # Email fetching utilities
│   └── templates/               # Web interface templates
├── attachments/                 # Category-specific attachments
├── data/                       # JSON data files
├── handling_attachments/       # Legacy attachment handling
├── config_template.py          # Configuration template
├── requirements.txt            # Python dependencies
├── classes_of_company.txt      # Email category definitions
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gmail account with app-specific password
- AWS account with Textract access
- Ollama with llama3.1:8b model

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sarjil77/smart-mail-reply-Using-AI-Agents.git
   cd smart-mail-reply-Using-AI-Agents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   # Install Ollama (visit https://ollama.ai for instructions)
   ollama pull llama3.1:8b
   ```

4. **Configure the system**
   ```bash
   cp config_template.py config.py
   # Edit config.py with your credentials
   ```

5. **Set up Gmail App Password**
   - Enable 2-factor authentication on your Gmail account
   - Generate an app-specific password
   - Update `config.py` with your credentials

6. **Configure AWS Textract**
   - Set up AWS account and get access keys
   - Update AWS credentials in `config.py`

### Configuration

Edit `config.py` with your settings:

```python
# Email Configuration
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_specific_password"

# AWS Configuration
AWS_ACCESS_KEY_ID = "your_aws_access_key"
AWS_SECRET_ACCESS_KEY = "your_aws_secret_key"
AWS_REGION = "us-east-1"

# AI Model
AI_MODEL = "llama3.1:8b"
```

## 🎯 Usage

### 1. Start the Web Dashboard

```bash
cd src
python app.py
```

Visit `http://localhost:5000` to access the dashboard.

### 2. Run the Email Processing Workflow

```bash
cd src
python main.py
```

Or use the "Run Email Workflow" button in the web dashboard.

### 3. Manual Email Fetching

```bash
cd src
python unseen_count_Info.py
```

## 🔧 API Endpoints

The system provides several REST API endpoints:

- `GET /api/dashboard-data` - Get dashboard statistics
- `GET /api/emails` - Get paginated email list
- `GET /api/email/<id>` - Get specific email details
- `GET /api/response-details` - Get response details
- `POST /api/fetch-unseen-emails` - Fetch new emails
- `POST /api/run-main` - Execute main workflow

## 🤖 AI Agents

### Email Classifier Agent
- **Role**: Categorizes incoming emails
- **Goal**: Accurately classify emails into predefined categories
- **Output**: Category classification

### Email Responder Agent
- **Role**: Generates appropriate responses
- **Goal**: Create contextual and helpful replies
- **Output**: Email response content

### Image OCR Summarizer Agent
- **Role**: Processes image attachments
- **Goal**: Extract and summarize text from images
- **Output**: Concise summary of image content

### PDF Summarizer Agent
- **Role**: Processes PDF attachments
- **Goal**: Extract and summarize PDF content
- **Output**: Concise summary of PDF content

## 📊 Dashboard Features

- **Real-time Statistics**: Unseen emails, pending responses, completion rates
- **Email Management**: View, filter, and search emails
- **Response Monitoring**: Track AI-generated responses
- **Workflow Control**: Start/stop email processing
- **Error Logging**: Monitor system errors and issues

## 🔒 Security Considerations

- Use app-specific passwords for Gmail
- Store sensitive credentials in environment variables
- Implement proper access controls for the web dashboard
- Regularly rotate AWS access keys
- Monitor email processing logs for suspicious activity

## 🛠️ Customization

### Adding New Email Categories

1. Update `classes_of_company.txt`
2. Modify the AI agent prompts in `ai_agents.py`
3. Add category-specific attachments
4. Update the web interface accordingly

### Changing AI Models

1. Update `config.py` with new model name
2. Ensure the model is available in Ollama
3. Adjust agent prompts if necessary

### Custom Attachment Processing

1. Extend the OCR processing functions
2. Add new agent types for specific document types
3. Implement custom parsing logic

## 🐛 Troubleshooting

### Common Issues

1. **Gmail Authentication Errors**
   - Ensure 2FA is enabled
   - Use app-specific password, not regular password
   - Check IMAP is enabled in Gmail settings

2. **AWS Textract Errors**
   - Verify AWS credentials and permissions
   - Check AWS region configuration
   - Ensure Textract service is available in your region

3. **Ollama Connection Issues**
   - Verify Ollama is running: `ollama list`
   - Check model availability: `ollama pull llama3.1:8b`
   - Restart Ollama service if needed

4. **Web Dashboard Not Loading**
   - Check Flask is running on correct port
   - Verify no other services are using port 5000
   - Check browser console for JavaScript errors

## 📈 Performance Optimization

- **Batch Processing**: Process multiple emails simultaneously
- **Caching**: Implement response caching for similar emails
- **Database**: Consider moving from JSON to proper database
- **Async Processing**: Implement asynchronous email processing
- **Model Optimization**: Fine-tune AI models for your specific use case

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [Ollama](https://ollama.ai) for local LLM deployment
- [AWS Textract](https://aws.amazon.com/textract/) for OCR capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search [existing issues](https://github.com/sarjil77/smart-mail-reply-Using-AI-Agents/issues)
3. Create a [new issue](https://github.com/sarjil77/smart-mail-reply-Using-AI-Agents/issues/new) with detailed information

## 🔮 Roadmap

- [ ] Support for additional email providers (Outlook, Yahoo)
- [ ] Machine learning model fine-tuning
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Integration with CRM systems
- [ ] Mobile application
- [ ] Advanced security features (OAuth2, SSO)

---

**Made with ❤️ for automating customer communication in insurance tech**