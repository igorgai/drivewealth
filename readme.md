# Summary
Provides a Pythonic wrapper around the DriveWealth REST API (documentation located at http://developer.drivewealth.com/docs).

## 

# Run all tests (unit and integration)
First, update pytest.ini with the DriveWealth username and password.
```
addopts = --durations=3 --username=DRIVEWEALTH_USERNAME --password=DRIVEWEALTH_PASSWORD
```

Then, run the following command:
```
python setup.py test
```

## Colophon
- [Marshmallow](https://marshmallow.readthedocs.org/)
- [pytest](http://pytest.org/)
- [hammock](https://github.com/kadirpekel/hammock)
- [cachetools](http://pythonhosted.org/cachetools/)
