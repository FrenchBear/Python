def download_many(cc_list: list[str]) -> int:
    with futures.ProcessPoolExecutor() as executor:
