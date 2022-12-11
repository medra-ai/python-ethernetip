import nox

@nox.session()
def lint(session):
    session.install("flake8")
    session.run("flake8", "src/ethernetip/ethernetip.py")

@nox.session(python=["3.7","3.9"])
def tests(session):
    session.install(".")
    session.install("pytest", "pytest-cov")
    tests = session.posargs or ["tests/"]
    session.run("pytest",
            "--cov=ethernetip",
            "--cov-report=html:coverage-reports/" + session.python,
            *tests,
            env={"COVERAGE_FILE": f".coverage.{session.python}"},
            )
    session.notify("coverage")

@nox.session
def coverage(session):
    session.install("coverage[toml]")
    try:
        session.run("coverage", "combine")
    except:
        pass
    session.run("coverage", "report")

@nox.session(reuse_venv=True)
def docs(session):
    session.install(".")
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source", "build/docs")
