from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


 
import UI_window
graphviz = GraphvizOutput()
graphviz.output_file = 'call_graph.png'
with PyCallGraph(output=graphviz):

	user_i = UI_window.Router_UI()
	user_i.mainloop()
pass
