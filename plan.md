# Детальный план разработки CRM-системы для образовательной сферы (Solo Edition)

> **Проект:** CRM/ERP для музыкальных школ, языковых центров и тренинговых студий  
> **Цель:** создать рабочую, масштабируемую систему с фокусом на расписание, финансы, личные кабинеты и управление персоналом  
> **Ограничения:** 1 разработчик, хостинг NetAngels, интеграция с 1С отложена до крупного обновления v2.0+  
> **Формат:** Markdown-документ для ведения в репозитории и трекере задач

---

## 📋 Оглавление

1. [Обзор проекта и требования](#-обзор-проекта-и-требования)
2. [Технологический стек](#-технологический-стек)
3. [Архитектура системы](#-архитектура-системы)
4. [Структура базы данных](#-структура-базы-данных)
5. [План разработки по фазам](#-план-разработки-по-фазам)
6. [Структура проекта](#-структура-проекта)
7. [API и интеграции](#-api-и-интеграции)
8. [Безопасность и права доступа](#-безопасность-и-права-доступа)
9. [Тестирование (прагматичный подход)](#-тестирование-прагматичный-подход)
10. [Деплой на NetAngels](#-деплой-на-netangels)
11. [Стратегия для соло-разработчика](#-стратегия-для-соло-разработчика)
12. [Дорожная карта и метрики](#-дорожная-карта-и-метрики)
13. [Приложения](#-приложения)

---

## 🔍 Обзор проекта и требования

### Бизнес-требования
| Приоритет | Требование | Описание |
|-----------|------------|----------|
| 🔴 Высокий | Управление расписанием | Гибкие слоты, проверка конфликтов, уведомления, календарь |
| 🔴 Высокий | Финансовый модуль | Счета, платежи, рассрочка, контроль долгов, интеграция с эквайрингом |
| 🔴 Высокий | Личные кабинеты | Разные интерфейсы для студента, преподавателя, менеджера, владельца |
| 🟡 Средний | Управление персоналом | База преподавателей, графики, договоры, расчёт зарплат |
| 🟡 Средний | Бухгалтерия и отчёты | Выручка, задолженности, экспорт в Excel/CSV |
| ⏳ Отложено | Интеграция с 1С | Вынесено в обновление v2.0+ (требует отдельного бюджета и времени) |

### Нефункциональные требования
- **Масштабируемость:** от 1 организации до 50+ без пересмотра архитектуры
- **Производительность:** отклик API <500мс, страница <2с на 3G
- **Безопасность:** защита ПДн, ролевая модель, аудит критических действий
- **Поддержка:** Python 3.12, PostgreSQL 14, совместимость с NetAngels VPS

---

## ⚙️ Технологический стек

| Компонент | Выбор | Обоснование |
|-----------|-------|-------------|
| **Backend** | Python 3.12 + FastAPI | Асинхронность, автодокументация, типизация, лёгкость поддержки |
| **ORM** | SQLAlchemy 2.0 + Alembic | Стабильность, поддержка асинхронных запросов, миграции |
| **Валидация** | Pydantic v2 | Строгая типизация, генерация OpenAPI-схем |
| **Фоновые задачи** | Celery + Redis | Уведомления, расчёт зарплат, очистка просроченных счетов |
| **Frontend** | Vue 3 + Composition API + Vite + Pinia | Быстрая разработка, реактивность, готовая экосистема |
| **UI-кит** | Element Plus | Таблицы, календари, формы из коробки — экономия 30-40% времени |
| **База данных** | PostgreSQL 14 | JSONB, UUID, full-text search, надёжность, поддержка до 2026+ |
| **Кеширование** | Redis | Сессии, rate-limiting, очереди Celery |
| **Веб-сервер** | Nginx + Uvicorn (gunicorn workers) | Стандарт для FastAPI, простота настройки на VPS |

---

## ️ Архитектура системы

```
─────────────────────────────────────┐
│            Client Layer              │
│  ┌──────────┐  ┌──────────┐         │
│  │ Vue 3 SPA│  │ Admin UI │         │
│  │ (PWA)    │  │          │         │
│  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼───────────────┘
        │ HTTPS/WS     │
        ▼              ▼
┌─────────────────────────────────────┐
│          Nginx (reverse proxy)      │
│  • SSL termination                  │
│  • Static files (Vue build)         │
│  • Rate limiting / CORS             │
└────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│        FastAPI (Python 3.12)        │
│  • Modular Monolith                 │
│  • RBAC + JWT Auth                  │
│  • Pydantic validation              │
───────┬────────────────────────────┘
        │               │
        ▼               ▼
┌──────────────┐  ┌──────────────────┐
│ PostgreSQL 14│  │ Redis + Celery   │
│ • Data       │  │ • Tasks          │
│ • JSONB      │  │ • Cache          │
│ • UUID       │  │ • Queues         │
└──────────────┘  └──────────────────┘
```

> **Примечание:** Стартуем с **модульного монолита**. Микросервисы не нужны до 10k+ активных пользователей.

---

## 🗃️ Структура базы данных (ключевые сущности)

```sql
-- Организации
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    settings JSONB DEFAULT '{}',
    timezone VARCHAR(50) DEFAULT 'Europe/Moscow',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Пользователи
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255),
    role VARCHAR(50) NOT NULL, -- student, teacher, manager, admin, owner
    profile_data JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Курсы
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2),
    duration_weeks INTEGER,
    lessons_count INTEGER,
    settings JSONB DEFAULT '{}',
    is_archived BOOLEAN DEFAULT false
);

-- Расписание
CREATE TABLE time_slots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    day_of_week INTEGER,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room VARCHAR(100),
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id),
    teacher_id UUID REFERENCES users(id),
    slot_id UUID REFERENCES time_slots(id),
    scheduled_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    attendees JSONB DEFAULT '[]'
);

-- Финансы
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    due_date DATE,
    payment_method VARCHAR(50),
    external_id VARCHAR(100)
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID REFERENCES invoices(id),
    amount DECIMAL(10,2) NOT NULL,
    paid_at TIMESTAMPTZ DEFAULT NOW(),
    transaction_id VARCHAR(100)
);

CREATE TABLE installments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID REFERENCES invoices(id),
    total_parts INTEGER NOT NULL,
    paid_parts INTEGER DEFAULT 0,
    next_due_date DATE,
    auto_reminder BOOLEAN DEFAULT true
);

-- Персонал и зарплаты
CREATE TABLE staff_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    teacher_id UUID REFERENCES users(id),
    contract_type VARCHAR(20),
    rate_per_hour DECIMAL(8,2),
    percent_of_revenue DECIMAL(5,2),
    tax_settings JSONB DEFAULT '{}'
);

CREATE TABLE salary_calculations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    teacher_id UUID REFERENCES users(id),
    period_start DATE,
    period_end DATE,
    lessons_count INTEGER,
    total_hours DECIMAL(6,2),
    gross_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    net_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'draft'
);

-- Аудит
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    organization_id UUID,
    user_id UUID,
    action VARCHAR(50),
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_lessons_scheduled ON lessons(scheduled_at) WHERE status = 'scheduled';
CREATE INDEX idx_invoices_status ON invoices(status, due_date);
CREATE INDEX idx_users_org_role ON users(organization_id, role);
```

---

## 📅 План разработки по фазам

###  Фаза 0: Подготовка (1-2 недели)
- [ ] Инициализация репозитория, `pre-commit` (black, isort, ruff)
- [ ] FastAPI + SQLAlchemy + Alembic boilerplate
- [ ] Базовая БД: организации, пользователи, аутентификация (JWT)
- [ ] Настройка Vue 3 + Element Plus + Vite
- [ ] Базовый CI: запуск тестов и линтеров при push

### 🔹 Фаза 1: Ядро + Расписание (3-6 недель)
- [ ] RBAC middleware (student/teacher/manager/admin/owner)
- [ ] CRUD организаций и пользователей, импорт CSV
- [ ] Временные слоты, занятия, проверка конфликтов
- [ ] Календарь администратора (Week/Month)
- [ ] Личный кабинет студента (расписание, история, профиль)
- [ ] Кабинет преподавателя (свои занятия, список студентов)

### 🔹 Фаза 2: Финансы и платежи (7-10 недель)
- [ ] Счета, статусы, привязка к курсам
- [ ] Интеграция эквайринга (ЮKassa / CloudPayments) + webhooks
- [ ] Пакетные предложения (N занятий со скидкой)
- [ ] Рассрочка: части, напоминания, отслеживание остатка
- [ ] Финансовый дашборд: выручка, долги, способы оплаты
- [ ] Экспорт отчётов в CSV/Excel

### 🔹 Фаза 3: Персонал и зарплаты (11-14 недель)
- [ ] Профили преподавателей: квалификация, договоры, ставки
- [ ] Гибкие тарифы: почасовая, %, фикс
- [ ] Автоматический расчёт зарплат за период
- [ ] Учёт налогов/комиссий, генерация ведомостей
- [ ] Система задач: назначение, приоритеты, комментарии, @mentions

### 🔹 Фаза 4: Улучшения и стабилизация (15-18 недель)
- [ ] Умная запись (предложение соседних слотов)
- [ ] Массовое создание занятий по шаблону
- [ ] Email/SMS/Telegram уведомления с шаблонами
- [ ] 2FA для владельцев/админов
- [ ] Детальный аудит-лог, бэкапы, мониторинг ошибок
- [ ] Нагрузочные тесты, оптимизация запросов, багфикс

### 🔹 Фаза 5: Интеграции и экосистема (19-22 недели)
- [ ] Публичное REST API + OpenAPI документация
- [ ] Webhooks (оплата, запись, отмена)
- [ ] Синхронизация с Google Calendar / iCal
- [ ] PWA-режим, офлайн-просмотр расписания
- [ ] Подготовка к v2.0: архитектура под 1С, масштабирование

> ⏳ **Интеграция с 1С вынесена в отдельный эпик v2.0+**. На старте реализуем только выгрузку CSV/Excel для бухгалтерии.

---

## 📁 Структура проекта

```
crm-edu/
├── backend/
│   ├── app/
│   │   ├── core/          # config, security, db session
│   │   ├── api/           # routers, dependencies
│   │   ├── modules/       # auth, users, schedule, finance, staff, tasks
│   │   ├── workers/       # celery tasks, beat schedule
│   │   └── utils/         # logger, validators, helpers
│   ├── alembic/           # migrations
│   ├── tests/             # pytest, httpx, factories
│   ├── pyproject.toml
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── api/           # axios, interceptors
│   │   ├── components/    # base UI (Element Plus wrappers)
│   │   ├── views/         # pages (Dashboard, Schedule, Finance...)
│   │   ├── stores/        # pinia
│   │   ├── router/        # vue-router, guards
│   │   └── utils/         # formatters, i18n
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
├── deploy/                # scripts для NetAngels (systemd, nginx)
├── .github/workflows/     # simple CI (lint + test)
└── README.md
```

---

## 🔌 API и интеграции

### Внутренний API (FastAPI)
```python
@router.post("/lessons", response_model=LessonOut)
async def create_lesson(
    data: LessonCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.has_permission("schedule.create"):
        raise HTTPException(403, "Недостаточно прав")
    
    if await schedule_service.check_conflicts(db, data):
        raise HTTPException(409, "Конфликт в расписании")
    
    lesson = await schedule_service.create(db, data)
    notify_participants.delay(lesson.id)
    return lesson
```

### Внешние интеграции (v1)
| Сервис | Назначение | Метод |
|--------|------------|-------|
| ЮKassa / CloudPayments | Приём платежей | Webhook + REST |
| SMS.ru / Unisender | Уведомления | REST API |
| Telegram Bot API | Оповещения | Webhook |
| Google Calendar | Синхронизация | OAuth 2.0 |
| Экспорт CSV/Excel | Бухгалтерия | Файловая выгрузка |

> 🔸 **1С:Enterprise** — подключение в v2.0 через HTTP API или файловый обмен.

---

##  Безопасность и права доступа

### Гибридная модель RBAC + ABAC
```python
class PermissionChecker:
    MAP = {
        "schedule.view": ["student", "teacher", "manager", "admin", "owner"],
        "schedule.create": ["manager", "admin", "owner"],
        "finance.view": ["manager", "admin", "owner"],
        "staff.salary.calculate": ["admin", "owner"],
    }
    
    @staticmethod
    def check(user: User, perm: str, resource=None) -> bool:
        if user.role not in PermissionChecker.MAP.get(perm, []):
            return False
        if perm == "finance.view" and resource:
            return resource.organization_id == user.organization_id
        return True
```

### Чеклист
- [ ] JWT + refresh tokens в HTTP-only cookie
- [ ] Хеширование: Argon2 / bcrypt
- [ ] Rate limiting на `/auth/*`
- [ ] CORS только на домен приложения
- [ ] Шифрование ПДн в БД (на уровне приложения)
- [ ] Аудит-лог изменений критических сущностей

---

## 🧪 Тестирование (прагматичный подход)

| Тип | Инструменты | Покрытие |
|-----|-------------|----------|
| Unit | `pytest`, `pytest-asyncio`, `factory_boy` | Бизнес-логика сервисов |
| API | `httpx`, `TestClient` | Эндпоинты, валидация, права |
| E2E | `Playwright` | Критические сценарии (запись → оплата → уведомление) |
| Безопасность | `bandit`, `pip-audit`, `ruff` | Статический анализ |

**Правило для соло-разработчика:**  
Пишем тесты только на сложную логику (расчёт зарплат, конфликты расписания, webhooks). Простые CRUD покрываем минимальными smoke-тестами.

---

## 🚀 Деплой на NetAngels

### Базовая схема (VPS)
1. **ОС:** Ubuntu 22.04/24.04 LTS
2. **Системные пакеты:** `python3.12`, `python3.12-venv`, `postgresql-14`, `redis-server`, `nginx`, `certbot`
3. **Backend:** виртуальное окружение, `pip install -r requirements.txt`, запуск через `gunicorn` с `uvicorn.workers.UvicornWorker`
4. **Frontend:** `npm run build`, статика раздается nginx
5. **Процессы:** `systemd` юниты для `gunicorn` и `celery worker/beat`
6. **Бэкапы:** cron-скрипт `pg_dump` + `rsync` на внешний диск/облако (1 раз в сутки)
7. **Мониторинг:** `journalctl`, `nginx access/error log`, опционально `UptimeRobot` для healthcheck

### Пример systemd (backend)
```ini
[Unit]
Description=CRM Edu Backend
After=network.target postgresql.service redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/crm-edu/backend
Environment="PATH=/var/www/crm-edu/backend/venv/bin"
ExecStart=/var/www/crm-edu/backend/venv/bin/gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker -w 3 -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

> При росте нагрузки мигрируем на выделенный сервер или облако с Docker/K8s. На старте — классический LEMP-подобный стек.

---

## 👤 Стратегия для соло-разработчика

1. **Не усложнять архитектуру.** Модульный монолит > микросервисы.
2. **Использовать готовые UI-компоненты.** Element Plus сэкономит недели верстки.
3. **Автоматизировать рутину.** `pre-commit`, `ruff`, `black`, шаблоны задач, скрипты деплоя.
4. **Делить на недели.** Каждый спринт — законченный функционал, который можно показать/протестировать.
5. **Приоритет: ценность > красота.** Сначала работает, потом полируем UI/UX.
6. **Фиксировать решения.** Вести `DECISIONS.md`, чтобы не переосмыслять одно и то же.
7. **Резервное копирование с дня 1.** Даже на тестовом сервере.

---

## 🗺️ Дорожная карта и метрики

### Таймлайн (1 разработчик)
| Этап | Срок | Результат |
|------|------|-----------|
| Фаза 0 | Недели 1-2 | Репозиторий, БД, авторизация, базовый фронт |
| Фаза 1 | Недели 3-6 | Расписание, конфликты, кабинеты студента/преподавателя |
| Фаза 2 | Недели 7-10 | Счета, платежи, пакеты, рассрочка, дашборд |
| Фаза 3 | Недели 11-14 | Персонал, зарплаты, задачи, уведомления |
| Фаза 4 | Недели 15-18 | Умная запись, шаблоны, 2FA, аудит, стабилизация |
| Фаза 5 | Недели 19-22 | API, webhooks, календари, PWA, подготовка к v2.0 |

### Метрики успеха
| Фаза | Технические | Бизнес |
|------|-------------|--------|
| 1 | API <500мс, миграции работают | Демо готово, 3 тестовые школы |
| 2 | 99% успешных платежей, webhooks стабильны | Оплата онлайн, долги ↓ на 30% |
| 3 | Расчёт зарплаты <2с для 50 чел. | Экономия 10+ ч/мес, удержание преподавателей ↑ |
| 4+ | Uptime 99.5%, бэкапы проверены | NPS >40, конверсия в платящих ↑ |

---

## 📎 Приложения

### А. Глоссарий
| Термин | Определение |
|--------|-------------|
| **Слот** | Временной интервал для занятия (день + время + аудитория) |
| **Пакет** | Набор занятий, оплачиваемый единовременно со скидкой |
| **Рассрочка** | Оплата курса частями, школа выступает кредитором |
| **Умная запись** | Алгоритм подбора слотов рядом с существующими у студента |
| **Мульти-тенанси** | Одна инсталляция → множество независимых организаций |

### Б. Полезные ссылки
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue 3 + Composition API](https://vuejs.org/guide/introduction.html)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Element Plus](https://element-plus.org/)
- [NetAngels VPS Guides](https://docs.netangels.ru/)

### В. Шаблон пользовательской истории (User Story)
```markdown
## Как [роль], я хочу [действие], чтобы [ценность]

**Критерии приемки:**
- [ ] Условие 1
- [ ] Условие 2
- [ ] Условие 3

**Технические заметки:**
- Эндпоинт: `POST /api/v1/...`
- Модель: `ClassName`
- Зависимости: `module.service.method()`

**Связанные задачи:**
- #123 — валидация
- #124 — уведомление
```

---

> ✅ **Следующий шаг:** Инициализировать репозиторий, настроить `pre-commit`, создать базовые модели БД и эндпоинт авторизации.  
> 💡 **Совет:** Веди `CHANGELOG.md` и фиксируй версии API с первого дня. Это сэкономит часы при отладке и масштабировании.

*Документ актуален на: 2026-05-09 | Версия: 2.0 (Solo + NetAngels) | Автор: Сергей Токмаков*
