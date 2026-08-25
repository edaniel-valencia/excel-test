CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(250) NOT NULL,
    correo VARCHAR(250) NOT NULL,
    celular VARCHAR(250) NOT NULL
);

INSERT INTO clientes (nombre, correo, celular) VALUES
('Urian Viera', 'urian@gmail.com', '123'),
('Saul R', 'saul@gmail.com', '456');
