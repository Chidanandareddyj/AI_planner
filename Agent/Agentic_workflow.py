# from utils
from langgraph.graph import StateGraph,END,START,MessagesState

from Prompt_library.Prompts import SYSTEM_PROMPT
from langgraph.prebuilt import ToolNode, tool_node, tools_condition

class graphbuilder(object):
    def __init__(self):
        self.tools=[
             # Tool1,
             # Tool2,
            ]
        
        self.system_prompt=SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """
        Docstring for agent_function
        
        :param self: Description
        :param input: Description
        """
        user_question=state["messages"]
        input_question=self.system_prompt+user_question
        response=self.llm_with_tools.invoke(input_question)
        # state["messages"].append(response)  
        return {"response": response}


    def build_graph(self, nodes, edges):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        self.graph=graph_builder.compile()
        return self.graph
    
    def __call__(self, *args, **kwds):
            return self.build_graph()