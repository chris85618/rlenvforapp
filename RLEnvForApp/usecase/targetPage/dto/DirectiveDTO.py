from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class DirectiveDTO:
    def __init__(self, url: str, dom: str, form_x_path: str, app_event_dt_os: [
                 AppEventDTO], code_coverage_dt_os: [CodeCoverageDTO]):
        self._url = url
        self._dom = dom
        self._form_x_path = form_x_path
        self._app_event_dt_os = app_event_dt_os
        self._code_coverage_dt_os = code_coverage_dt_os

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_x_path(self) -> str:
        return self._form_x_path

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._app_event_dt_os

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        return self._code_coverage_dt_os
