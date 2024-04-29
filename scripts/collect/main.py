#  By vicvenpet (nano. && ovra.)
#  This script executes tools.py, its function is to collect coins from your accounts.json to a blog.
#  https://github.com/vicvenpet/amino/blob/main/scripts/collect/main.py


from lib.tools import AminoCollector

if __name__ == "__main__":
    colector = AminoCollector()
    colector.start()