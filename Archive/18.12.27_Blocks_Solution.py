#!/usr/bin/env python
# coding: utf-8

# Editor | Date | Comment
# --- | --- | ---
# Alireza Ranjbar | 27.12.2018 | Initial version

# In[1]:


import os
import io
import glob
import blockdiag
from blockdiag import parser, builder, drawer, noderenderer
from blockdiag.metrics import DiagramMetrics
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from importlib import reload


# In[2]:


reload(blockdiag)
reload(noderenderer)
reload(parser)


# In[3]:


from pyensae.graphhelper.blockdiag_helper import _create_fontmap


# The below string is the main input which discribes the relation between the blocks, colors, and various settings which are elaborated in the documentation of Blockdiag package.
# 
# The idea is so far to have a script which generates the below string automatically based on a given table (e.g. pandas DataFrame) which includes the information such as node colors and nodes relation (parent/child shown by the direction of the arrow or a neutral relation with no direction and merely a connection between the two nodes).
# 
# Having used the logic behind the blockdiag kit, the output pillow image is used to paste the remaining information (such as the image of the flags) on the nodes, with the coordinates provided by the blockdiag output.

# In[9]:


graph_string = """{
//default settings'documentation:
// http://blockdiag.com/en/blockdiag/attributes/diagram.attributes.html?highlight=default#blockdiag_diagram_attr-default_fontsize
// 1 -> 2 makes two nodes with ids of 1 and 2 where 1 has an edge pointing towards 2. Using these ids, a label can
// be written for the nodes as shown. These ids can also be later used for knowing the coordinates of the nodes.
    
    
    // Set span metrix
     //  span_height = 90;
      // span_width = 160;
       
    
    orientation = portrait
        6 -> 7;
        2 -- 11;   
        1 -> 2;   1 [label = "Britain_1"];
        2 -- 3;   2 [label = "Label4  \n label5 \n label6"]
        3 -- 4;   
        4 -> 5;   
        5 -> 6; //6 [shape = "ellipse", stacked] 
        9 -> 7;   9 [shape = "cloud", stacked] 
        2 -- 10;  10 [shape = "box", stacked]; 10 [linecolor =  "#7777FF"];
         
        2 -> 9;   
        
//define default parameters 

   // defaultnode sizes
        node_width =130;
        node_height = 50;
        
    // default colors
        default_node_color = "#d3d3d3";
        
        
        default_group_color = "#7777FF";
        default_linecolor = black;
      
// give a specific color to a node:
      1 [color  = "#008080"];
      
// showing certain nodes in one group:
      group {
              // set the group label text and its color
              label = "Third group";
              color =blue //"#0000FF";

              // Set group shape to 'line group' (default is box)
              shape = line;

              // Set line style (effects to 'line group' only)
              style = dashed;
               6 -> 8 ;7
             }
}"""

output_formatv = "png" #or svg,
default_shadow_color = (255, 255, 255) # RGB white
default_nodeline_color = (255, 255, 255) # RGB white
size=None

tree = parser.parse_string(graph_string)
fontmap =_create_fontmap(fontmap=None,  font=None)
ScreenNodeBuilder = blockdiag.builder.ScreenNodeBuilder



diagram = ScreenNodeBuilder.build(tree, None)
diagram.separated=True
diagram.set_color('red')
diagram.set_orientation('portrait')


diagram.set_default_linecolor(default_nodeline_color)
metrics = DiagramMetrics(diagram=diagram, drawer=None, fontmap=fontmap)


drawer = blockdiag.drawer.DiagramDraw(_format=output_formatv,
                                      diagram=diagram,
                                      fontmap=fontmap,
                                      code=graph_string,
                                      antialias=True,
                                      nodoctype=False,
                                      transparency=False)

drawer.shadow=default_shadow_color





drawer.draw()
res = drawer.save()
if output_formatv=="png":
    img = Image.open(io.BytesIO(res))
img


# Getting the coordinates of the boxes which can be used for pasting, for example, flag images on the output pillow image:

# In[10]:


nodes_coordinates=[]
nodes_ids=[]
for node in drawer.nodes:
    r = noderenderer.get(node.shape)
    shape = r(node, metrics)
    box = metrics.cell(node).box
    nodes_coordinates.append([box.topleft, box.bottomright, box.width, box.height, box.center])
    nodes_ids.append(int(node.id))
    if int(node.id)==9:
        NODE=node
nodes_info = pd.DataFrame(nodes_coordinates,index=nodes_ids,columns=['top_left', 'bottom_right', 'width', 'height', 'center'])
nodes_info.index.name='node id'
nodes_info


# Getting the coordinates information of the edges:

# In[11]:


edges_info=[]
for edge in drawer.edges:
    coordinates = metrics.edge(edge).shaft.xy
    heads = metrics.edge(edge).heads
    if coordinates:
        edges_info.append([edge.node1.id, edge.node2.id, coordinates[0], coordinates[1], heads])        
edges_info = pd.DataFrame(edges_info,columns=['node1 id','node2 id','X','Y','heads'])
edges_info


# # Pasting flag images

# In[12]:


flag_img = Image.open('britain_flag.png', 'r')
flag_img.thumbnail((35,35), Image.ANTIALIAS) # resizing the flag
img.paste(flag_img, (nodes_info.at[1, 'bottom_right'][0]-20,
                     nodes_info.at[1, 'bottom_right'][1]-15))
img


# # Writing text on the image

# In[14]:


draw = ImageDraw.Draw(img)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((300,130),'SAMPLE TEXT',(0,0,0), font=ImageFont.truetype('arial.ttf', 10))
img

