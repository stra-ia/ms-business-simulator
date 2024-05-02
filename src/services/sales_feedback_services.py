from vertexai.generative_models import GenerativeModel, Content, Part, Tool, FunctionDeclaration

def get_sales_feedback(chat_history, brief: str ):
    client_model = GenerativeModel(
        model_name="gemini-1.0-pro",
    )
    result = client_model.generate_content(f"""

        """)
    
    feedback = result.candidates[0].content.parts[0].text
    return feedback