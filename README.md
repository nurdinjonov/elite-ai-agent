# JARVIS-X — Avtonom AI Agent

JARVIS-X — Smart Life Assistant, Multi-AI Orchestration, Memory tizimi, RAG va ko'plab vositalar bilan jihozlangan to'liq avtonom AI Agent.

## Xususiyatlar

- 🤖 **Multi-AI Orchestration** — OpenRouter, Groq provayderlarini qo'llab-quvvatlaydi
- 🧠 **Memory System** — Qisqa va uzoq muddatli xotira (ChromaDB)
- 📚 **RAG** — Lokal hujjatlardan bilim olish
- 🔧 **Tools** — Web qidiruv, fayl boshqaruvi, kod bajarish, terminal
- 🎓 **Life Assistant** — Dars jadvali, uy vazifalari, kundalik reja
- 🌐 **Ko'p tilli** — O'zbek, Ingliz, Rus tillarini avtomatik aniqlaydi
- 🎙 **Voice** (ixtiyoriy) — Whisper STT + piper TTS

## Tezkor ishga tushirish

```bash
# 1. Bog'liqliklarni o'rnatish
pip install -r requirements.txt

# 2. API kalitlarini sozlash
cp .env.example .env
# .env faylini tahrirlang va API kalitlarini kiriting

# 3. JARVIS-X ni ishga tushirish
python start.py

# Yoki Life Assistant rejimida
python start.py --life-only

# Yoki bash skript orqali (Linux/macOS)
./jarvis
```

## Rejimlar

| Rejim | Buyruq | Tavsif |
|-------|--------|--------|
| PRO | `/pro` | Batafsil, tadqiqot darajasidagi javoblar |
| CODE | `/code` | Kod yozishga ixtisoslashgan |
| FAST | `/fast` | Tez, qisqa javoblar |

## Arxitektura

```
elite-ai-agent/
├── jarvis_life.py         # Life Assistant CLI
├── start.py               # Asosiy ishga tushirish nuqtasi
├── jarvis                 # Linux/macOS launcher
├── jarvis.bat             # Windows launcher
│
├── core/                  # AI Agent modullari
│   ├── jarvis.py          # Asosiy Orchestrator
│   ├── ai_router.py       # Multi-AI yo'naltiruvchi
│   ├── modes.py           # Rejim tizimi
│   ├── language.py        # Til aniqlovchi
│   ├── memory.py          # Xotira tizimi
│   ├── tools.py           # Vositalar reestri
│   ├── rag.py             # RAG tizimi
│   └── voice.py           # Ovoz tizimi
│
├── life/                  # Life Assistant modullari
│   ├── models.py          # Pydantic data modellari
│   ├── storage.py         # JSON saqlash
│   ├── scheduler.py       # Dars jadvali
│   ├── homework.py        # Uy vazifalari
│   ├── daily_planner.py   # Kundalik reja
│   └── reminders.py       # Eslatmalar
│
├── tools/                 # Tashqi vositalar
│   ├── web_search.py      # DuckDuckGo qidiruv
│   ├── file_manager.py    # Fayl operatsiyalari
│   ├── code_executor.py   # Kod bajarish
│   └── terminal.py        # Terminal buyruqlari
│
├── config/                # Sozlamalar
│   ├── models.json        # AI model konfiguratsiyasi
│   ├── settings.json      # Umumiy sozlamalar
│   └── schedule_config.json  # Jadval sozlamalari
│
└── data/                  # Ma'lumotlar
    ├── memory/            # ChromaDB saqlash
    ├── documents/         # RAG hujjatlar
    └── schedule/          # Jadval JSON fayllari
```

## Life Assistant buyruqlari

### Jadval
| Buyruq | Tavsif |
|--------|--------|
| `/schedule` | Bugungi dars jadvali |
| `/week` | Haftalik dars jadvali |
| `/add_class <fan> <kun> <boshlanish> <tugash> [xona]` | Yangi dars qo'shish |
| `/remove_class <id>` | Darsni o'chirish |
| `/load_sample` | Namuna jadval yuklash |

### Uy Vazifalari
| Buyruq | Tavsif |
|--------|--------|
| `/homework` | Bajarilmagan uy vazifalari |
| `/add_hw <fan> <tavsif> [muddat] [ustuvorlik]` | Yangi uy vazifasi qo'shish |
| `/done_hw <id>` | Uy vazifasini bajarilgan deb belgilash |

### Vazifalar
| Buyruq | Tavsif |
|--------|--------|
| `/tasks` | Barcha bajarilmagan vazifalar |
| `/add_task <sarlavha> [tavsif] [muddat]` | Yangi vazifa qo'shish |
| `/done_task <id>` | Vazifani bajarilgan deb belgilash |

### Reja va Eslatmalar
| Buyruq | Tavsif |
|--------|--------|
| `/plan` | Bugungi optimal reja |
| `/reminders` | Barcha eslatmalar |
| `/stats` | Statistika |
| `/summary` | Kun oxiri xulosasi |

## Sozlash

### .env fayli
```env
# AI Providers
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Life Assistant
JARVIS_WAKE_UP_TIME=07:00
JARVIS_CLASS_ALERT_MINUTES=15

# Memory
CHROMA_PERSIST_DIR=./data/memory
```

## Ma'lumotlar Modellari

- **ClassSchedule** — Dars jadvali (fan, kun, vaqt, xona, o'qituvchi)
- **Homework** — Uy vazifasi (fan, tavsif, muddat, ustuvorlik)
- **Task** — Umumiy vazifa (sarlavha, kategoriya, muddat)
- **DailyPlan** — Kundalik reja (darslar, o'qish bloklari, dam olish)