async with connection.transaction():
    await connection.execute("INSERT INTO mytable VALUES (1, 2, 3)")
