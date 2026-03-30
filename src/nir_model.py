import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer
import numpy as np

# ✅ NIR_RuBERT_LSTM v3.2 (PHISHING версия)
class NIR_RuBERT_LSTM_v3(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModel.from_pretrained('cointegrated/rubert-tiny')
        self.lstm = nn.LSTM(312, 128, bidirectional=True, batch_first=True, dropout=0.2)
        self.pooling = nn.Linear(880, 256)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(256, 3)
    
    def mean_pooling(self, hidden_states, attention_mask):
        input_mask_expanded = attention_mask.unsqueeze(-1).float()
        sum_embeddings = torch.sum(hidden_states * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask
    
    def forward(self, input_ids, attention_mask):
        bert_out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_token = bert_out.last_hidden_state[:, 0, :]
        mean_pool = self.mean_pooling(bert_out.last_hidden_state, attention_mask)
        
        lstm_out, (h_n, _) = self.lstm(bert_out.last_hidden_state)
        lstm_fwd = h_n[-2, :, :]
        lstm_bwd = h_n[-1, :, :]
        
        combined = torch.cat([cls_token, mean_pool, lstm_fwd, lstm_bwd], dim=1)
        pooled = torch.relu(self.pooling(combined))
        pooled = self.dropout(pooled)
        return self.classifier(pooled)

# ✅ Инициализация модели + predict
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained('cointegrated/rubert-tiny')
model = NIR_RuBERT_LSTM_v3().to(device)

def load_model(model_path):
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    print(f"✅ Модель загружена: F1={checkpoint.get('f1_macro', 'N/A')}")
    return model

def nir_phishing_predict(text):
    model.eval()
    inputs = tokenizer(
        str(text), return_tensors='pt', padding=True, 
        truncation=True, max_length=128
    )
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probs = torch.softmax(logits, dim=-1)[0].cpu().numpy()
    
    result = dict(zip(['✅ REAL', '❌ FAKE', '🚨 PHISHING'], probs.round(3)))
    return result

# Загрузка модели (вызывать при старте)
# model = load_model('NIR_phishing_v3.2_best_F1_0.849.pth')
