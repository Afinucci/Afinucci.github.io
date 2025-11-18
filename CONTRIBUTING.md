# Contributing to WWS Inventory Platform

Thank you for your interest in contributing to the WWS Inventory Platform! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- Git

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Afinucci.github.io.git
   cd Afinucci.github.io
   ```

3. Set up environment:
   ```bash
   make setup
   # Edit .env with your configuration
   ```

4. Start services:
   ```bash
   make start
   ```

5. Verify everything works:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/docs

## Development Workflow

### Branch Naming

- `feature/` - New features (e.g., `feature/ai-chat-interface`)
- `fix/` - Bug fixes (e.g., `fix/inventory-count-error`)
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Detailed explanation if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(inventory): add bulk import feature`
- `fix(api): resolve authentication timeout issue`
- `docs(readme): update installation instructions`

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 100 characters
- Use Black for formatting:
  ```bash
  black backend/
  ```

- Use flake8 for linting:
  ```bash
  flake8 backend/
  ```

### TypeScript/React (Frontend)

- Follow TypeScript best practices
- Use functional components with hooks
- Maximum line length: 100 characters
- Use Prettier for formatting:
  ```bash
  cd frontend && npm run format
  ```

### General Guidelines

1. **Write Clear Code**: Code should be self-documenting
2. **Add Comments**: Explain why, not what
3. **Keep Functions Small**: One function, one responsibility
4. **Error Handling**: Always handle errors appropriately
5. **Security**: Never commit secrets or API keys

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Writing Tests

- Write tests for all new features
- Maintain minimum 80% code coverage
- Include edge cases and error scenarios
- Use descriptive test names

Example (Python):
```python
def test_create_product_with_valid_data():
    """Test product creation with valid data"""
    # Arrange
    product_data = {...}

    # Act
    result = create_product(product_data)

    # Assert
    assert result.status_code == 201
    assert result.json()["name"] == product_data["name"]
```

## Pull Request Process

### Before Submitting

1. **Update from main**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run tests**:
   ```bash
   make test
   ```

3. **Format code**:
   ```bash
   cd backend && black .
   cd frontend && npm run format
   ```

4. **Update documentation** if needed

### PR Checklist

- [ ] Tests pass locally
- [ ] Code is formatted properly
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] PR description explains changes
- [ ] Related issues referenced

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested these changes

## Screenshots (if applicable)

## Related Issues
Fixes #123
```

### Review Process

1. Automated checks must pass (CI/CD)
2. At least one maintainer approval required
3. All conversations must be resolved
4. Keep PRs focused and small when possible

## Project Structure

```
.
├── frontend/          # Next.js frontend
├── backend/           # FastAPI backend
├── ai-engine/         # AI/ML components
├── infrastructure/    # IaC and deployment
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

## Key Technologies

### Frontend
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Shadcn/ui

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

### AI/ML
- LangChain
- OpenAI GPT-4
- Anthropic Claude

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an issue with the bug template
- **Features**: Create an issue with the feature template
- **Chat**: Join our Discord (coming soon)

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Annual contributor highlights

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to making inventory management better for SMEs! 🚀
