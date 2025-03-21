.PHONY: clean install test

# Install the package
install:
	pip3 install . --break-system-packages

# Run tests
test:
	pytest tests/

# Clean up build artifacts
clean:
	rm -rf */build/
	rm -rf */.pytest_cache/
	rm -rf */dist/
	rm -rf */input/
	rm -rf */output/
	find . -name "*.egg-info" -type d -exec rm -rf {} +
	find . -name "stage" -type d -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.zip" -delete