import bcrypt

senha = '123'

senhaHash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

print(senhaHash.decode('utf-8'))