CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE medications (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    instructions TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_medication_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE medication_schedules (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    medication_id INTEGER NOT NULL,
    time TIME NOT NULL,
    active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_schedule_medication
        FOREIGN KEY (medication_id)
        REFERENCES medications(id)
        ON DELETE CASCADE
);


CREATE TABLE medication_logs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    medication_id INTEGER NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    taken_at TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',

    CONSTRAINT fk_log_medication
        FOREIGN KEY (medication_id)
        REFERENCES medications(id)
        ON DELETE CASCADE
);