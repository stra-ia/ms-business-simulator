import google.generativeai as genai
from fastapi.responses import JSONResponse

genai.configure(api_key="AIzaSyAeR3HN4a6DjDlBSSUBJtMxatNhja3Ns-8")

generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

def generate_feedback(
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
  model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
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
  return JSONResponse(content=response.text)