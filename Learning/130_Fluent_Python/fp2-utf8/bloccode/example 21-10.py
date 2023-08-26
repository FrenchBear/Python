# Example 21-10. Lines to use instead of await asyncio.to_thread

        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, save_flag,
                             image, f'{cc}.gif')
