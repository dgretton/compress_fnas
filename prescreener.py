import os
from construct_filters import FILTER_NAME

class Prescreener:
    MAX_BATCH_SIZE = 2000

    def __init__(self):
        self.filters = None

    def prescreen(self, query_iter):
        query_iter = iter(query_iter)
        def positives():
            query_batch = None
            while query_batch is None or query_batch:
                query_batch = [q for _, q in zip(range(self.MAX_BATCH_SIZE), query_iter)]
                for positive in self.prescreen_list(query_batch):
                    yield positive
        return positives()

    def prescreen_list(self, query_list):
        self._load_filters()
        present = set()
        query_set = set(query_list)
        for custom_filter in self.filters:
            present.update(query_set.intersection(custom_filter))
        return present
            
    def _load_filters(self):
        if self.filters is None:
            self.filters = []
            for filter_dir in filter(os.path.isdir, os.listdir('.')): # only directories
                try:
                    with open(os.path.join(filter_dir, FILTER_NAME)) as filter_file:
                        custom_filter = set(filter_file.read().split()) # will just be a set of strings for now
                        self.filters.append(custom_filter)
                except FileNotFoundError:
                    pass

if __name__ == '__main__':
    prescreener = Prescreener()
    print(list(prescreener.prescreen(['YAPLHLKEVMLPTGELLTD', 'MDPGNGGWHSGTMRORIGK', 'AAAAAAAAAAAAAAAAAAA'])))
