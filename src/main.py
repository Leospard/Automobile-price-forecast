from multiprocessing import Pool
from crap import get_html, get_json, run
import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    pool = Pool(4)
    for i in range(42703015, 42800000):
        pool.apply_async(run, (i, ))
    pool.close()
    pool.join()
