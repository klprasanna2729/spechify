#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []):
        self.name = name
        self.attributes = attributes
        self.children = children

@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text

def parse_attributes(attr_str: str) -> Dict[str, str]:
    attributes = {}
    parts = attr_str.split()
    for part in parts:
        if '=' in part:
            key, val = part.split('=', 1)
            val = val.strip('"').strip("'")
            attributes[key] = val
    return attributes

def parseSSML(ssml: str) -> SSMLNode:
    ssml = ssml.strip()
    i = 0
    n = len(ssml)

    def parse_node() -> SSMLNode:
        nonlocal i
        if ssml[i] != '<':
            j = i
            while i < n and ssml[i] != '<':
                i += 1
            return SSMLText(unescapeXMLChars(ssml[j:i]))

        assert ssml[i] == '<'
        i += 1
        is_closing = ssml[i] == '/'
        if is_closing:
            while i < n and ssml[i] != '>':
                i += 1
            i += 1
            return None  # closing tag handled in upper context

        # Parse tag name
        start = i
        while i < n and ssml[i] not in [' ', '/', '>']:
            i += 1
        tag_name = ssml[start:i]

        # Parse attributes
        attr_start = i
        while i < n and ssml[i] != '>':
            i += 1
        attr_str = ssml[attr_start:i].strip().rstrip('/')
        is_self_closing = ssml[i - 1] == '/'
        i += 1  # skip '>'

        attributes = parse_attributes(attr_str)
        if is_self_closing:
            return SSMLTag(tag_name, attributes, [])

        # Parse children
        children = []
        while True:
            if ssml[i:i + 2 + len(tag_name)] == f"</{tag_name}":
                while i < n and ssml[i] != '>':
                    i += 1
                i += 1  # skip '>'
                break
            child = parse_node()
            if child:
                children.append(child)
        return SSMLTag(tag_name, attributes, children)

    return parse_node()

def ssmlNodeToText(node: SSMLNode) -> str:
    if isinstance(node, SSMLText):
        return unescapeXMLChars(node.text)
    elif isinstance(node, SSMLTag):
        output = ""
        for child in node.children:
            output += ssmlNodeToText(child)
        return output
    else:
        return ""

def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

def escapeXMLChars(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# Example usage (can be uncommented for local test)
# ssml_string = '<speak>Hello, <break time="500ms"/>world</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)
