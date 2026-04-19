from misago import MisagoPlugin


manifest = MisagoPlugin(
    name="Dev Warning",
    description=(
        "Displays a warning message below the site navbar about using code "
        "from the main repository for live sites or evaluation purposes."
    ),
    license="GNU GPL v2",
    icon="fa fa-exclamation-triangle",
    color="#f97316",
    version="1.0",
    author="Rafał Pitoń",
    homepage="https://misago-project.org",
    sponsor="https://github.com/sponsors/rafalp",
    help="https://misago-project.org/c/support/30/",
    bugs="https://misago-project.org/c/bug-reports/29/",
    repo="https://github.com/rafalp/misago",
)
