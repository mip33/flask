Создание пользователя:
```
response = requests.post('http://127.0.0.1:5000/create_user/', json={'email':'mail@mail.ru', 'password':'dghhgfjh5GJK4@#%$57!@G%$H223!)hg'})
```
Получение токена:
```
response = requests.post('http://127.0.0.1:5000/token/create/', json={'email':'mail@mail.ru', 'password':'dghhgfjh5GJK4@#%$57!@G%$H223!)hg'})
```
Удаление токена:
```
response = requests.delete('http://127.0.0.1:5000/token/delete/', json={'email':'mail@mail.ru', 'password':'dghhgfjh5GJK4@#%$57!@G%$H223!)hg', 'token':'4f9b78e5-d398-4653-9bc8-1b444a886926'})
```
Удаление всех токенов:
```
response = requests.delete('http://127.0.0.1:5000/token/delete_all/', json={'email':'mail@mail.ru', 'password':'dghhgfjh5GJK4@#%$57!@G%$H223!)hg'})
```
Создание объявления:
```
response = requests.post('http://127.0.0.1:5000/advertisement/', json={'title': 'стол', 'description': 'б/у'}, headers={'token': 'b344ffc6-f75d-42cb-944e-074d6034d305'})
```
Просмотр объявления:
```
response = requests.get('http://127.0.0.1:5000/advertisement/1')
```
Изменение объявления:
```
response = requests.patch('http://127.0.0.1:5000/advertisement/1', json={'title': 'стол', 'description': 'новый'}, headers={'token': 'b344ffc6-f75d-42cb-944e-074d6034d305'})
```
Удаление объявления: 
```
response = requests.delete('http://127.0.0.1:5000/advertisement/1', headers={'token': 'b344ffc6-f75d-42cb-944e-074d6034d305'})
```
