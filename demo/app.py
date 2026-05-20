import gradio as gr
import torch
import os
from huggingface_hub import hf_hub_download
from nir_model import nir_phishing_predict, model, device, load_model

# --- НАСТРОЙКИ HUGGING FACE ---
REPO_ID = "jesthy/NIR_phishing_v3.2"
FILENAME = "NIR_phishing_v3.2_best_F1_0.849.pth"

def initialize_model():
    """Скачивает веса с HF и загружает их в модель"""
    try:
        print(f"🔄 Проверка наличия модели в {REPO_ID}...")
        # Скачивает файл во временный кэш или берет уже скачанный
        model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
        
        print(f"✅ Файл найден: {model_path}")
        # Загружаем веса через функцию load_model
        return load_model(model_path)
    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        return None

# Инициализация при запуске сервера
model = initialize_model()

def gradio_predict(text):
    if not text.strip():
        return "⚠️ **Ошибка:** Введите SMS для анализа!"
    
    if model is None:
        return "❌ **Ошибка системы:** Модель не была загружена. Проверьте соединение с Hugging Face."

    # Вызываем твою функцию предсказания
    result = nir_phishing_predict(text)
    
    # Определяем лучший класс
    prediction = max(result, key=result.get)
    confidence = max(result.values())
    
    # Красивое оформление вероятностей списком
    probs_md = "\n".join([f"* **{k}**: {v:.2%}" for k, v in result.items()])
    
    return f"""### 🎯 РЕЗУЛЬТАТ NIR_PHISHING v3.2 (F1=0.849)

📱 SMS: `{text[:100]}{'...' if len(text) > 100 else ''}`

🚨 Предсказание: {prediction}  
💯 Уверенность: {confidence:.1%}

📊 Детали вероятностей:
{probs_md}
"""

# --- ИНТЕРФЕЙС GRADIO ---
demo = gr.Interface(
    fn=gradio_predict,
    inputs=gr.Textbox(
        label="📱 Вставьте SMS для проверки", 
        placeholder="Пример: Сбербанк: подтвердите данные для вывода 5000₽",
        lines=3
    ),
    outputs=gr.Markdown(),
    title="🚨 NIR_PHISHING Detector v3.2",
    description="""
    НИР МИСИС 2026 | Ana B
    
    Гибридная модель на базе RuBERT-tiny + BiLSTM для защиты пользователей от мошенничества.
    
    Метрики качества:
     PHISHING F1: 0.995
     REAL/FAKE F1: ~0.84
     F1_macro: 0.849
    """,
    examples=[
        ["BTC x10! Депозит 1000$ → 10k! t.me/wallet"],
        ["Сбербанк: подтвердите данные для вывода 5000₽"],
        ["нато и сербия достигли соглашения по урану"],
        ["Привет! Завтра в 10:00 встреча в библиотеке."],
    ],
    theme=gr.themes.Soft(),
    allow_flagging="never"
)

if __name__ == "__main__":
    # share=True создаст публичную ссылку на 72 часа
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
