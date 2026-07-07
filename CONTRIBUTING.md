# Contributing to BioNexus AI

Thank you for your interest in contributing to BioNexus AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Set up development environment (see README.md)
5. Make your changes
6. Write/update tests
7. Ensure all tests pass
8. Commit with clear messages: `git commit -m 'Add feature: description'`
9. Push to your fork
10. Create a Pull Request

## Code Standards

### Python
- Follow PEP 8
- Use type hints
- Format with Black
- Lint with Flake8
- Run: `black . && flake8 .`

### TypeScript/JavaScript
- Use ESLint + Prettier
- Strict TypeScript mode
- No `any` types
- Run: `prettier --write . && eslint .`

## Testing

- Write unit tests for all new features
- Aim for >80% code coverage
- Backend: `pytest`
- Frontend: `npm test`
- E2E: `npx playwright test`

## Commit Messages

Use conventional commits:
- `feat: add feature`
- `fix: fix bug`
- `docs: update documentation`
- `test: add tests`
- `chore: maintenance`
- `refactor: refactor code`

## Pull Request Process

1. Update README.md if needed
2. Update documentation
3. Ensure all CI/CD checks pass
4. Request review from maintainers
5. Address review feedback
6. Merge after approval

## Reporting Issues

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Screenshots/logs if applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
