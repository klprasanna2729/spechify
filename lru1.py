#!/usr/bin/env python3
from typing import Any, Optional
class Node:
     def __int__(self,key:str,value:Any):
         self.key=key
         self.value=value
         self.prev=None
         self.next=None

class LRUCache:


    def __init__(self, item_limit: int):
        self.capacity = item_limit
        self.cache = {}  # key -> Node
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
    def _add_node_to_front(self, node: Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_front(self, node: Node):
        self._remove_node(node)
        self._add_node_to_front(node)

    def _evict_lru(self):
        lru_node = self.tail.prev
        if lru_node and lru_node != self.head:
            self._remove_node(lru_node)
            del self.cache[lru_node.key]

        

    def has(self, key: str) -> bool:
        return key in self.cache
        
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            node=self.cache[key]
            self._move_to_front(node)
            return node.value
        return None
        

    def set(self, key: str, value: Any):
      if key in self.cache:
          node = self.cache[key]
          node.value = value
          self._move_to_front(node)
      else:
         if len(self.cache) >= self.capacity:
             self._evict_lru()
         new_node = Node(key, value)
         self._add_node_to_front(new_node)
         self.cache[key] = new_node
        