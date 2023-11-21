# Sistema de Cupons

## Descrição

O projet consiste num sistema de cupons onde clientes podem usar cupons para obter descontos em suas compras.

## Características

- CRUD para clientes, cupons e consumos.
- Aplicação de descontos através de cupons em compras.
- Filtragem e busca avançada.
- Testes unitários e de integração.
- API RESTful.

## Documentação e formas de testar
Você pode testar a api tanto pela Collection do Postman que está na pasta "postman_collection" ou pelo Swagger na rota http://127.0.0.1:8000/swagger/

## Instalação e Configuração

1. **Clone o Repositório**

```bash
git clone https://github.com/cadulanzi/cupons_django.git
cd cupons_django
```

## Ambiente Virtual
Recomendamos criar um ambiente virtual para executar este projeto:
Obs.: Esse projeto foi desenvolvido com Python 3.9.0.

```
python3.9 -m venv venv
source venv/bin/activate
```

### Instalar Dependências
```
pip install -r requirements.txt
```

### Executar Migrações
```
python manage.py migrate
```

### Iniciar o Servidor de Desenvolvimento
```
python manage.py runserver
```

Agora, você pode acessar o servidor localmente em http://localhost:8000/.

## Uso da API
### Testes
Para executar os testes
```
pytest
```
