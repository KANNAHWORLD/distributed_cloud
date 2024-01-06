class Node:
    """
    Represents a node in a doubly linked list.
    
    Attributes:
        data: The data stored in the node.
        prev: A reference to the previous node in the list.
        next: A reference to the next node in the list.
    """
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLinkedList:
    """
    A class representing a double linked list.

    Attributes:
        head (Node): The head node of the linked list.
        tail (Node): The tail node of the linked list.
    """

    def __init__(self):
        """
        Initializes an empty double linked list.
        """
        self.head = None
        self.tail = None

    def add_front(self, new_node):
        """
        Adds a new node with the given data to the front of the linked list.

        Args:
            data: The data to be stored in the new node.
        """

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def add_end(self, new_node):
        """
        Adds a new node with the given data to the end of the linked list.

        Args:
            data: The data to be stored in the new node.
        """
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def remove_node(self, node):
        """
        Removes the given node from the linked list.

        Args:
            node (Node): The node to be removed.
        """

        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next

        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

    def remove_front(self):
        """
        Removes the first node from the linked list.
        """
        if self.head is not None:
            self.remove_node(self.head)
        
        return

    def move_to_end(self, node):
        """
        Moves the given node to the end of the linked list.

        Args:
            node (Node): The node to be moved.
        """
        if node == self.tail:
            return

        self.remove_node(node)
        self.tail.next = node
        node.prev = self.tail
        node.next = None
        self.tail = node

    def create_add_node(self, node)-> Node:
        """
        Creates a new node with the given value and adds it to the front of the linked list.

        Args:
            node: The value of the new node to be created.

        Returns:
            Node class: The newly created node.
        """
        nNode = Node(node)
        self.add_front(nNode)
        return nNode

    def get_front(self):
        """
        Returns the data stored in the first node of the linked list.

        Returns:
            The data stored in the first node of the linked list.
        """
        return None if not self.head else self.head.data
        