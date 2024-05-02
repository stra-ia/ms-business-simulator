import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from tensorflow.keras.models import load_model

# Initialize tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')
bert_model.eval()

model_path = './src/models/final_model.h5'

# Load the model
model = load_model(model_path)

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Use mean pooling to get a single vector (simple sentence embedding)
    return outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

def prepare_user_input(body_string, headline_string, link_description_string):
    embedded_body_string = text_to_embedding(body_string)
    embedded_headline_string = text_to_embedding(headline_string)
    embedded_link_description_string = text_to_embedding(link_description_string)
    return embedded_body_string, embedded_headline_string, embedded_link_description_string

def predict_from_user_input_embeddings(embedded_body_string, embedded_headline_string, embedded_link_description_string, model):
  body_array = np.array(embedded_body_string)
  headline_array = np.array(embedded_headline_string)
  link_description_array = np.array(embedded_link_description_string)
  concatenated_array = np.concatenate([body_array, headline_array, link_description_array])
  reshaped_array = concatenated_array.reshape(1, 2304)
  return model.predict(reshaped_array)[0][0]

def calculate_total_impressions_over_total_spend(score):
  TOP_1_PERCENTILE = 250
  return TOP_1_PERCENTILE * score

def calculate_total_result(days_duration, spend_by_day, model_score):
  return int(np.round(days_duration * spend_by_day * model_score, 0))

def calculate_categorical_score(prediction):
    if 0.00 <= prediction < 0.33:
        return "needs work"
    elif 0.33 <= prediction < 0.66:
        return "good"
    elif 0.66 <= prediction <= 1.00:
        return "excellent"
    else:
        return "invalid input"  # Handling values outside 0.00 to 1.00



def calculate_user_scores(user_creative_body, user_headline, user_link_description, days_duration, spend_by_day):
  embedded_body_string, embedded_headline_string, embedded_link_description_string = prepare_user_input(
    user_creative_body,
    user_headline,
    user_link_description
)
  prediction = predict_from_user_input_embeddings(embedded_body_string, embedded_headline_string, embedded_link_description_string, model)
  print(prediction)

  user_input_impressions_over_spend = calculate_total_impressions_over_total_spend(prediction)
  total_impressions = calculate_total_result(days_duration, spend_by_day, user_input_impressions_over_spend)
  categorical_score = calculate_categorical_score(prediction)
  return {
      "categorical_score": categorical_score,
      "total_impressions": total_impressions,
      "user_input_impressions_over_spend": user_input_impressions_over_spend
  }

