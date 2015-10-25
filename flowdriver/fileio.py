import os
from yattag import Doc, indent
from xml.dom.minidom import parse
from os.path import exists
from flowdriver.flowcanvas import FlowItem

def save_file(filename, flow_items):
    doc, tag, text = Doc().tagtext()

    with tag('flowdriver'):
        with tag('flow_items'):
            for item in flow_items:
                with tag('item', id=str(item.id), title=item.title, position=str(item.pos), size=str(item.size)):
                    text(item.content or '')
                    with tag('linked_items'):
                        for linked_item in item.linked_items:
                            with tag('linked_item', id=str(linked_item.id)):
                                pass


    tmp_filename = filename+'.tmp'
    with open(tmp_filename, 'w') as file:
        file.write(indent(doc.getvalue())+"\n")
    if exists(filename):
        os.unlink(filename)
    os.rename(tmp_filename, filename)


def open_file(filename):

    loaded_items = []
    DOMTree = parse(filename)
    document = DOMTree.documentElement
    if document.tagName != "flowdriver":
        return None
    flow_items = document.getElementsByTagName("item")

    for item in flow_items:
        save_id = item.getAttribute('id')
        title = item.getAttribute('title')
        pos = item.getAttribute('position')
        size = item.getAttribute('size')
        content = item.firstChild.nodeValue
        new_flow_item = FlowItem(pos, size, title, content)
        new_flow_item.id = save_id
        loaded_items.append(new_flow_item)
        for linked_item in item.getElementsByTagName("linked_item"):
            linked_id = linked_item.getAttribute('id')
            new_flow_item.linked_items.append(linked_id)

    # We need to convert the linked ids to the actual object references
    for item in loaded_items:
        linked_items = item.linked_items
        for resolver_item in loaded_items:
            if resolver_item.id in linked_items:
                in_linked_pos = linked_items.index(resolver_item.id)
                linked_items[in_linked_pos] = resolver_item

    return loaded_items