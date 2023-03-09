from kernel4 import IDSearcher
import sqlite3
from multiprocessing import Pool

def main():
    anon1 = IDSearcher()
    l = anon1.search_ids(1, 928)
    print(l)
    # anon1.save_to_file(f)

if __name__ == "__main__":
    main()
