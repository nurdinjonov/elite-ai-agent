# JARVIS-X — Multi-AI Agent

```
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗      ██╗  ██╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝      ╚██╗██╔╝
     ██║███████║██████╔╝██║   ██║██║███████╗       ╚███╔╝
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║       ██╔██╗
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║      ██╔╝ ██╗
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝      ╚═╝  ╚═╝
               Multi-AI Agent — v2.0 (JARVIS-X)
```

**JARVIS-X** — OpenRouter, Groq va OpenAI provayderlarini bir joyda boshqaruvchi, 3 xil ish rejimiga ega, o'zbek va ingliz tillarini tushunuvchi zamonaviy AI agent.

---

## Arxitektura

```
FOYDALANUVCHI (Ovoz/Matn)
    → JARVIS CORE (core/jarvis.py)
        → MODE SELECTOR (core/modes.py)     → [FAST | CODE | PRO]
        → AI ROUTER (core/ai_router.py)     → [OpenRouter | Groq | OpenAI | Fallback]
        → LANGUAGE DETECTOR (core/language.py) → [UZ | EN | Auto]
        → VOICE ENGINE (core/voice.py)      → [STT (SpeechRecognition) | TTS (pyttsx3/gTTS)]
```

---

## 3 Ish Rejimi

| Rejim | Rang | Tavsif | Asosiy Provider |
|-------|------|---------|-----------------|
| `fast` | Cyan | Ultra-qisqa javoblar, 2-3 jumla | Groq (eng tez) |
| `code` | Green | Ishlaydigan kod, type hints, best practices | OpenRouter (DeepSeek) |
| `pro` | Magenta | Chuqur tushuntirish, arxitektura dizayni | OpenAI GPT-4o |

---

## Multi-AI Router

Har bir so'rov avtomatik ravishda eng optimal provayderga yo'naltiriladi.  
Agar tanlangan provider ishlamasa — keyingi fallback provayderga o'tiladi.

### Provider prioritetlari

| Rejim | 1-chi | 2-chi | 3-chi |
|-------|-------|-------|-------|
| fast  | Groq  | OpenRouter | OpenAI |
| code  | OpenRouter | Groq | OpenAI |
| pro   | OpenAI | OpenRouter | Groq |

---

## O'rnatish

### Talablar

- Python 3.10+
- pip

### Linux / macOS

```bash
git clone https://github.com/abbosbek112/elite-ai-agent
cd elite-ai-agent
python launchers/setup.py        # paketlar + .env yaratish
nano .env                        # API kalitlarni kiriting
python jarvis_main.py            # ishga tushirish
# yoki
bash launchers/jarvis.sh
```

### Windows

```bat
git clone https://github.com/abbosbek112/elite-ai-agent
cd elite-ai-agent
python launchers\setup.py
notepad .env
launchers\jarvis.bat
```

---

## API Kalitlar

`.env` faylini `.env.example` dan nusxa ko'chiring:

```bash
cp .env.example .env
```

Keyin quyidagi kalitlarni to'ldiring:

| O'zgaruvchi | Qayerdan olish |
|-------------|----------------|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `OPENROUTER_API_KEY` | https://openrouter.ai/keys |
| `GROQ_API_KEY` | https://console.groq.com/keys |

> **Eslatma:** Kamida bitta API kalit bo'lsa yetarli. Bir necha kalit bo'lsa, fallback mexanizmi ishlaydi.

---

## Foydalanish

### Matn rejimi

```
[PRO] > Salom! Python da Fibonacci ketma-ketligini yoz
```

### Slash buyruqlari

```
/mode fast          — Tezkor rejimga o'tish
/mode code          — Kod rejimiga o'tish
/mode pro           — Pro rejimga o'tish (default)
/voice              — Ovoz rejimini toggle qilish
/models             — Barcha modellar ro'yxati
/providers          — Provider holati (API kalitlar bor/yo'q)
/provider groq      — Faqat Groq ishlatish
/provider           — Avtomatik tanlashga qaytish
/ingest <path>      — Hujjat yuklash (knowledge base)
/remember <text>    — Xotiraga saqlash
/recall <query>     — Xotiradan qidirish
/clear              — Ekranni tozalash
/help               — Yordam
/exit               — Chiqish
```

### Ovoz rejimi (ixtiyoriy)

Ovoz uchun qo'shimcha kutubxonalar kerak:

```bash
pip install SpeechRecognition pyttsx3
```

Keyin `.env` faylida:

```
JARVIS_VOICE_ENABLED=true
```

---

## Loyiha Tuzilmasi

```
elite-ai-agent/
├── core/
│   ├── __init__.py          # Eksportlar
│   ├── jarvis.py            # Asosiy orchestrator
│   ├── ai_router.py         # Multi-AI router (OpenRouter/Groq/OpenAI)
│   ├── modes.py             # 3 rejim tizimi (FAST/CODE/PRO)
│   ├── language.py          # Til aniqlash (UZ/EN)
│   └── voice.py             # Ovoz tizimi (STT/TTS)
├── config/
│   ├── models.json          # Model konfiguratsiyasi
│   └── settings.py          # Pydantic settings
├── launchers/
│   ├── jarvis.sh            # Linux/macOS launcher
│   ├── jarvis.bat           # Windows launcher
│   └── setup.py             # Auto setup
├── jarvis_main.py           # Rich terminal UI entry point
├── requirements.txt         # Python paketlar
├── .env.example             # Namuna konfiguratsiya
└── README.md
```

---

## Kengaytirish

### Yangi provider qo'shish

`config/models.json` ga yangi provider bloki qo'shing, keyin `core/ai_router.py` da `_api_keys` va `_call_provider` metodini yangilang.

### Yangi rejim qo'shish

`core/modes.py` da `Mode` enum ga yangi qiymat, `_SYSTEM_PROMPTS`, `_PREFERRED_PROVIDERS` va `_RECOMMENDED_MODELS` lug'atlariga mos yozuv qo'shing.

---

## Litsenziya

MIT — erkin foydalaning, kengaytiring va tarqating.