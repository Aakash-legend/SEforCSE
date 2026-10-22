from collections import deque
class QueueManager:
    def __init__(self):
        self.queue = deque()
        self.visited = set()
    def add_url(self, item):
        url, _ = item
        queued_urls = {u for u, _ in self.queue}
        if url not in self.visited and url not in queued_urls:
            self.queue.append(item)
    def get_next_url(self):
        if self.queue:
            return self.queue.popleft()
        return None
    def mark_visited(self, url):
        self.visited.add(url)
    def is_visited(self, url):
        return url in self.visited
    def queue_size(self):
        return len(self.queue)
    def visited_size(self):
        return len(self.visited)