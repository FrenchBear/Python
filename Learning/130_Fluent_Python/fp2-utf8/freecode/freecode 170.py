try:
    dangerous_call()
    after_call()
except OSError:
    log('OSError...')
