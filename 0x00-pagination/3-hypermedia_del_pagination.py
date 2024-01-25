#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict

def index_range(index: int, page_size: int) -> Dict:
    """
    Return a dictionary with information about the current start index and next index.

    Args:
        index (int): The current start index of the return page.
        page_size (int): The number of items per page.

    Returns:
        Dict: A dictionary containing index information.
    """
    next_index = index + page_size
    return {"index": index, "next_index": next_index, "page_size": page_size}

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Get hypermedia information for a given index and page_size.

        Args:
            index (int): The current start index of the return page. Default is None.
            page_size (int): The number of items per page. Default is 10.

        Returns:
            Dict: Hypermedia information containing index, next index, page size, and data.
        """
        assert index is None or (isinstance(index, int) and 0 <= index < len(self.indexed_dataset())), "Index must be in a valid range."
        assert isinstance(page_size, int) and page_size > 0, "Page size must be a positive integer."

        if index is None:
            index = 0

        page_data = [self.indexed_dataset().get(i, []) for i in range(index, index + page_size)]
        next_index = index + page_size

        hypermedia_info = {
            "index": index,
            "next_index": next_index,
            "page_size": page_size,
            "data": page_data,
        }

        return hypermedia_info
