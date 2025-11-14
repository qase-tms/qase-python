# flake8: noqa

if __import__("typing").TYPE_CHECKING:
    # import apis into api package
    from qase.api_client_v2.api.custom_fields_api import CustomFieldsApi
    from qase.api_client_v2.api.results_api import ResultsApi
    
else:
    from lazy_imports import LazyModule, as_package, load

    load(
        LazyModule(
            *as_package(__file__),
            """# import apis into api package
from qase.api_client_v2.api.custom_fields_api import CustomFieldsApi
from qase.api_client_v2.api.results_api import ResultsApi

""",
            name=__name__,
            doc=__doc__,
        )
    )
