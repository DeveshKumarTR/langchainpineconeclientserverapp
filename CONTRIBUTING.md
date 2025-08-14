# Contributing to LangChain Pinecone Vector Database Application

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### 1. Fork the Repository
Fork the repository on GitHub and clone your fork locally.

### 2. Set Up Development Environment
```bash
# Clone your fork
git clone https://github.com/your-username/langchainpineconeclientserverapp.git
cd langchainpineconeclientserverapp

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Create a Branch
Create a new branch for your feature or bug fix:
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- Write clear, concise code
- Follow existing code style and conventions
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run tests
pytest tests/

# Test the server
python test_setup.py

# Manual testing
python server/app.py  # In one terminal
python client/client.py  # In another terminal
```

### 6. Commit and Push
```bash
git add .
git commit -m "Add: Brief description of your changes"
git push origin feature/your-feature-name
```

### 7. Create a Pull Request
Submit a pull request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots or examples if applicable

## Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed

## Types of Contributions

### Bug Reports
- Use the issue template
- Include steps to reproduce
- Provide error messages and logs
- Specify environment details

### Feature Requests
- Describe the problem you're solving
- Explain your proposed solution
- Consider backwards compatibility

### Code Contributions
- New features and enhancements
- Bug fixes
- Performance improvements
- Documentation updates
- Test improvements

## Development Guidelines

### Adding New Document Loaders
When adding support for new file types:
1. Update `server/routes/documents.py`
2. Add the file extension to `ALLOWED_EXTENSIONS` in config
3. Implement the loader in `load_document()` function
4. Add tests in `tests/test_server.py`
5. Update documentation

### Adding New API Endpoints
1. Create the endpoint in appropriate route file
2. Add corresponding client method
3. Update API documentation in README
4. Add comprehensive tests
5. Update examples if needed

### Database/Vector Store Changes
1. Update `server/models/vector_store.py`
2. Consider migration scripts if needed
3. Update configuration if new settings required
4. Test with different data sizes
5. Update performance documentation

## Testing

### Unit Tests
- Write tests for all new functions
- Test edge cases and error conditions
- Use meaningful test names
- Mock external dependencies

### Integration Tests
- Test API endpoints end-to-end
- Verify client-server communication
- Test with real file uploads (small test files)

### Manual Testing
- Test the interactive client
- Verify documentation examples work
- Test with different file types and sizes

## Documentation

### Code Documentation
- Add docstrings to all public functions
- Include parameter types and return values
- Add usage examples for complex functions

### User Documentation
- Update README.md for new features
- Add examples to examples/README.md
- Update INSTALL.md if setup changes
- Keep API documentation current

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on implementation details
- Discussion of proposed changes

Thank you for contributing! 🎉
