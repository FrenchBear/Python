REM check all python learning projects with mypy
REM 2022-03-03 PV

cd C:\Development\GitHub\Python\Learning
for /d %%f in (*.*) DO (
  pushd %%f
  mypy .
  popd
)