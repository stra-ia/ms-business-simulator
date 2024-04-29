from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part, Tool, FunctionDeclaration
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

def chat(request: ChatRequest, stream=False):

    client_brief =  None

    def update_is_field(item_type, new_value):
        items = request.salesObjects
        for item in items:
            if item.type == item_type:
                item.isField = new_value
        return items
    
    def create_sales_client(customer, company_size, sales_approach):
        client_model = GenerativeModel(
            model_name="gemini-1.5-pro-preview-0409",
        )
        result = client_model.generate_content(f"""
            Description: "From the given inputs - customer, company size, and sales approach - extract and organize the information into a coherent client profile. Additionally, synthesize a 'More Info' section that provides insights into the client’s specific needs and preferences that would be useful for a seller during a sales engagement. For 'Demo' and 'Closer' sales types, focus on primary needs that can be directly addressed in the pitch. For 'Discovery', compile information similar to what could be found online to prepare for exploratory conversation."
                                               
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
            - A structured list of inputs including 'Client Type', 'Company Size', and 'Sales Type'.
            - A 'More Info' section tailored to the sales type, providing actionable insights for the seller to use when offering services or products.
            """)
        return result
    
    update_field_func = FunctionDeclaration(
        name="update_is_field",
        description="""Update the isField attribute for a specific item when the user provides related information.
            This function is triggered when information about the customer profile (customer),
            company size (company_size), or type of sales approach (sales_approach) is provided.
            It should be called to update the corresponding item's isField attribute to true,
            indicating that the field has been addressed.""",
        parameters={
            "type": "object",
            "properties": {
                "item_type": {
                    "type": "string",
                    "description": """The type of item to update. Use 'customer' for customer type updates, 
                        'company_size' for company size updates, and 'sales_approach' for updates about the type of sales approach."""
                },
                "new_value": {
                    "type": "boolean",
                    "description": "The new value for the isField attribute of the item. It could be 'true' or 'false'"
                }
            },
            "required": ["item_type", "new_value"]
        }
    )
    create_sales_client_func = FunctionDeclaration(
        name="create_sales_client",
        description="""Generates a detailed client profile based on customer type, company size, and sales approach. This function synthesizes information to aid sellers in engaging effectively with potential clients by providing tailored insights and actionable strategies specific to the sales type chosen.""",
        parameters={
            "type": "object",
            "properties": {
                "customer": {
                    "type": "string",
                    "description": """Specifies the type of customer (e.g., CEO, Product Manager, Sales) to tailor the client profile for specific customer roles, reflecting their strategic importance and decision-making power in the sales process."""
                },
                "company_size": {
                    "type": "string",
                    "description": """Indicates the size of the company (e.g., '150 people') to provide context on the complexity of the decision-making processes and the bureaucratic layers, which impacts the sales strategy."""
                },
                "sales_approach": {
                    "type": "string",
                    "description": """Describes the sales approach (Discovery, Demo, Closer) to be used. This determines the type of information compiled:
                        - 'Discovery' focuses on general company information and potential interests.
                        - 'Demo' and 'Closer' focus on specific needs and how the product or service can meet those needs."""
                },
            },
            "required": ["customer", "company_size", "sales_approach"]
        }
    )

    functions_tools = Tool(
        function_declarations=[create_sales_client_func, update_field_func]
    )

    history = convert_history(request.history)

    # prompt = f"The response will be short and concise. {request.message}"
    prompt = f"{request.message}"

    system_instruction = """
        You are a chatbot called StraIA tasked with collecting detailed information to generate a customer profile for a sales training simulation. Begin by asking the user about the type of customer they aim to sell to and practice with. The options are: CEO, Product Manager, or Sales. Explain that higher positions like CEOs will involve more challenging negotiations due to their strategic importance and decision-making power.

        Next, inquire about the size of the company the user will be dealing with. Emphasize that larger companies often have more complex decision-making processes and bureaucratic layers, affecting the sales approach and strategy.

        Then, ask the user to specify the type of sales approach they intend to practice:
        1. **Discovery** - Training for a setter, where the user needs to gather initial information about the potential needs and interests of the client.
        2. **Demo** - A meeting scenario where the user already has some information about what the client wants, and the goal is to pitch and identify a specific need that their product or service can fulfill.
        3. **Closer** - The user has identified the client's need and must make a detailed proposal to seal the deal.

        After collecting all the necessary information, Gemini should take on the role of the customer profile just created. This role-play will simulate a sales interaction, allowing the user to practice their sales pitch and negotiation skills based on the profiled scenario. Ensure that Gemini adapts its responses to mimic the complexity and specific requirements of the customer's position, company size, and the selected sales approach.
    """

    model = GenerativeModel(
        model_name="gemini-1.5-pro-preview-0409", 
        # generation_config={"max_output_tokens": 100}, 
        system_instruction=system_instruction, 
        tools=[functions_tools]
        )
    chat = model.start_chat(history=history, response_validation=False)
    responses = chat.send_message(prompt, stream=stream)

    # if(stream):
    #     return responses
    print(responses)

    # print(responses.candidates[0].content.parts[0].function_call)

    if(responses.candidates[0].content.parts[0].function_call):
        function_call = responses.candidates[0].content.parts[0].function_call
        print("\n\n\nfunction_call: ", function_call, "\n\n\n")
        prompt = f"Responde the next message withow call a funciton: {request.message}"
        if function_call.name == "update_is_field":
            item_type = function_call.args["item_type"]
            new_value = function_call.args["new_value"]
            # print("item_type: ", item_type)
            request.salesObjects = update_is_field(item_type, new_value)

        if function_call.name == "create_sales_client":
            customer = function_call.args["customer"]
            company_size = function_call.args["company_size"]
            sales_approach = function_call.args["sales_approach"]
            responses = create_sales_client(customer, company_size, sales_approach)
            print("\n\n\n create_sales_client: ", responses, "\n\n\n")
            print("\n\n\n create_sales_client: ", responses.candidates[0].content, "\n\n\n")
            client_brief = responses.candidates[0].content.parts[0].text,

        responses = chat.send_message(prompt, stream=stream)
    print("client_brief",client_brief)

    # messages = {"message": responses.candidates[0].content.parts[0].text}
    # messages = {"message": "esta es una prueba"}
    return {
        "message": responses.candidates[0].content.parts[0].text,
        "salesObjects": request.salesObjects,
        "clientBrief": client_brief
    }
    # return {
    #     "message": "Transcription failed",
    # }