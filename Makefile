PYTHON=python
PYTEST=pytest
PYLINT=pylint
PYTHONPATH=auth_service/


lint:
	$(PYLINT) $(PYTHONPATH) --verbose