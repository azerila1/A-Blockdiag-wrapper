#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import io
import glob
import blockdiag
from blockdiag import parser, builder, drawer, noderenderer
from blockdiag.metrics import DiagramMetrics
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from importlib import reload
import numpy as np
from cairosvg import svg2png


# In[2]:


reload(blockdiag)
reload(noderenderer)
reload(parser)


# In[3]:


columns = ['node_id',
           'directed_to',
           'direction_type',
           'edge_label',
           'label',
           'node_flag',
           'shape',
           'stacked',
           'linecolor',
           'color',
           'style',
           'textcolor',
           'width',
           'height',
           'fontsize',
           'numbered',
           'description',
           'percentage'
           'background',
           'group']
input_df = pd.DataFrame(columns=columns)

for i in range(7):
    input_df.at[i,'node_id'] = i
    input_df.at[i,'shape'] = 'box'
    input_df.at[i,'label'] = 'label_'+str(i)
    input_df.at[i,'fontsize'] = '10'
    input_df.at[i,'stacked'] = ''
    input_df.at[i,'textcolor'] = 'white'
    input_df.at[i,'directed_to'] = []
    input_df.at[i,'direction_type'] = []
    input_df.at[i,'linecolor'] = '#a9a9a9'
    input_df.at[i,'color'] = '#a9a9a9'
    
input_df.at[0,'directed_to'] = [1,]
input_df.at[0,'direction_type'] = ['towards']
input_df.at[0,'edge_label'] = ['100%','50%','85%']

input_df.at[1,'directed_to'] = [2,]
input_df.at[1,'direction_type'] = ['normal',]
input_df.at[1,'edge_label'] = ['99%']

input_df.at[2,'directed_to'] = [3,]
input_df.at[2,'direction_type'] = ['normal',]
input_df.at[2,'edge_label'] = ['70%']

input_df.at[3,'directed_to'] = [4,5,]
input_df.at[3,'direction_type'] = ['towards','towards',]

#input_df.at[4,'directed_to'] = 
#input_df.at[4,'direction_type'] = () 

input_df.at[5,'directed_to'] = [6,]
input_df.at[5,'direction_type'] = ['bidirectional',]
input_df.at[5,'edge_label'] = ['25%']

#input_df.at[6,'directed_to'] = ()
#input_df.at[6,'direction_type'] = () 

input_df.at[0,'node_flag'] = 'se'
input_df.at[1,'node_flag'] = 'us'
input_df.at[2,'node_flag'] = 'ie'
input_df.at[3,'node_flag'] = ''
input_df.at[4,'node_flag'] = 'eu'
input_df.at[5,'node_flag'] = 'ch'
input_df.at[6,'node_flag'] = 'ca'


# In[10]:


#input_df.to_csv(r'group-diagrams\Notebooks\sample_input.csv',sep=';',index=False)


# In[16]:


#input_df_2= pd.read_csv(r'group-diagrams\Notebooks\sample_input.csv',sep=';' )


# In[24]:


def parse_df_to_string(input_df):
    relation={'towards': ' -> ',
          'backwards': ' <- ',
          'normal': ' -- ',
          'bidirectional': ' <-> '}
    
    input_df.fillna('',inplace=True)
    
    edges_relation=[]
    all_nodes_attributes_string=[]
    for node_id, node_attributes in input_df.iterrows():
        node_attributes = input_df.iloc[node_id]
        for child_id, direction_type in zip(node_attributes['directed_to'], node_attributes['direction_type']):
            edges_relation.append(str(node_id) + relation[direction_type]+str(child_id))
        node_attributes_string =  str(node_id)    +'['
        for attr_name, attr_value in node_attributes.iteritems():
            if attr_value and attr_name not in ['directed_to','edge_label','direction_type','node_id','node_flag','stacked','percentage']:
                node_attributes_string += attr_name+'="'+attr_value+'",' 
        all_nodes_attributes_string.append(node_attributes_string[:-1]+']' )
    defaults = 'orientation = portrait;node_width =130;node_height = 50;default_node_color = "#d3d3d3"; default_group_color = "#7777FF";default_linecolor = black;'    
    string_commands=edges_relation+ all_nodes_attributes_string
    string_commands = '{' +";".join(string_commands)+defaults+'}'
    return string_commands


