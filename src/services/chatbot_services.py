from vertexai.generative_models import GenerativeModel, Content, Part
from src.configs.chatbot_configs import sales_system_instructions, marketing_system_instructions
from src.utils.chatbot_utils import functions_tools, create_sales_client, convert_history
from src.schemas.chatbot_schemas import ChatRequest
from src.services import prediction_services
from src.schemas.chatbot_schemas import SimulationType

def chat(request: ChatRequest, stream=False):

    client_brief =  None
    marketing_prediction =  None
    marketin_proposal = None

    history = convert_history(request.history)

    prompt = request.message

    system_instruction = ""

    if request.type.value == SimulationType.SALES.value:
        system_instruction = sales_system_instructions
    if request.type.value == SimulationType.MARKETING.value:
        system_instruction = marketing_system_instructions
    else :
        system_instruction = sales_system_instructions

    model = GenerativeModel(
        model_name="gemini-1.5-pro-preview-0409", 
        system_instruction=system_instruction,
        tools=[functions_tools]
    )
    
    chat = model.start_chat(history=history, response_validation=False)
    responses = chat.send_message(prompt, stream=stream)
    part = Part.from_text(text = prompt)
    content = Content(parts=[part], role="user")
    history.append(content)

    if(responses.candidates[0].content.parts[0].function_call):
        function_call = responses.candidates[0].content.parts[0].function_call
        prompt = f"Answer the next message without call a function: {request.message}"

        if function_call.name == "create_sales_client":

            customer = function_call.args["customer"]
            company_size = function_call.args["company_size"]
            sales_approach = function_call.args["sales_approach"]
            responses = create_sales_client(customer, company_size, sales_approach)
            client_brief = responses.candidates[0].content.parts[0].text
            part = Part.from_text(text = f"This is client profile. Dont send this to the user, its only to have context about it: {client_brief}")
            content = Content(parts=[part], role="model")
            history.append(content)

        if function_call.name == "marketing_prediction":
            prompt = f"Answer the next message without call a function an answering the person can whatch their prediction: {request.message}"

            user_creative_body= function_call.args["user_creative_body"]
            user_headline= function_call.args["user_headline"]
            user_link_description= function_call.args["user_link_description"]
            days_duration= function_call.args["days_duration"]
            spend_by_day= function_call.args["spend_by_day"]

            marketin_proposal = {
                "user_creative_body": user_creative_body,
                "user_headline": user_headline,
                "user_link_description": user_link_description,
                "days_duration": days_duration,
                "spend_by_day": spend_by_day
            }

            marketing_prediction = prediction_services.calculate_user_scores(
                user_creative_body,
                user_headline,
                user_link_description,
                days_duration,
                spend_by_day
            )
            part = Part.from_text(text = f"This is the prediction: {marketing_prediction}")
            content = Content(parts=[part], role="model")
            history.append(content)

        chat = model.start_chat(history=history, response_validation=False)
        responses = chat.send_message(prompt, stream=stream)

    text_message = responses.candidates[0].content.parts[0].text

    return {
        "message": text_message,
        "clientBrief": client_brief,
        "marketin_proposal": marketin_proposal,
        "marketing_prediction": marketing_prediction
    }