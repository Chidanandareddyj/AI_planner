from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from Agent.Agentic_workflow import graphbuilder
app = FastAPI()

class Queryrequest(BaseModel):
    question: str

@app.post("/query") 
async def query_agent(query: Queryrequest):
    try:
        print(query)
        graph=graphbuilder(model_provider="groq").build_graph(nodes=[],edges=[])
        react_app=graph()


        png_graph=react_app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_graph)

        print("Graph drawn and saved as graph.png")

        messages={"messages": [query.question]}
        output=react_app.invoke(messages)
        print("Output from agent:", output)

        if isinstance(output, dict) and "response" in output:
            return {"response": output["response"]}
        else:
            return str(output)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