# In[25]:


def draw_diagram(string_commands):
    
    #output_formatv = "svg" #or svg,
    default_shadow_color = (255, 255, 255) # RGB white
    default_nodeline_color = (255, 255, 255) # RGB white
    size=None
    graph_string = string_commands
    tree = parser.parse_string(graph_string)

    diagram = blockdiag.builder.ScreenNodeBuilder.build(tree, None)
    diagram.separated=True
    diagram.set_color('red')
    diagram.set_orientation('portrait')


    diagram.set_default_linecolor(default_nodeline_color)
    

    fontmap = blockdiag.utils.fontmap.FontMap()
    font_loc = '/home/alireza/group-diagrams/Notebooks/Fonts/georgia.ttf'
    fontmap.set_default_font(path = font_loc)
    
    metrics = DiagramMetrics(diagram=diagram, drawer=None, fontmap=fontmap)
    
    #fontmap.set_default_fontfamily(fontfamily='serif-bold')
    #fontmap.set_default_fontfamily(fontfamily='serif')
    fontmap.fontsize =10
    #fontmap = _create_fontmap(fontmap=None, font=None)

    drawer = blockdiag.drawer.DiagramDraw(_format='svg',
                                          diagram=diagram,
                                          fontmap=fontmap,
                                          code=graph_string,
                                          antialias=True,
                                          nodoctype=False,
                                          transparency=False)

    drawer.shadow = default_shadow_color





    drawer.draw()
    svg = drawer.save()
    svg2png(bytestring = svg, write_to='/home/XXX/group-diagrams/Notebooks/output2.png',scale=4)
    #img = Image.open(io.BytesIO(res))
    img = Image.open('/home/XXX/group-diagrams/Notebooks/output2.png')    
        
        
    nodes_coordinates=[]
    nodes_ids=[]
    for node in drawer.nodes:
        r = noderenderer.get(node.shape)
        shape = r(node, metrics)
        box = metrics.cell(node).box
        nodes_coordinates.append([box.topleft,
                                  box.bottomright,
                                  box.width,
                                  box.height,
                                  box.center,
                                  (box.center[0],box.center[1]-int(box.height/2)),
                                 ])
        nodes_ids.append(int(node.id))
        if int(node.id)==9:
            NODE=node
    nodes_info = pd.DataFrame(nodes_coordinates,index=nodes_ids,columns=['top_left', 'bottom_right', 'width', 'height', 'center','top_center'])
    nodes_info.index.name='node id'
    
    for node_id in input_df.index:
        if input_df.at[node_id,'node_flag']:
            flag_img = Image.open('country-flags-master/png100px/'
                      +input_df.at[node_id,'node_flag']
                      +'.png', 'r')
            flag_img.thumbnail((100,100), Image.ANTIALIAS) # resizing the flag
            img.paste(flag_img, (nodes_info.at[node_id, 'bottom_right'][0]*4-50,
                                 nodes_info.at[node_id, 'bottom_right'][1]*4-30))
    draw = ImageDraw.Draw(img)
    for node_id in input_df.index:
        if input_df.at[node_id,'edge_label']:
            for child_id, edge_label in zip(input_df.at[node_id,'directed_to'], input_df.at[node_id,'edge_label']):
                draw.text((nodes_info.at[child_id, 'top_center'][0]*4+25,
                           nodes_info.at[child_id, 'top_center'][1]*4-50),
                          edge_label,
                          (0,0,0),
                          font=ImageFont.truetype(font_loc, 40))
                
        
    return img, svg, nodes_info


# In[32]:


img,svg,info = draw_diagram(parse_df_to_string(input_df))
#img


# In[31]:


img.save('output.png')

