CREATE TABLE dispositivos (
    id_dispositivo INTEGER PRIMARY KEY AUTOINCREMENT,
    dispositivo VARCHAR(50),
    valor INTEGER
);

INSERT INTO dispositivos (dispositivo, valor) VALUES ('led', 0);
INSERT INTO dispositivos (dispositivo, valor) VALUES ('sensor', 0);
