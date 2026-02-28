# JARVIS-X — Ilg'or Sun'iy Intellekt Agenti

```
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗    ██╗  ██╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ╚██╗██╔╝
     ██║███████║██████╔╝██║   ██║██║███████╗     ╚███╔╝
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║     ██╔██╗
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ██╔╝ ██╗
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝    ╚═╝  ╚═╝
         Advanced AI Agent  |  v2.0  |  Multi-Provider
```

**JARVIS-X** — ko'p provayderli, ko'p tilli, ovoz qo'llab-quvvatlanadigan,
LangGraph asosidagi ilg'or AI agenti. O'zbek va ingliz tillarini avtomatik
aniqlaydi; OpenAI, Groq va OpenRouter orqali ishlaydi.

---

## Arxitektura

```
FOYDALANUVCHI (Ovoz / Matn)
    → JARVIS CORE (jarvis.py)
        ├── MODE SELECTOR (modes.py)      → [FAST | CODE | PRO]
        ├── AI ROUTER (ai_router.py)      → [OpenRouter | Groq | OpenAI | Fallback]
        ├── LANGUAGE DETECTOR (language.py) → [UZ | EN | Auto]
        ├── VOICE ENGINE (voice.py)       → [STT (SpeechRecognition) | TTS (pyttsx3/gTTS)]
        ├── TOOL ENGINE (tools/)          → [Web | Code | File | Terminal]
        ├── MEMORY ENGINE (memory/)       → [Short-term | Long-term]
        └── KNOWLEDGE ENGINE (knowledge/) → [RAG + ChromaDB]
```

---

## 3 Ta Ishlash Rejimi

| Rejim | Tavsif | Provider | Foydalanish |
|-------|--------|----------|-------------|
| **FAST** | Ultra-tez, qisqa javoblar | Groq (llama-3.1-8b) | Oddiy savollar |
| **CODE** | Kod yozish mutaxassisi | OpenRouter (deepseek-coder) | Dasturlash |
| **PRO** | Chuqur tahlil, arxitektura | OpenAI GPT-4o | Murakkab vazifalar |

Rejim almashtirish: `/mode fast` | `/mode code` | `/mode pro`

---

## Multi-AI Router

JARVIS-X bir vaqtning o'zida uchta AI provayderini boshqaradi:

| Provider | Endpoint | Xususiyati |
|----------|----------|------------|
| **Groq** | `api.groq.com` | Eng tez (millisekund) |
| **OpenRouter** | `openrouter.ai` | Eng ko'p modellar |
| **OpenAI** | `api.openai.com` | Eng sifatli |

**Fallback mexanizmi:** Agar birinchi provider ishlamasa, avtomatik keyingisiga o'tadi.

---

## Til Qo'llab-quvvatlash

- **O'zbek tili** — lotin va kirill yozuvini aniqlaydi
- **Ingliz tili** — standart
- **Avtomatik aniqlash** — heuristic marker tahlili asosida

---

## Ovoz Tizimi (Ixtiyoriy)

| Komponent | Kutubxona | Tavsif |
|-----------|-----------|--------|
| **STT** | SpeechRecognition | Mikrofon → Matn |
| **TTS (offline)** | pyttsx3 | Matn → Ovoz (internet siz) |
| **TTS (online)** | gTTS + playsound | Matn → Ovoz (internet kerak) |

Ovoz kutubxonalari **ixtiyoriy**. O'rnatilmagan holda agent matn rejimida ishlaydi.

---

## O'rnatish

### Talablar

- Python 3.11+
- API kalitlari: OpenAI, Groq, OpenRouter (kamida bittasi)

### Linux / macOS

```bash
# 1. Loyihani yuklab oling
git clone https://github.com/abbosbek112/elite-ai-agent
cd elite-ai-agent

# 2. Avtomatik o'rnatish
python launchers/setup.py

# 3. API kalitlarni sozlash
cp .env.example .env
nano .env   # API kalitlarni kiriting

# 4. Ishga tushirish
./launchers/jarvis.sh
# yoki
python jarvis_main.py
```

### Windows

```bat
# 1. Loyihani yuklab oling
git clone https://github.com/abbosbek112/elite-ai-agent
cd elite-ai-agent

# 2. Avtomatik o'rnatish
python launchers\setup.py

# 3. API kalitlarni sozlang
copy .env.example .env
notepad .env

# 4. Ishga tushirish
launchers\jarvis.bat
```

### Ovoz Kutubxonalarini O'rnatish (Ixtiyoriy)

```bash
pip install SpeechRecognition pyttsx3
# Yoki online TTS uchun:
pip install gTTS playsound
```

---

## API Kalitlarini Olish

| Servis | Havola | Narxi |
|--------|--------|-------|
| OpenAI | https://platform.openai.com/api-keys | Pullik |
| OpenRouter | https://openrouter.ai/keys | Bepul modellar mavjud |
| Groq | https://console.groq.com/keys | Bepul tier mavjud |

---

## Foydalanish Misollari

```
[PRO] You: Python da async/await qanday ishlaydi?
[PRO] You: /mode fast
[FAST] You: Python nima?
[FAST] You: /mode code
[CODE] You: FastAPI bilan REST API yoz
[CODE] You: /voice
[CODE] You: /providers
[CODE] You: /provider groq
[CODE] You: /models
[CODE] You: /help
```

---

## Loyiha Tuzilmasi

```
elite-ai-agent/
├── core/
│   ├── __init__.py          # Modul eksportlari
│   ├── jarvis.py            # Asosiy orchestrator
│   ├── ai_router.py         # Multi-AI provider router
│   ├── modes.py             # 3 ta rejim tizimi
│   ├── language.py          # Til aniqlash
│   └── voice.py             # STT + TTS
├── config/
│   ├── models.json          # AI model konfiguratsiyalari
│   └── settings.py          # Pydantic sozlamalar
├── launchers/
│   ├── jarvis.sh            # Linux ishga tushiruvchi
│   ├── jarvis.bat           # Windows ishga tushiruvchi
│   └── setup.py             # Avtomatik o'rnatish
├── jarvis_main.py           # Asosiy entry point (rich UI)
├── requirements.txt         # Kutubxonalar ro'yxati
└── .env.example             # API kalitlar namunasi
```

---

## Kengaytirish

### Yangi Provider Qo'shish

1. `config/models.json` ga yangi provider qo'shing
2. `core/ai_router.py` da `_call_<provider>()` metodi yarating
3. `_call_provider()` metodiga yangi provaiderni qo'shing

### Yangi Rejim Qo'shish

1. `core/modes.py` da `Mode` enum ga yangi qiymat qo'shing
2. `_SYSTEM_PROMPTS` va `_PREFERRED_PROVIDERS` lug'atlarini yangilang
3. `config/models.json` da `default_provider_priority` ni yangilang

---

## Litsenziya

MIT License — bepul foydalaning, o'zgartiring va tarqating.