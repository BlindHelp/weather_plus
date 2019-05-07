for %%i in (*.pyc,*.pyo,*.nvda-addon) do if not "%%i"=="oauth.pyc" if not "%%i"=="oauth.pyo" del /S "%%i"

scons -c && scons pot && scons && pause