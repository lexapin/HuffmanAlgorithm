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
  return word_hash.keys()[0]


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


def show_how_it_works(string):
  tree = generate_tree(string)
  table = code_hash(tree)
  print "Huffman algorithm"
  print " TABLE:"
  for word, way in sorted(table.items(), key = lambda data: len(data[1])):
    print "   - '%s': %s"%(word, "".join(way))
  print " DECODE", decode(string, table)
  print " ENCODE", encode(decode(string, table), table)
  print "source length", len(string), "bytes"
  print "decode length", len(decode(string, table))/8, "+", 2*len(table), "bytes"
  

show_how_it_works("beep boop beer!")
show_how_it_works("The accepted answer is correct, but there is a more clever/efficient way to do\
 this if you need to convert a whole \
 bunch of ASCII characters to their ASCII codes at once")
