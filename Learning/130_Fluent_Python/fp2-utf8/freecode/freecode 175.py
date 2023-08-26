# Example 20-5. Output of flags_threadpool_futures.py

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:
