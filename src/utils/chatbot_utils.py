from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration
from src.configs.chatbot_configs import create_sales_client_prompt
from vertexai.generative_models import GenerativeModel, Content, Part, Tool, FunctionDeclaration
import markdown
from bs4 import BeautifulSoup

def create_sales_client(customer, company_size, sales_approach):
    client_model = GenerativeModel(
        model_name="gemini-1.0-pro",
    )
    result = client_model.generate_content(create_sales_client_prompt.format(customer=customer, company_size=company_size, sales_approach=sales_approach))
    return result

create_sales_client_func = FunctionDeclaration(
    name="create_sales_client",
    description="""Initiates the synthesis of a client profile leveraging the input data: customer type, company size, and sales approach. This function is activated only after all the necessary 'isField' attributes have been confirmed as 'true', indicating the completion of the data collection phase. It is designed to compile this information into a comprehensive profile, which then provides actionable insights and customized strategies suitable for the client, enabling effective sales engagement.""",
    parameters={
        "type": "object",
        "properties": {
            "customer": {
                "type": "string",
                "description": """Determines the customer role to be addressed in the profile. This attribute is foundational as it informs the strategic direction and the sales strategies to be incorporated within the profile, catering to the specific role's influence and decision-making capacity within the sales process."""
            },
            "company_size": {
                "type": "string",
                "description": """Establishes the company's scale, which could range from the number of employees to its market position, providing crucial context for the complexity and scope of the sales strategy to be developed."""
            },
            "sales_approach": {
                "type": "string",
                "enum": ["Discovery", "Demo", "Closer"],
                "description": """Specifies the sales methodology to be applied in the profile. It tailors the profile to align with the chosen approach, reflecting the varying levels of information gathering, demonstration, or closing strategies needed for each sales stage."""
            },
        },
        "required": ["customer", "company_size", "sales_approach"]
    }
)

functions_tools = Tool(
    function_declarations=[create_sales_client_func]
)

def convert_history(history):
    content_list = []
    for message in history:
        part = Part.from_text(text = message.content)
        content = Content(parts=[part], role=message.role)
        content_list.append(content)
    return content_list

def markdown_to_text(markdown_text):
    # Convertir Markdown a HTML
    html = markdown.markdown(markdown_text)
    
    # Parsear HTML para obtener texto plano
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    
    # Opcionalmente, puedes eliminar espacios adicionales
    text = ' '.join(text.split())
    
    return text