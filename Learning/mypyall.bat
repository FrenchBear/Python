for /D %%d in (*.*) do (
	pushd %%d
	mypy .
	popd
)