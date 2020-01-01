import concurrent.futures
from tqdm.auto import tqdm

def async_run(f, my_iter):
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(tqdm(executor.map(f, my_iter), total=len(my_iter)))

    return results
