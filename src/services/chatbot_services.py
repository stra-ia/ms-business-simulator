from vertexai.generative_models import GenerativeModel, Content, Part, Tool, FunctionDeclaration
from pydantic import BaseModel
from typing import List, Dict

class SalesObject(BaseModel):
    id: int
    type: str
    isField: bool
    title: str
    description: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]
    salesObjects: List[SalesObject]

def convert_history(history):
    content_list = []
    for message in history:
        part = Part.from_text(text = message.content)
        content = Content(parts=[part], role=message.role)
        content_list.append(content)
    return content_list

def imprimir_texto(texto):
    # Verificar si la entrada es una tupla
    if isinstance(texto, tuple):
        # Asumimos que la tupla contiene solo un elemento que es el texto
        print(texto[0])
    else:
        # Si no es una tupla, imprimir directamente
        print(texto)

def chat(request: ChatRequest, stream=False):

    client_brief =  None


    def update_is_field(item_type, new_value):
        items = request.salesObjects
        for item in items:
            if item.type == item_type:
                item.isField = new_value
        return items
    
    
    def update_is_field(item_type, new_value):
        items = request.salesObjects
        for item in items:
            if item.type == item_type:
                item.isField = new_value
        return items
    
    def create_sales_client(customer, company_size, sales_approach):
        client_model = GenerativeModel(
            model_name="gemini-1.0-pro",
        )
        result = client_model.generate_content(f"""
            Description: "From the given inputs - customer, company size, and sales approach - extract and organize the information into a coherent client profile. Additionally, synthesize a 'More Info' section that provides insights into the client's specific needs and preferences that would be useful for a seller during a sales engagement. For 'Demo' and 'Closer' sales types, focus on primary needs that can be directly addressed in the pitch. For 'Discovery', compile information similar to what could be found online to prepare for exploratory conversation."
                                               
            Inputs:
            - Customer: {customer}
            - Company Size: {company_size}
            - Sales Approach: {sales_approach}

            Instructions:
            1. Input the client type, company size, and sales type into the system.
            2. Based on the sales type, generate insights appropriate for the engagement:
            - For 'Demo' and 'Closer', list specific needs and how the product/service can meet those needs.
            - For 'Discovery', gather general company information and potential areas of interest that align with what is typically available online.

            Output:
            - A structured list of inputs including 'Client Type', 'Company Size', and 'Sales Type' separated by '***'.
            - A 'More Info' section tailored to the sales type, providing actionable insights for the seller to use when offering services or products. It should be short, concise, and relevant to the client's needs and preferences. No more than 100 characters. Create an original name for the business and a brief description of the company's industry position and specific needs.

            Example:
            ### Client Type
            [Client Type]
            ***

            ### Company Size
            [Company Size]
            ***

            ### Sales Type
            [Sales Type]
            ***

            ### More Info
            [Here provide a tailored, third-person narrative about the client's industry position, specific needs, and how the seller's products or services could meet these needs, based on the type of sales approach selected.]

            Give me only this information. Dont show the Character count.
            """)
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
        # function_declarations=[create_sales_client_func]
        # function_declarations=[update_field_func]
        function_declarations=[create_sales_client_func]
    )

    history = convert_history(request.history)

    # prompt = f"The response will be short and concise. {request.message}"
    prompt = f"{request.message}"

    system_instruction = """
        
        You are a chatbot tasked with collecting detailed information to generate a customer profile for a sales training simulation. Begin by asking the user about the type of customer they aim to sell to and practice with. The options are: CEO, Product Manager, or Sales. Explain that higher positions like CEOs will involve more challenging negotiations due to their strategic importance and decision-making power.

        Next, inquire about the size of the company the user will be dealing with. Emphasize that larger companies often have more complex decision-making processes and bureaucratic layers, affecting the sales approach and strategy.

        Then, ask the user to specify the type of sales approach they intend to practice:
        1. **Discovery** - Training for a setter, where the user needs to gather initial information about the potential needs and interests of the client.
        2. **Demo** - A meeting scenario where the user already has some information about what the client wants, and the goal is to pitch and identify a specific need that their product or service can fulfill.
        3. **Closer** - The user has identified the client's need and must make a detailed proposal to seal the deal.

        If the user is ready to transition to creating the sales client profile, ask them to confirm they have finished providing the initial information. Upon their confirmation, you should then call the create_sales_client function to generate the customer profile.
        
        After collecting all the necessary information, Gemini should take on the role of the customer profile just created. This role-play will simulate a sales interaction, allowing the user to practice their sales pitch and negotiation skills based on the profiled scenario. Ensure that Gemini adapts its responses to mimic the complexity and specific requirements of the customer's position, company size, and the selected sales approach.

    """

    # If the user is ready to transition to creating the sales client profile, ask them to confirm they have finished providing the initial information. Upon their confirmation, you should then call the create_sales_client function to generate the customer profile. This will lead to the commencement of the role-play module, allowing the user to engage in a simulated sales interaction.

    model = GenerativeModel(
        model_name="gemini-1.5-pro-preview-0409", 
        # model_name="gemini-1.0-pro", 
        system_instruction=system_instruction,
        tools=[functions_tools]
        )
    chat = model.start_chat(history=history, response_validation=False)
    responses = chat.send_message(prompt, stream=stream)
    part = Part.from_text(text = prompt)
    content = Content(parts=[part], role="user")
    history.append(content)


    # if(stream):
    #     return responses
    print("\n\n\nresponses: ", responses.candidates[0].content, "\n\n\n")

    # print(responses.candidates[0].content.parts[0].function_call)

    if(responses.candidates[0].content.parts[0].function_call):
        function_call = responses.candidates[0].content.parts[0].function_call
        prompt = f"Responde the next message withow call a funciton: {request.message}"

        if function_call.name == "create_sales_client":
            customer = function_call.args["customer"]
            company_size = function_call.args["company_size"]
            sales_approach = function_call.args["sales_approach"]
            responses = create_sales_client(customer, company_size, sales_approach)
            client_brief = responses.candidates[0].content.parts[0].text
            part = Part.from_text(text = f"This is client profile. Dont send this to the user, its only to have context about it: {client_brief}")
            content = Content(parts=[part], role="model")
            history.append(content)

        # if(responses.candidates[0].content.parts[0].text):
        chat = model.start_chat(history=history, response_validation=False)
        responses = chat.send_message(prompt, stream=stream)
    print("client_brief",client_brief)

    # text_message = None
    text_message = responses.candidates[0].content.parts[0].text

    # if responses.candidates[0].content.parts[0].text:
    #     text_message = responses.candidates[0].content.parts[0].text
    # if client_brief:
    #     text_message = client_brief

    # messages = {"message": responses.candidates[0].content.parts[0].text}
    # messages = {"message": "esta es una prueba"}
    return {
        "message": text_message,
        "clientBrief": client_brief
    }
    # return {
    #     "message": "Transcription failed",
    # }