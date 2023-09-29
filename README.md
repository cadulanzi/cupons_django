# Spotlar Test: Sistema de Cupons

## Descrição

Este projeto foi desenvolvido como parte do processo seletivo para a Spotlar. Ele implementa um sistema de cupons onde clientes podem usar cupons para obter descontos em suas compras.

## Características

- CRUD para clientes, cupons e consumos.
- Aplicação de descontos através de cupons em compras.
- Filtragem e busca avançada.
- Testes unitários e de integração.
- API RESTful.

## Instalação e Configuração

1. **Clone o Repositório**

```bash
git clone https://github.com/cadulanzi/spotlar_cupons_django.git
cd spotlar_test
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