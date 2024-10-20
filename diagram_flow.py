from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
import sqlite3
from models import Artist

def add_node_all_artists(builder):
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM Artist')
    artist_rows = cursor.fetchall()
    for row in artist_rows:
        artist = Artist(row[0], row[1], row[2])
        builder.add_node(str(artist.id), (100, 100), {'content': artist.full_name}, 'default', 'right', 'right')
    conn.close()

class DiagramBuilder:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, pos, data, node_type='default', source_position=None, target_position=None):
        node = StreamlitFlowNode(id=id, pos=pos, data=data, node_type=node_type, source_position=source_position, target_position=target_position)
        self.nodes.append(node)

    def add_edge(self, id, source, target, animated=False):
        edge = StreamlitFlowEdge(id=id, source=source, target=target, animated=animated)
        self.edges.append(edge)

    def build(self, diagram_id='diagram', fit_view=True, show_minimap=True, show_controls=True, hide_watermark=True):
        state = StreamlitFlowState(self.nodes, self.edges)
        streamlit_flow(diagram_id, state, fit_view=fit_view, show_minimap=show_minimap, show_controls=show_controls, hide_watermark=hide_watermark)

def diagram_flow():
    builder = DiagramBuilder()
    add_node_all_artists(builder)

    #builder.add_node('1', (100, 100), {'content': 'Node 1'}, 'input', 'right', 'right')
    #builder.add_node('2', (350, 50), {'content': 'Node 2'}, 'default', 'right', 'left')
    #builder.add_node('3', (350, 150), {'content': 'Node 3'}, 'default', 'right', 'left')
    #builder.add_node('4', (600, 100), {'content': 'Node 4'}, 'output', 'left', 'left')

    #builder.add_edge('1-2', '1', '2', animated=True)
    #builder.add_edge('1-3', '1', '3', animated=True)
    #builder.add_edge('2-4', '2', '4', animated=True)
    #builder.add_edge('3-4', '3', '4', animated=True)

    builder.build('minimap_controls_flow')