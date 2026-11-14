erDiagram
USER ||--o{ TASK : owns
CATEGORY ||--o{ TASK : contains

    USER {
        int id PK
        string username UK
        string hashed_password
        string role
    }

    CATEGORY {
        int id PK
        string name UK
        string description
    }

    TASK {
        int id PK
        string title
        string description
        boolean completed
        int category_id FK
        int owner_id FK
    }
