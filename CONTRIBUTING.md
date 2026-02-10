# Contributing to AutoMate Studio

First off, thank you for considering contributing to AutoMate Studio! 🎉

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com].

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and helpful
- **Be professional** in all interactions
- **Accept constructive criticism** gracefully
- **Focus on what is best** for the community

---

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When submitting a bug report, include:**

- **Clear title** - Descriptive summary of the issue
- **Steps to reproduce** - Exact steps to trigger the bug
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - OS, Python version, Node version, etc.
- **Logs** - Relevant error messages or stack traces
- **Screenshots** - If applicable

**Template:**

```markdown
## Bug Description
A clear description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: Windows 11
- Python: 3.12.1
- Node: 18.17.0
- Browser: Chrome 120

## Logs
```
Paste error logs here
```

## Screenshots
If applicable
```

---

### Suggesting Features

Feature requests are welcome! Please provide:

- **Clear use case** - Why is this feature needed?
- **Expected behavior** - How should it work?
- **Alternatives** - Have you considered other solutions?
- **Additional context** - Any other relevant information

---

### Code Contributions

We love pull requests! Here's the process:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

---

## 🛠️ Development Setup

### Prerequisites

```powershell
# Required software
- Python 3.12+
- Node.js 18+
- uv (Python package manager)
- Git
```

### Initial Setup

```powershell
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/automate-studio.git
cd automate-studio

# 2. Create a branch
git checkout -b feature/your-feature-name

# 3. Install dependencies
uv sync
cd web && npm install && cd ..

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Start development servers
.\start_fullstack.ps1
```

### Project Structure

```
autoMate/
├── api_server.py          # FastAPI backend
├── graph.py               # LangGraph workflow
├── RAG/                   # RAG pipeline
└── web/                   # Next.js frontend
```

---

## 📝 Coding Standards

### Python Code

Follow **PEP 8** style guide:

```python
# Good
def analyze_documents(files: List[UploadFile]) -> Dict[str, Any]:
    """
    Analyzes uploaded documents and extracts automation opportunities.
    
    Args:
        files: List of uploaded files
        
    Returns:
        Dictionary containing analysis results
    """
    results = []
    for file in files:
        result = process_file(file)
        results.append(result)
    return {"opportunities": results}

# Bad
def analyze(f):
    r=[]
    for x in f:
        r.append(process(x))
    return r
```

**Key Points:**
- Use **type hints** for all functions
- Add **docstrings** to all public functions
- Use **descriptive variable names**
- Keep functions **small and focused**
- Follow **4-space indentation**
- Limit lines to **88 characters** (Black formatter)

### TypeScript Code

Follow **Airbnb TypeScript Style Guide**:

```typescript
// Good
interface OpportunityProps {
  title: string;
  priorityScore: number;
  department: string;
}

export const OpportunityCard: React.FC<OpportunityProps> = ({
  title,
  priorityScore,
  department,
}) => {
  return (
    <div className="rounded-lg bg-white/5 p-6">
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="text-sm text-gray-400">{department}</p>
    </div>
  );
};

// Bad
export const Card = (props:any) => (
  <div>
    <h3>{props.t}</h3>
    <p>{props.d}</p>
  </div>
)
```

**Key Points:**
- Use **TypeScript** for all components
- Add **proper interfaces** for props
- Use **functional components** with hooks
- Follow **React best practices**
- Use **Tailwind CSS** for styling
- Keep components **small and reusable**

---

## 📬 Commit Guidelines

We follow **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good commits
feat(rag): add document chunking with tiktoken
fix(api): resolve CORS error for localhost:3000
docs(readme): update installation instructions
refactor(graph): simplify opportunity extraction logic

# Bad commits
update stuff
fix bug
changes
wip
```

### Commit Message Rules

- Use **present tense** ("add feature" not "added feature")
- Use **imperative mood** ("move cursor to..." not "moves cursor to...")
- First line **max 72 characters**
- Reference **issue numbers** when applicable

```bash
feat(workflow): add n8n deployment endpoint

Implements direct workflow deployment to n8n cloud instances.
Includes error handling for API failures and connection issues.

Closes #42
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md**
5. **Rebase on latest main**

### PR Checklist

```markdown
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No merge conflicts
- [ ] CHANGELOG.md updated
```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe testing process

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added
- [ ] Documentation updated
```

### Review Process

- Maintainers will review within **48 hours**
- Address **all review comments**
- Once approved, maintainer will **merge**
- **Squash merge** for clean history

---

## 🧪 Testing

### Python Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_rag.py
```

### Frontend Tests

```powershell
cd web

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

---

## 📚 Resources

### Learning Materials

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [LangChain Docs](https://python.langchain.com/)
- [Next.js Learn](https://nextjs.org/learn)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

### Tools

- **Linting**: `black`, `flake8`, `eslint`
- **Formatting**: `prettier`, `black`
- **Type Checking**: `mypy`, `tsc`

---

## ❓ Questions?

- 💬 Open a [GitHub Discussion](https://github.com/your-username/automate-studio/discussions)
- 🐛 Report bugs via [GitHub Issues](https://github.com/your-username/automate-studio/issues)
- 📧 Email: your-email@example.com

---

**Thank you for contributing to AutoMate Studio!** 🚀

Every contribution, no matter how small, is valuable and appreciated.

---

*Happy Coding!* 💻✨
