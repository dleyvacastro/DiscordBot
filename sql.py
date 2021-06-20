def sql_insert_user(user):
    return f"""
    INSERT INTO usuario(id) VALUES('{user}')
    """

def sql_user_money(id):
    return f"""
    SELECT dinero 
    FROM usuario
    WHERE id = '{id}'"""

def sql_members_money():
    return """
    SELECT id, dinero
    FROM usuario
    """
def sql_set_money(user, value):
    return f"""
    UPDATE usuario
    SET dinero = {value}
    WHERE id = {user}
    """

def sql_reset_economy():
    return """
    UPDATE usuario FOR EACH ROW
    SET dinero = 0
    """

def sql_get_multas(user):
    return f'''SELECT * FROM usuario WHERE id = '{user}';'''

def sql_get_multa(user, rtype):
    return f'''SELECT m_{rtype} FROM usuario WHERE id = {user}'''

def sql_pay_multa(user, rtype):
    return f"""
    UPDATE usuario
    SET m_{rtype} = m_{rtype} -1
    WHERE id = '{user}'
    """

def sql_generate_report(user, rtype):
    return f"""INSERT INTO reportes(tipo, usuario_id) VALUES('{rtype}' ,'{user}');"""

def sql_get_reports(user, rtype):
    return f"""SELECT count(*) FROM reportes WHERE usuario_id = {user.id} and tipo = '{rtype}'"""

def sql_get_last_report_id(user):
    return f"""
        SELECT id
        FROM reportes
        WHERE usuario_id = {user}
        ORDER BY id DESC
    """

def sql_remove_report(id):
    return f"""DELETE FROM reportes WHERE id = {id}"""
