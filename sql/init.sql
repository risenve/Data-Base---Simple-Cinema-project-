CREATE TABLE events (
    id INT PRIMARY KEY,
    place VARCHAR(100),
    city VARCHAR(100),
    date DATE,
    duration INT,
    danger VARCHAR(50),
    type VARCHAR(100)
);

CREATE TABLE correspondent (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    specification VARCHAR(50),
    operator BOOLEAN,
    price DECIMAL(10,2)
);

CREATE TABLE reportage (
    id INT PRIMARY KEY,
    date DATE,
    quality VARCHAR(50),
    time TIME,
    video BOOLEAN,
    event_id INT REFERENCES events(id),
    correspondent_id INT REFERENCES correspondent(id)
);