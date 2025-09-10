# main.py
# Example usage for the myglob library

import os
import time
import statistics
from myglob import MyGlobBuilder, MyGlobSearch, MyGlobError

def main():
    print(f"MyGlob lib version: {MyGlobSearch.version()}\n")

    seg = MyGlobBuilder.glob_to_segments(r"file[\d].cs")
    print(f"Segments: {seg}")

    # It's safer to use absolute paths or ensure the script is run from an expected directory.
    # The original Rust code changes the current directory, which can be fragile.
    # Here, we construct paths relative to a base directory if needed, or use absolute paths.
    
    # Example 1:
    # test_myglob(r"S:\**\*Intel*", True, ["d2"], 0, 1)
    # Note: Replace with a path that exists on your system for testing.
    # For example, searching for python files in your user directory:
    # home_dir = os.path.expanduser("~")
    # test_myglob(os.path.join(home_dir, "Documents", "**", "*.py"), True, [], 0, 1)

    # Example 2:
    # test_myglob(r"C:\Temp\search1\info", False, [], 0, 1)
    # Replace with a file or directory that exists.
    
    # Example 3:
    # test_myglob(r"S:\MaxDepth", True, [], 1, 1)
    # Replace with a directory structure to test maxdepth.

    # Example 4 from original code:
    # test_myglob(r"C:\Development\GitVSTS\DevForFun", True, [], 2, 1)
    # Replace with a path on your system. Let's try the Gemini project folder itself.

    # project_path = r"C:\Users\Pierr\Gemini\*Py"
    # print(f"--- Testing in '{project_path}' ---")
    # test_myglob(os.path.join(project_path, "**", "*.py"), True, [], 0, 1)

    #test_myglob(r"C:\Development\Git*\**\Net9\**\launch.json", True, [], 0, 1)
    

def test_myglob(pattern, autorecurse, ignore_dirs, maxdepth, loops):
    durations = []
    for i in range(loops):
        print(f"\nTest #{i+1}")
        
        start_time = time.perf_counter()
        
        try:
            builder = MyGlobBuilder(pattern).set_autorecurse(autorecurse).set_maxdepth(maxdepth)
            for ignore_dir in ignore_dirs:
                builder = builder.add_ignore_dir(ignore_dir)
            
            gs = builder.compile()
            
            print(f"Root: {gs.root}, Segments: {gs.segments}")

            nf = 0
            nd = 0
            for ma in gs.explore():
                if ma.error:
                    print(f"Error: {ma.error}")
                    continue

                if ma.is_file:
                    print(str(ma.path))
                    nf += 1
                elif ma.is_dir:
                    print(f"{ma.path}{os.path.sep}")
                    nd += 1
            
            duration = time.perf_counter() - start_time
            print(f"{nf} file(s) found")
            print(f"{nd} dir(s) found")
            print(f"Iterator search in {duration:.3f}s\n")
            durations.append(duration)

        except MyGlobError as e:
            print(f"Error building MyGlob: {e}")

    if loops > 1:
        print(f"Median time: {statistics.median(durations):.3f}")

if __name__ == "__main__":
    main()
