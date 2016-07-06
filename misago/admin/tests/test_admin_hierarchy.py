from django.test import TestCase

from misago.admin.hierarchy import Node


class NodeTests(TestCase):
    def test_add_node(self):
        """add_node added node"""
        master = Node(name='Apples', link='misago:index')

        child = Node(name='Oranges', link='misago:index')
        master.add_node(child)

        self.assertTrue(child in master.children())

    def test_add_node_after(self):
        """add_node added node after specific node"""
        master = Node(name='Apples', link='misago:index')

        child = Node(name='Oranges', link='misago:index')
        master.add_node(child)

        test = Node(name='Potatoes', link='misago:index')
        master.add_node(test, after='misago:index')

        all_nodes = master.children()
        for i, node in enumerate(all_nodes):
            if node.name == test.name:
                self.assertEqual(all_nodes[i - 1].name, child.name)

    def test_add_node_before(self):
        """add_node added node  before specific node"""
        master = Node(name='Apples', link='misago:index')

        child = Node(name='Oranges', link='misago:index')
        master.add_node(child)

        test = Node(name='Potatoes', link='misago:index')
        master.add_node(test, before='misago:index')

        all_nodes = master.children()
        for i, node in enumerate(all_nodes):
            if node.name == test.name:
                self.assertEqual(all_nodes[i + 1].name, child.name)
