# -*- coding: utf-8 -*-
from collections import defaultdict
 
class Node(object):
  """docstring for Node"""
  def __init__(self, key = None, left = None, right = None):
    super(Node, self).__init__()
    self.key = key
    self.left = left
    self.right = right
 
  def __hash__(self):
    return id(self) if self.key is None else ord(self.key)
 
  def __eq__(self, obj):
    self_key = id(self) if self.key is None else ord(self.key)
    obj_key = id(obj) if obj.key is None else ord(obj.key)
    return self_key == obj_key
 
  def __repr__(self):
    return "<NODE: %s>"%self.key
 
def generate_tree(string):
  word_hash = defaultdict(int)
  for word in string:
    word_hash[Node(word)] += 1
  while len(word_hash) > 1:
    left, right = sorted(word_hash.items(), key = lambda repeat: repeat[1])[:2]
    node = Node(left = left[0], right = right[0])
    word_hash[node] = left[1] + right[1]
    del word_hash[left[0]], word_hash[right[0]]
  return list(word_hash.keys())[0]
 
def code_hash(node, direction = None):
  result = {}
  if node.key is None:
    result.update(code_hash(node.left, "0"))
    result.update(code_hash(node.right, "1"))
    if direction is not None:
      for key in result: result[key].insert(0, direction)
  else: result[node.key] = [direction]
  return result
 
def decode(string, table):
  result = ""
  for word in string:
    result += "".join(table[word])
  return result
 
def restore_tree(table):
  node = Node()
  for word, way in table.items():
    current_node = node
    for direction in way:
      attr = ""
      if direction == "0": attr = "left"
      elif direction == "1": attr = "right"
      if getattr(current_node, attr, None) is None:
        setattr(current_node, attr, Node())
      current_node = getattr(current_node, attr)
    current_node.key = word
  return node
 
def encode(string, table):
  root_node = restore_tree(table)
  result = ""
  current_node = root_node
  for bit in string:
    attr = ""
    if bit == "0": attr = "left"
    elif bit == "1": attr = "right"
    current_node = getattr(current_node, attr)
    if current_node.key is None: continue
    else:
      result += current_node.key
      current_node = root_node
  return result
 
def open_txt_file(file_name):
  data = ""
  with open(file_name, "r") as file:
    data = file.read()
  line = ""
  try:
    return data.decode('utf-8').encode('utf-8')
  except:
    print("WARNING")
    return str(data.encode('utf-8'))

def to_int(char):
  return char if isinstance(char, int) else ord(char)
 
def open_huf_file(file_name):
  data = None
  with open(file_name, "rb") as file:
    data = file.read()
  keys_len = to_int(data[0])
  data = data[1:]
  table = {}
  for i in range(keys_len):
    key = chr(to_int(data[0])); data = data[1:]
    char_len = to_int(data[0]); data = data[1:]
    chars = data[:char_len-1]; data = data[char_len-1:]
    lb = to_int(data[0]); data = data[1:]
    table[key] = [char for char in create_binary_string_from_chars(chars, lb)]
  raw_string = data[:-1]
  last_byte_len = to_int(data[-1])
  return table, create_binary_string_from_chars(raw_string, last_byte_len)
 
def create_char_string_from_binary(binary_string):
  bin_array = []
  while len(binary_string) > 8:
    bin_array.append(binary_string[:8])
    binary_string = binary_string[8:]
  last_bit = 0
  if binary_string:
    last_bit = 8-len(binary_string)
    binary_string += "0"*last_bit
    bin_array.append(binary_string)
  binary_string = "".join([chr(int(char, 2)) for char in bin_array])
  return binary_string, chr(last_bit)
 
def create_binary_string_from_chars(raw_string, last_byte_len):
  string_array = ["0"*(8-len(bin(to_int(char))[2:]))+bin(to_int(char))[2:] for char in raw_string]
  string_array[-1] = string_array[-1][:(8-last_byte_len)]
  string = "".join(string_array)
  return string
 
def save_huf_file(file_name, table, binary_string):
  table_string = [len(table)]
  for key, bit_list in table.items():
    bs, lb = create_char_string_from_binary("".join(bit_list))
    bit_len = len(bs) + 1
    table_string += [ord(key), bit_len] + [ord(char) for char in bs] + [ord(lb)]
  binary_string, last_bit = create_char_string_from_binary(binary_string)
  with open(file_name, "wb") as file:
    file.write(bytearray(table_string))
    file.write(bytearray([ord(char) for char in binary_string]))
    file.write(bytearray([ord(char) for char in last_bit]))
  return True
 
def show_how_it_works(file_name):
  string = open_txt_file(file_name)
  tree = generate_tree(string)
  table = code_hash(tree)
  print ("Huffman algorithm")
  print (" TABLE:")
  for word, way in sorted(table.items(), key = lambda data: len(data[1])):
    print ("   - '%s': %s"%(word, "".join(way)))
  save_huf_file("%s_huf"%file_name, table, decode(string, table))
  new_table, new_string = open_huf_file("%s_huf"%file_name)
  print (" ENCODE", encode(new_string, new_table))
 
show_how_it_works("tests/test1")
show_how_it_works("tests/test2")
show_how_it_works("tests/test3")
