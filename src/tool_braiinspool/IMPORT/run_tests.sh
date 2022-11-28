# https://docs.pytest.org/en/latest/explanation/goodpractices.html#test-discovery

# -s is becuase we read from standard input during the test

PYTHONPATH=src pytest -s
