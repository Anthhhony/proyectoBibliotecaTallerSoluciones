from django.db import connection

def crear_procedimientos():
    procedimientos_sql = [
        """
        CREATE TRIGGER after_cliente_insert
        AFTER INSERT ON AppBiblioteca_cliente
        FOR EACH ROW
        BEGIN
            INSERT INTO cliente_log (accion, cliente_id, nombre, fecha)
            VALUES ('INSERT', NEW.id, NEW.nombre, NOW());
        END;
        """,
        """
        CREATE TABLE cliente_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            accion VARCHAR(10) NOT NULL,
            cliente_id INT NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            fecha DATETIME NOT NULL
        );
        """,
        """
        CREATE TRIGGER after_cliente_update
        AFTER UPDATE ON AppBiblioteca_cliente
        FOR EACH ROW
        BEGIN
            INSERT INTO cliente_log (accion, cliente_id, nombre, fecha)
            VALUES ('UPDATE', NEW.id, NEW.nombre, NOW());
        END
        """,
        """
        CREATE TRIGGER after_cliente_delete
        AFTER DELETE ON AppBiblioteca_cliente
        FOR EACH ROW
        BEGIN
            INSERT INTO cliente_log (accion, cliente_id, nombre, fecha)
            VALUES ('DELETE', OLD.id, OLD.nombre, NOW());
        END;
        """,
        """
        CREATE PROCEDURE EliminarCliente(IN cliente_id INT)
        BEGIN
            DELETE FROM cliente WHERE id = cliente_id;
        END;
        """,
        
    ]
    with connection.cursor() as cursor:
        for sql in procedimientos_sql:
            try:
                cursor.execute(sql)
            except Exception as e:
                print(f"Error al crear el procedimiento: {e}")