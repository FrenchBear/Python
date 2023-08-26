try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()
