
# BackEnd - GigaPizza

<img align="center" alt="Python" width="30" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="Django" width="30" src="https://cdn.worldvectorlogo.com/logos/django.svg"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="Django Rest Framework" height="40" src="https://i.imgur.com/dcVFAeV.png"><span>&nbsp;&nbsp;&nbsp;</span>
<img align="center" alt="PostgreSQL" width="36" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg"><span>&nbsp;&nbsp;&nbsp;</span>

#
Oi, tudo bem?
Este é um projeto para futura implantação de um sistema de cardápio online e gerenciamento de pedidos e etoque de produtos.
O foco é a criação de uma API em Django e Django Rest Framework para todo o gerenciamento de um restaurante, com foco específico em Pizzarias, mas com nível de abstração suficiente para permitir qualquer tipo de restaurantes e itens.
O app está atualmente hospedado no endereço abaixo:
><https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com/>

O link redireciona à documentação Swagger do projeto, com a possibilidade de consumo de algumas rotas públicas.
O serviço está funcionando corretamente online.
Também é possível acessar as rotas da API normalmente com POSTMan/Insomnia, além da documentação online.
A API segue o padrão REST, cumprindo todos os requisitos para ser considerada uma API RESTful

## Recursos implementados
-   Criação, manutenção e busca de Categorias, Subcategorias, Insumos, Vendáveis (produtos a serem vendidos), Ingredientes usados no itens vendáveis
- Gerenciamento de estoque
-   Segurança e gerenciamento para diferentes tipos de usuários
-   Personalização de views de acordo com permissões de usuário
-   Segurança baseada em tokens jwt (access e refresh tokens)
-   Código simples e de fácil entendimento
-   Criação de usuários
-   Listagem de itens para montagem do cardápio público
-   Método HATEOAS implementado em todas os endpoints
### Futuros incrementos
- Montagem de carrinho de compra
- Finalização de compras
- Dedução automática de estoque
- Dashboards e relatórios
- Suporte para upload de imagens

## API

A API foi implementada com autenticação SimpleJWT, usando Django Rest Framework, a documentação foi feita com Swagger, via DRF-Spectacular, sendo totalmente funcional e testável. Para isso, é possível o consumo de rotas classificadas como **Public**, mas também será listado um usuário do tipo *Admin* abaixo para que seja possível o login e consumo de rotas classificadas como **Admin** (para este usuário será liberado apenas requisições do tipo *GET*). 

Abaixo um print da área de login da API com JWT, é necessário consummir a rota /api/token/, obter o token "access" e colar o valor recebido na opção circulada logo acima "Authorize"

<img src="https://i.imgur.com/rRDLtf5.png" alt="Rotas para autenticação">


Foram implementados filtros de pesquisa (query-params) em todas as rotas pertecentes a usuários do tipo Admin, para facilitar o manuseio do sistema.
Cada endpoint traz também links de referências a todos os documentos relacionados ao objeto de requisição, obedecendo ao método REST HATEOAS, o que pode ser útil para entender os retornos da API sem a ajuda da documentação, mas pode deixar o retorno mais pesado. Para desativar o retorno dos links, use o query parameter `links=false`.

A documentação está na rota `/api/schema/swagger/`
Por consequência, documentação online pode ser acessada em <https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com/api/schema/swagger/>


## Acesso

Na instância online da aplicação foi mockado um usuário para que seja possível fazer o um *GET* em todas as rotas do sistema:

|  Usuário          |Login                            |Senha        |Observação        |
|-------------------|---------------------------------|-------------|------------------|
|admin2documentation|admin2documentation@gigapizza.com|documentation|User apenas com permissões *GET* na categoria **Admin**



# Rodando o projeto offline

Para rodar o projeto é bem simples e convencional, basta dar um `pip install -r requirements.txt` (recomendável rodar em uma venv).
O código busca um arquivo `env.py` para procurar as variáveis internas do projeto, caso não ache as variáveis de ambiente instaladas no SO. O arquivo deve seguir os seguintes moldes:
```python
secretKeyDjango =  "Sua chave secreta do Django aqui"
secretKeyJWT =  "Sua chave secreta do DRF-SimpleJWT aqui"
debug =  True # Ou False
bdEngine =  "django.db.backends.postgresql (Ou outro engine de banco)"
bdName =  "postgres (o nome do banco)"
bdUser =  "postgres.user (o usuário do banco)"
bdPass =  "BDpass#123 (a senha do banco)"
bdHost =  "localhost (o host do banco)"
bdPort =  "5432 (a porta do banco)"
allowedHosts = ["*", "Os hosts permitidos para fazer request na sua API"]
```
Colocar o arquivo `env.py` dentro da pasta `backendgigapizza/` do projeto (mesmo nível de settings.py)
E rodar o projeto com `python manage.py runserver`

## Testes

Os testes estão configurados para rodar em uma instância local do SQLite
Para execução dos testes é preciso executar `python manage.py test` no projeto offline
Atualmente os testes cobrem os seguintes grupos de endpoints (métodos *GET*, *POST*, *PATCH* e *DELETE*):
- **Auth**
- **Admin.Categorys** (somente método *GET* para o usuário admin2documentation)
- **Admin.Subcategorys** (somente método *GET* para o usuário admin2documentation)
- **Public.CreateUsers** (somente para usuários não autenticados)

Mais testes serão adicionados no decorrer dos dias

## Autenticação

 O Access Token da API tem duração de 60 minutos, enquanto o Refresh Token tem duração de 240 minutos.
