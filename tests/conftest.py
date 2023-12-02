import pytest

# https://github.com/pytest-dev/pytest-html/blob/master/docs/user_guide.rst#modifying-the-results-table

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>AAA</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<tr>{report.description}</tr>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
