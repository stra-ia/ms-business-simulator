import google.generativeai as genai
from fastapi.responses import JSONResponse
from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part, Tool, FunctionDeclaration

genai.configure(api_key="AIzaSyCM5ekAWoggT5PtyOMu-bMLuJrauQgPO8M")

generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

def generate_marketing_feedback(
    user_creative_body, 
    user_headline, 
    user_link_description, 
    spend_by_day, 
    days_duration, 
    total_impressions, 
    categorical_score,
    user_input_impressions_over_spend,
    brief,
    ):
  model = GenerativeModel(
      model_name="gemini-1.0-pro",
      generation_config=generation_config
  )
  prompt_parts = [
    f"""You are a Digital Marketing and Copywriting expert. Retrieve all your knowledge on the topic in order to answer the following.
        You will now receive user creative input for the different parts of the Facebook or Meta ad campaign:
        The creative for the ad is: '{{user_creative_body}}',
        The headline for the ad is '{{user_headline}}',
        The link description for the ad is '{{user_link_description}}',
        These previous parameters were passed to a machine learning model that predicted its performance and the results were the following:
        The simulation assumed that the spend by day was '{{spend_by_day}}' and the duration of the campaign in days was '{{days_duration}}'.
        total_impressions: '{{total_impressions}}'
        categorical_score (this can be 'needs work', 'good', or 'excellent') : '{{categorical_score}}'
        impression_per_dollar_spent: '{{user_input_impressions_over_spend}}'
        """,
        "user_creative_body Immerse yourself in the world of reading with our latest e-reader! Its sleek design and portable size will captivate you, while the extensive library and waterproof capabilities will keep you entertained anywhere, anytime.",
        "user_headline Escape with Books 📚 Waterproof Reader",
        "user_link_description Dive into endless reading adventures with our waterproof 7-inch HD e-reader! Carry your entire library wherever you go. Explore our massive selection now!",
        "days_duration 7",
        "spend_by_day 100",
        "total_impressions 149733",
        "categorical_score excellent",
        "user_input_impressions_over_spend 213.90",
        """The following brief contains relevant information about the company, type of user that created the campaign, and others:
        brief: '{{brief}}'
        """
        f"""output: 
        ## Campaign Feedback: Strengths and Areas for Improvement

        Based on the predicted performance results, your Facebook/Meta ad campaign looks promising! Achieving an "excellent" categorical score and over 200 impressions per dollar spent suggests you're on the right track. Let's break down the strengths of your current copy and explore some potential areas for improvement:

        **Strengths:**

        *   **Compelling Headline:** "Escape with Books 📚 Waterproof Reader" is concise, attention-grabbing, and clearly communicates the product and its unique selling point (waterproof). 
        *   **Benefit-Driven Description:** The ad creative and link description highlight key benefits like portability, extensive library access, and waterproof capabilities, which appeal to readers' desires for convenience and versatility.
        *   **Strong Call to Action:** The link description encourages users to "Explore our massive selection now!", prompting immediate action.

        **Areas for Improvement:**

        While your campaign has a strong foundation, there's always room to refine and optimize your copy. Consider these suggestions:

        *   **Target Audience:**  

            *   **Refine Targeting:**  Ensure your ad targets the right audience demographics and interests for maximum impact. Consider interests like specific book genres, reading devices, or outdoor activities (to emphasize the waterproof feature).
            *   **Personalization:** Explore ad variations that speak directly to different reader segments (e.g., fiction lovers, non-fiction enthusiasts, students). 
        *   **Creative Enhancements:**

            *   **Visual Appeal:** Include high-quality images or videos showcasing the e-reader's design and functionality.  
            *   **Lifestyle Imagery:**  Depict people enjoying the e-reader in various settings (beach, bath, commute) to emphasize its versatility.
        *   **Copywriting Tweaks:**

            *   **Specificity:** Quantify the benefits. Instead of "extensive library," mention the number of books available. 
            *   **Emotional Appeal:**  Connect with readers on an emotional level. Use words like "relax," "escape," "discover," and "imagine."
            *   **Sense of Urgency:**   Experiment with limited-time offers or exclusive deals to encourage immediate action. 
        *   **A/B Testing:** 

            *   **Continuously Test:**  Run A/B tests with different headlines, descriptions, and visuals to identify the best performing combinations. 

        **Remember, effective copywriting is an iterative process. Keep testing, analyzing results, and refining your approach to achieve optimal campaign performance.** 
        """,
        f"user_creative_body: {user_creative_body}",
        f"user_headline: {user_headline}",
        f"user_link_description: {user_link_description}",
        f"spend_by_day: {spend_by_day}",
        f"days_duration: {days_duration}",
        f"total_impressions: {total_impressions}",
        f"categorical_score: {categorical_score}",
        f"user_input_impressions_over_spend: {user_input_impressions_over_spend}"
        f"brief: {brief}"
  ]
  response = model.generate_content(prompt_parts)
  return JSONResponse(content={
        "feedback": response.candidates[0].content.parts[0].text
  })
def get_sales_feedback(brief, chat_history):
    client_model = GenerativeModel(
        model_name="gemini-1.0-pro",
    )
    result = client_model.generate_content(f"""
    You are Gemini, an AI designed to evaluate sales conversation. Based on the transcript provided, assess the sales representative's performance during the call. Focus on specific aspects of the conversation according to the type of sales approach used. Provide feedback on each parameter, offering constructive criticism and areas of improvement where necessary.
    
    #Inputs
    - Call Information: {brief}
    - Call History: {chat_history}
    
    ### Cold Call Evaluation

    #### Preparation & Engagement:
    1. Tailoring: Did the representative tailor the opening to the prospect's role and needs, demonstrating research?
    2. Clarity and Engagement: Was the opening statement clear, concise, and designed to engage the prospect?

    #### Communication & Rapport Building:
    3. Open-Ended Questions: Did the rep use open-ended questions effectively to build rapport and engage the prospect?
    4. Benefits Over Features: Did the rep emphasize benefits relevant to the prospect rather than just listing features?
    5. Active Listening: Did the rep demonstrate active listening by responding appropriately to the prospect's answers?

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
    17. Appreciation: Was appreciation shown towards the prospect's time and participation?

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

    Please provide a feedback for each of these parameters, specifying areas of strength and opportunities for improvement. It could be short and concise, focusing on the key aspects of the conversation.

    """)
    
    feedback = result.candidates[0].content.parts[0].text
    return JSONResponse(content={
        "feedback": feedback
  })