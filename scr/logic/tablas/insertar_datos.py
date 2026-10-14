from scr.logic.tablas.funciones_datos import insertar_datos_en_db2


def insertar_calendario():
    """Inserta el CSV del calendario en DB2."""
    insertar_datos_en_db2("calendario.csv", "CALENDARIO")


def insertar_demanda():
    """Inserta el CSV de demanda en DB2."""
    insertar_datos_en_db2("demanda.csv", "DEMANDA")


# INSERTAR DATOS EN DB2
#insertar_calendario()
#insertar_demanda()