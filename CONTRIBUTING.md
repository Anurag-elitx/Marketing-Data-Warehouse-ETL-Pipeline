# Contributing to Marketing ETL Pipeline

Thank you for your interest in contributing to this project!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Anurag-elitx/Marketing-Data-Warehouse-ETL-Pipeline.git
   cd Marketing-Data-Warehouse-ETL-Pipeline
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run the test suite with pytest:
```bash
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ -v --cov=src --cov-report=html
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass
4. Update documentation as needed
5. Submit a pull request with a clear description

## Reporting Issues

Please use GitHub Issues to report bugs or request features.
Include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and environment details
