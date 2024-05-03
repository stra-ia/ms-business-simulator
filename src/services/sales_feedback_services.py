from vertexai.generative_models import GenerativeModel, Content, Part, Tool, FunctionDeclaration
from src.schemas.feedback_schemas import FeedbackRequest

def get_sales_feedback(request: FeedbackRequest ):
    client_model = GenerativeModel(
        model_name="gemini-1.0-pro",
    )
    result = client_model.generate_content(f"""
    You are Gemini, an AI designed to evaluate sales conversation. Based on the transcript provided, assess the sales representative's performance during the call. Focus on specific aspects of the conversation according to the type of sales approach used. Provide feedback on each parameter, offering constructive criticism and areas of improvement where necessary.
    
    #Inputs
    - Call Information: {request.brief}
    - Call History: {request.chat_history}
    
    ### Cold Call Evaluation

    #### Preparation & Engagement:
    1. Tailoring: Did the representative tailor the opening to the prospect's role and needs, demonstrating research?
    2. Clarity and Engagement: Was the opening statement clear, concise, and designed to engage the prospect?

    #### Communication & Rapport Building:
    3. Open-Ended Questions: Did the rep use open-ended questions effectively to build rapport and engage the prospect?
    4. Benefits Over Features: Did the rep emphasize benefits relevant to the prospect rather than just listing features?
    5. Active Listening: Did the rep demonstrate active listening by responding appropriately to the prospect’s answers?

    #### Objection Handling:
    6. Composure: Did the rep maintain composure when facing objections?
    7. Handling Techniques: How were objections handled? Were the responses clear, concise, and well-structured?
    8. Providing Value: Was objection handling used as an opportunity to provide additional value or insights?

    #### Qualification:
    9. Prospect Suitability: If relevant, was the rep able to quickly identify that the prospect was not suitable?
    10. Information Gathering: If relevant, was the rep able to pivot the conversation to gather additional useful information?
    11. Obtaining Contacts: If relevant, did the rep obtain details for a more appropriate contact within the organization?

    #### Professionalism:
    12. Professional Conduct: Was the conversation conducted with respect and professional language?
    13. Language Appropriateness: Was the language used suitable for the prospect's understanding?

    #### Closing & Follow-Up:
    14. Call to Action: Was there a clear call to action for the next step?
    15. Scheduling Follow-Up: Did the rep schedule a follow-up or commit to next steps, if necessary?
    16. Conversation Summary: Did the rep summarize the conversation effectively before closing?
    17. Appreciation: Was appreciation shown towards the prospect’s time and participation?

    ### Discovery Call Evaluation

    #### Understanding Needs:
    1. Quality of Questions: Were the questions asked effective in understanding the customer's needs?
    2. Problem Identification: Were the main problems of the customer identified and acknowledged?
    3. Problem Solving Benefits: Was it clearly explained how solving these problems can benefit the customer's business?
    4. Product Benefits: Were the benefits of the product or solution convincingly communicated?
    5. Solution Fit: Was it confirmed that the product or solution can address the customer's problems?
    6. Buying Process: Was the customer's buying process clearly understood and explained?
    7. Objection Handling: Were any worries or objections from the customer effectively handled?
    8. Next Steps: Were clear next steps in the sales process established?

    ### Additional Parameters for Demo and Closer Calls (If applicable)
    #### Demo:
    - Demonstration Relevance: Was the demonstration tailored to address the specific needs identified by the customer?
    - Engagement During Demo: Did the representative ensure the customer was engaged and understanding the demonstration?

    #### Closer:
    - Proposal Clarity: Was the proposal clearly aligned with the customer's needs and the benefits outlined?
    - Closing Urgency: Was a sense of urgency conveyed in a professional manner to close the deal?

    Please provide detailed feedback for each of these parameters, specifying areas of strength and opportunities for improvement.

    """)
    
    feedback = result.candidates[0].content.parts[0].text
    return feedback