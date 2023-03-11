# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from qaseio.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    ATTACHMENT = "/attachment"
    ATTACHMENT_CODE = "/attachment/{code}"
    ATTACHMENT_HASH = "/attachment/{hash}"
    AUTHOR = "/author"
    AUTHOR_ID = "/author/{id}"
    CASE_CODE = "/case/{code}"
    CASE_CODE_ID = "/case/{code}/{id}"
    CUSTOM_FIELD = "/custom_field"
    CUSTOM_FIELD_ID = "/custom_field/{id}"
    DEFECT_CODE = "/defect/{code}"
    DEFECT_CODE_ID = "/defect/{code}/{id}"
    DEFECT_CODE_RESOLVE_ID = "/defect/{code}/resolve/{id}"
    DEFECT_CODE_STATUS_ID = "/defect/{code}/status/{id}"
    ENVIRONMENT_CODE = "/environment/{code}"
    ENVIRONMENT_CODE_ID = "/environment/{code}/{id}"
    MILESTONE_CODE = "/milestone/{code}"
    MILESTONE_CODE_ID = "/milestone/{code}/{id}"
    PLAN_CODE = "/plan/{code}"
    PLAN_CODE_ID = "/plan/{code}/{id}"
    PROJECT = "/project"
    PROJECT_CODE = "/project/{code}"
    PROJECT_CODE_ACCESS = "/project/{code}/access"
    RESULT_CODE = "/result/{code}"
    RESULT_CODE_ID = "/result/{code}/{id}"
    RESULT_CODE_HASH = "/result/{code}/{hash}"
    RESULT_CODE_ID_BULK = "/result/{code}/{id}/bulk"
    RESULT_CODE_ID_HASH = "/result/{code}/{id}/{hash}"
    RUN_CODE = "/run/{code}"
    RUN_CODE_ID = "/run/{code}/{id}"
    RUN_CODE_ID_PUBLIC = "/run/{code}/{id}/public"
    RUN_CODE_ID_COMPLETE = "/run/{code}/{id}/complete"
    SEARCH = "/search"
    SHARED_STEP_CODE = "/shared_step/{code}"
    SHARED_STEP_CODE_HASH = "/shared_step/{code}/{hash}"
    SUITE_CODE = "/suite/{code}"
    SUITE_CODE_ID = "/suite/{code}/{id}"
