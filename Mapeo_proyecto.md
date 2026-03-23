# Mapeo del Proyecto

Cada módulo funcional del proyecto se convierte en una **app Django** dentro del directorio `apps/`.

```text
apps/
├── users/          # PRIMERO: Base de todo, autenticación
├── projects/       # Gestor de proyectos (tareas, hitos, versiones)
├── collaboration/  # Mensajería por canales de texto + docs compartidos
└── study/          # Herramienta de estudio con IA
```

---

## 🔐 apps/users — Usuarios y Autenticación

### Modelos (`models.py`)
* **User** (extiende `AbstractUser`)
    * `role`: "member" | "admin"
    * `avatar`: (opcional)

### Serializadores (`serializers.py`)
* `UserSerializer`: Datos del perfil.
* `RegisterSerializer`: Registro (valida email único, contraseña).
* `LoginSerializer`: Email + password → devuelve JWT.

### Endpoints (`views.py` / `urls.py`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| POST | `/api/v1/auth/register/` | Registro de usuario |
| POST | `/api/v1/auth/login/` | Login y obtención de JWT |
| POST | `/api/v1/auth/token/refresh/` | Refrescar el token |
| GET | `/api/v1/users/me/` | Ver perfil del usuario autenticado |
| PATCH | `/api/v1/users/me/` | Editar perfil |

---

## 📊 apps/projects — Gestor de Proyectos
*Inspirado en Trello/Asana. El "control de versiones" del documento se implementa como un historial de cambios en la BD (no Git).*

### Modelos (`models.py`)
* **Project**: `name`, `description`, `members` (M2M → User), `created_by` (FK → User), `created_at`.
* **Task**: `title`, `description`, `status` ("todo" | "in_progress" | "done"), `assigned_to` (FK), `project` (FK), `due_date`.
* **Milestone**: `name`, `due_date`, `project` (FK), `tasks` (M2M → Task).
* **ProjectActivity** (Control de versiones): `project` (FK), `user` (FK), `action` ("created_task", "changed_status", etc.), `timestamp`.

### Endpoints (`views.py` / `urls.py`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET/POST | `/api/v1/projects/` | Listar o crear proyectos |
| GET/PUT/DEL | `/api/v1/projects/{id}/` | Detalle, editar o borrar proyecto |
| GET/POST | `/api/v1/projects/{id}/tasks/` | Tareas de un proyecto |
| PATCH | `/api/v1/tasks/{id}/` | Cambiar estado de una tarea |
| GET/POST | `/api/v1/projects/{id}/milestones/` | Hitos del proyecto |
| GET | `/api/v1/projects/{id}/activity/` | Historial de actividad |

---

## 💬 apps/collaboration — Herramienta Colaborativa

### Estrategia de Mensajería
| Opción | Cómo | Complejidad |
| :--- | :--- | :--- |
| **Polling** | El frontend pregunta cada 2-3 seg si hay mensajes. | **Baja** (REST puro) |
| **WebSockets** | Django Channels + Redis. | **Alta** (Tiempo real) |

> **Nota para el TFG:** Empezar con *polling*. Si sobra tiempo, migrar a WebSockets.

### Modelos (`models.py`)
* **Channel**: `name`, `project` (FK), `type` ("text" | "announcement").
* **Message**: `channel` (FK), `author` (FK), `content`, `created_at`.
* **Document**: `title`, `content` (Markdown), `project` (FK), `last_edited_by` (FK).
* **DocumentVersion**: `document` (FK), `content_snapshot`, `saved_by` (FK), `created_at`.

### Endpoints (`views.py` / `urls.py`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET/POST | `/api/v1/projects/{id}/channels/` | Gestionar canales |
| GET/POST | `/api/v1/channels/{id}/messages/` | Mensajes del canal |
| GET/POST | `/api/v1/projects/{id}/documents/` | Documentos del proyecto |
| GET/PUT | `/api/v1/documents/{id}/` | Ver/Editar documento |
| GET | `/api/v1/documents/{id}/versions/` | Historial de versiones |

> **Canales de voz:** Se recomienda dejar fuera del alcance o usar un servicio externo como **LiveKit** o **Daily.co** mediante WebRTC.

---

## 🤖 apps/study — Herramienta de Estudio con IA
*El flujo es: Subir apuntes → IA genera preguntas → Realizar test → Feedback.*

### Modelos (`models.py`)
* **Note**: `title`, `content` (Markdown/Texto), `owner` (FK), `created_at`.
* **Quiz**: `note` (FK), `generated_at`, `score`.
* **Question**: `quiz` (FK), `text`, `option_a/b/c/d`, `correct_option`, `explanation`.
* **UserAnswer**: `question` (FK), `user` (FK), `selected_option`, `is_correct`.
* **ChatMessage**: `user` (FK), `note` (FK), `role` ("user" | "assistant"), `content`.

### Endpoints (`views.py` / `urls.py`)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| POST | `/api/v1/study/notes/` | Subir apuntes |
| GET | `/api/v1/study/notes/` | Listar apuntes |
| POST | `/api/v1/study/notes/{id}/generate-quiz/` | IA genera el quiz |
| GET | `/api/v1/study/quiz/{id}/` | Obtener el cuestionario |
| POST | `/api/v1/study/quiz/{id}/submit/` | Enviar respuestas |
| POST | `/api/v1/study/chat/` | Tutor chatbot |
| GET | `/api/v1/study/chat/history/` | Historial de chat |

### Integración IA
Se utiliza la librería `openai` para enviar el contenido de la nota y solicitar la generación de preguntas en formato **JSON**.