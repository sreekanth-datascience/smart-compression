from fastapi import FastAPI
import PIL
from PIL import Image
from pydantic import BaseModel


class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''


class pixel_node:
    def __init__(self, right=None, left=None, parent=None, weight=0, code=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.weight = weight
        self.code = code


def printNodes(node, val=''):
    newVal = val + str(node.huff)
    if (node.left):
        printNodes(node.left, newVal)
    if (node.right):
        printNodes(node.right, newVal)
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")


chars = ['a', 'b', 'c', 'd', 'e', 'f']

freq = [5, 9, 12, 13, 16, 45]

nodes = []

for x in range(len(chars)):
    nodes.append(node(freq[x], chars[x]))

while len(nodes) > 1:
    nodes = sorted(nodes, key=lambda x: x.freq)

    left = nodes[0]
    right = nodes[1]

    left.huff = 0
    right.huff = 1

    newNode = node(left.freq + right.freq, left.symbol + right.symbol, left, right)

    nodes.remove(left)
    nodes.remove(right)
    nodes.append(newNode)

printNodes(nodes[0])

def pixel_frequency(pxl_lst):
    pxl_freq = {}
    for i in pxl_lst:
        if i not in pxl_freq.keys():
            pxl_freq[i] = 1
        else:
            pxl_freq[i] += 1
    return pxl_freq

def construct_node(pixel):
    node_lst = []
    for i in range(len(pixel)):
        node_lst.append(pixel_node(weight = pixel[i][1], code=str(pixel[i][0])))
    return node_lst

def construct_tree(node_lst):
    node_lst = sorted(node_lst ,key=lambda pixel_node:pixel_node.weight)
    while(len(node_lst) != 1):
        node0, node1 = node_lst[0], node_lst[1]
        merge_node = pixel_node(left=node0, right=node1, weight=node0.weight + node1.weight)
        node0.parent = merge_node
        node1.parent = merge_node
        node_lst.remove(node0)
        node_lst.remove(node1)
        node_lst.append(merge_node)
        node_lst = sorted(node_lst ,key=lambda pixel_node:pixel_node.weight)
    return node_lst

def huffman_encoding(img):
    width = img.size[0]
    height = img.size[1]
    im = img.load()
    pixel_lst = []
    for i in range(width):
        for j in range(height):
            pixel_lst.append(im[i, j])

    pixel_freq = pixel_frequency(pixel_lst)
    pixel_freq = sorted(pixel_freq.items(), key=lambda item:item[1])
    node_lst = construct_node(pixel_freq)
    huff_tree_head = construct_tree(node_lst)[0]
    encoding_table = {}


    for x in node_lst:
        curr_node = x
        encoding_table.setdefault(x.code, "")
        while(curr_node != huff_tree_head):
            if curr_node.parent.left == curr_node:
                encoding_table[x.code] = "1" + encoding_table[x.code]
            else:
                encoding_table[x.code] = "0" + encoding_table[x.code]
            curr_node = curr_node.parent

    for key in encoding_table.keys():
        print("Source Pixel: " + key + "\nCode Strength after encoding:" + encoding_table[key])
    print("Encoding Table: ", encoding_table)

    statement = "Image compressed successfully and saved at workdir"
    return statement

def decoding(w, h, encoding_table, coding_res):
    code_read_now = ''  # The currently read code
    new_pixel =[]
    i = 0
    while (i != coding_res.__len__()):
        code_read_now = code_read_now + coding_res[i]
        for key in encoding_table.keys():
            if code_read_now == encoding_table[key]:
                new_pixel. append(key)
                code_read_now = ' '
                break
        i +=1
    decode_image = Image.new( 'L' ,(w,h))
    k = 0
    for i in range(w):
        for j in range(h):
            decode_image.putpixel((i,j),(int(new_pixel[k])))
        k+=1


app = FastAPI()
class Item(BaseModel):
    image_path: str

@app.get('/')
@app.post('/compress_image/')
async def create_item(item:Item):
    item_dict = item.dict()
    a = item_dict['image_path']
    img = Image.open(a)

    g_img = img.convert('L')
    x = huffman_encoding(g_img)
    img.save("Result2.jpg")
    return x

