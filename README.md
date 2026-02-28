# elite-ai-agent

JARVIS-X AI Agent — Smart Life Assistant bilan jihozlangan aqlli hayot yordamchisi.

## Smart Life Assistant

Real vaqtda dars jadvali monitoring, homework tracking, kundalik rejalashtirish va proaktiv eslatmalar tizimi.

### Ishga tushirish

```bash
pip install -r requirements.txt
python jarvis_life.py
```

### Buyruqlar

#### Jadval
| Buyruq | Tavsif |
|--------|--------|
| `/schedule` | Bugungi dars jadvali |
| `/week` | Haftalik dars jadvali |
| `/add_class <fan> <kun> <boshlanish> <tugash> [xona]` | Yangi dars qo'shish |
| `/remove_class <id>` | Darsni o'chirish |
| `/load_sample` | Namuna jadval yuklash |

#### Uy Vazifalari
| Buyruq | Tavsif |
|--------|--------|
| `/homework` | Bajarilmagan uy vazifalari |
| `/add_hw <fan> <tavsif> [muddat] [ustuvorlik]` | Yangi uy vazifasi qo'shish |
| `/done_hw <id>` | Uy vazifasini bajarilgan deb belgilash |

#### Vazifalar
| Buyruq | Tavsif |
|--------|--------|
| `/tasks` | Barcha bajarilmagan vazifalar |
| `/add_task <sarlavha> [tavsif] [muddat]` | Yangi vazifa qo'shish |
| `/done_task <id>` | Vazifani bajarilgan deb belgilash |

#### Reja va Eslatmalar
| Buyruq | Tavsif |
|--------|--------|
| `/plan` | Bugungi optimal reja |
| `/reminders` | Barcha eslatmalar |
| `/stats` | Statistika |
| `/summary` | Kun oxiri xulosasi |

### Arxitektura

```
life/
├── __init__.py
├── models.py          # Pydantic data models
├── storage.py         # JSON fayl asosidagi saqlash
├── scheduler.py       # Smart Calendar & Class Monitor
├── homework.py        # Homework & Task Manager
├── daily_planner.py   # Intelligent Daily Routine Builder
└── reminders.py       # Proactive Reminder Engine

data/
└── schedule/          # JSON saqlash katalogi

config/
└── schedule_config.json  # Default sozlamalar va namuna jadval
```

### Ma'lumotlar Modellari

- **ClassSchedule** — Dars jadvali (fan, kun, vaqt, xona, o'qituvchi)
- **Homework** — Uy vazifasi (fan, tavsif, muddat, ustuvorlik)
- **Task** — Umumiy vazifa (sarlavha, kategoriya, muddat)
- **DailyPlan** — Kundalik reja (darslar, o'qish bloklari, dam olish)