# 🚨 NIR_PHISHING Detector v3.2 (F1=0.849)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![F1=0.849](https://img.shields.io/badge/F1_macro-0.849-brightgreen.svg)](https://huggingface.co/spaces)
[![Gradio](https://img.shields.io/badge/Gradio-WebUI-green.svg)](https://gradio.app)

**НИР "Детектор фишинговых сообщений" | МИСИС 2026 | Ana B**

Гибридная модель **RuBERT-tiny + BiLSTM** для классификации SMS:
- 🚨 **PHISHING**: 99.5% (фишинг, мошенничество)
- ✅ **REAL**: ~84% (настоящие новости)
- ❌ **FAKE**: ~84% (фейковые новости)

**F1_macro = 0.849** (+6.1% к baseline)

## 🎯 ДЕМО
[![NIR Demo](demo_qr.png)](https://huggingface.co/spaces/ana-bee/NIR_phishing_detector)

## 🚀 Быстрый старт
```bash
pip install -r requirements.txt
python app.py  # Gradio UI → public link!
```

## 📊 РЕЗУЛЬТАТЫ
| Метрика | NIR_v3.2 | RuBERT-tiny | Улучшение |
|---------|----------|-------------|-----------|
| **F1_macro** | **0.849** | 0.800 | **+6.1%** |
| PHISHING F1 | **0.995** | 0.995 | 0% |
| REAL/FAKE F1 | **~0.84** | 0.703 | **+19%** |

## 🔧 Production API
```python
from nir_model import nir_phishing_predict
result = nir_phishing_predict("BTC x10! Вложи 1000$ → 10k!")
# → {'✅ REAL': 0.01, '❌ FAKE': 0.02, '🚨 PHISHING': 0.97}
```

## 📁 Структура проекта
Разработка фишинг модели (RUBert + LSTM)
NIR_phishing_detector/
├── nir_model.py # Модель + predict
├── app.py # Gradio UI
├── NIR_phishing_v3.2_best_F1_0.849.pth # Твоя модель!
├── requirements.txt
├── README.md
└── LICENSE # MIT


## 🎓 НИР МИСИС 2026
**Ana B** | Институт Компьютерных Наук | Наука о данных | Защита: июнь 2026

[MIT License](LICENSE) © 2026 Ana Bee
