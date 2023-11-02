# Example 20-15. flags2_sequential.py: the sequential implementation of download_many

def download_many(cc_list: list[str], base_url: str, verbose: bool,
                  _unused_concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose)
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR
        counter[status] += 1
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter
