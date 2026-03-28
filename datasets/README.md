# 📊 NIR Phishing Datasets

## Состав
| Файл | Примеры | Классы | Описание |
|------|---------|--------|----------|
| `NIR_phishing_train.csv` | **1280** | 0=REAL, 1=FAKE, 2=PHISHING | Обучающая выборка |
| `NIR_phishing_test.csv`  | **321**  | 0=REAL, 1=FAKE, 2=PHISHING | Тестовая выборка |

## Распределение классов 
REAL (0): 424 (33%)
FAKE (1): 456 (36%)
PHISHING (2): 400 (31%)
## Формат CSV
text,label_num,textlabel
"нато и сербия...",0,"REAL"
"BTC x10! Депозит...",2,"PHISHING"

**F1_macro=0.849**

📊 1280 train + 321 test SMS

PHISHING: 400+121 примеров

REAL: 424+106 примеров

FAKE: 456+114 примеров

[![Dataset](https://img.shields.io/badge/Dataset-1601-blue.svg)](datasets/)
