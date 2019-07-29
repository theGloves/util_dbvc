import fire
from dbvc import Db_vc

def main():
    vc = Db_vc()
    fire.Fire(vc)

if __name__ == "__main__":
    main()