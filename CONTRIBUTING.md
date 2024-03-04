# Contributing to the project

## Making a package release

To release a new package version:

1.  Update the package's version in `pyproject.toml`:

    ```toml
    [project]
    name = "qase-python-commons"
    version = "2.42.1"
    ```
    
2.  Open & merge a pull request, as usual.
3.  After merging to a stable branch, tag the commit with `qase-{packagename}-{version}`, for example:

    ```sh
    git tag qase-python-commons-2.42.1
    git push --follow-tags
    ```