from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from maingigapizza.models import (
    Categories,
    CategoryTypes,
    Inputs,
    Salables,
    Salables_Compositions,
    SubCategories,
    Users,
)


class AdminRoutersAPITestCase(APITestCase):
    #####################################################
    #####################################################
    ############## Auth & Public.CreateUser #############
    #####################################################
    #####################################################
    def setUp(self):
        # Credenciais que serão usadas para teste
        self.email_user = "testuser@example.com"
        self.pass_user = "password123"

        # Criação de Usuário
        self.user_data = {
            "name": "testuser",
            "email": self.email_user,
            "cpf": "12345678910",
            "tel": "9999999999",
            "password": self.pass_user,
        }
        self.create_user_url = reverse("public-create_user-list")
        response = self.client.post(self.create_user_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tranformação de usuário em Admin para os testes posteriores
        self.user = Users.objects.get(email=self.email_user)
        self.user.is_admin = True
        self.user.save()

        # Obtenção de token jwt para autenticação nos testes posteriores
        login_url = reverse("token_obtain_pair")
        login_data = {"email": self.email_user, "password": self.pass_user}
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Autenticação de usuário com o response obtido
        self.access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Criação de urls para os próximos testes da categoria Admin
        self.type_url = reverse("admin-types-list")
        self.category_url = reverse("admin-categories-list")
        self.subcategory_url = reverse("admin-subcategories-list")
        self.input_url = reverse("admin-inputs-list")
        self.salable_url = reverse("admin-salables-list")
        self.salables_compositions_url = reverse("admin-salables_compositions-list")

    #####################################################
    #####################################################
    ################ AdminToDocumentation ###############
    #####################################################
    #####################################################

    def test_1_permissions_adminToDocumentation(self):
        # Limpando as credenciais anteriores
        self.client.credentials()

        # Criação do usuário Admin para documentação
        admin2documentation_data = {
            "name": "admin2documentation",
            "email": "admin2documentation@gigapizza.com",
            "cpf": "11122233344",
            "tel": "1111111111",
            "password": "documentation",
        }
        create_user_url = reverse("public-create_user-list")
        response = self.client.post(
            create_user_url, admin2documentation_data, format="json"
        )
        print(
            "\nTest 1: Permissions AdminToDocumentation 1 de 14 - Resposta HTTP = 201"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Tranformação de usuário em Admin para os testes posteriores
        admin2documentation = Users.objects.get(
            email="admin2documentation@gigapizza.com"
        )
        admin2documentation.is_admin = True
        admin2documentation.save()

        # Obtenção de token jwt do usuário admin para documentação para autenticação nos testes posteriores
        login_url = reverse("token_obtain_pair")
        login_data = {
            "email": "admin2documentation@gigapizza.com",
            "password": "documentation",
        }
        login_response = self.client.post(login_url, login_data, format="json")
        print("Test 1: Permissions AdminToDocumentation 2 de 14 - Resposta HTTP = 200")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Autenticação de usuário com o response obtido
        self.access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Testes em Admin.CategoryTypes
        response = self.client.get(self.type_url)
        print("Test 1: Permissions AdminToDocumentation 3 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.type_url, {"test dict": "test"}, format="json")
        print("Test 1: Permissions AdminToDocumentation 4 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Category
        response = self.client.get(self.category_url)
        print("Test 1: Permissions AdminToDocumentation 5 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.category_url, {"test dict": "test"}, format="json"
        )
        print("Test 1: Permissions AdminToDocumentation 6 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Subcategory
        response = self.client.get(self.subcategory_url)
        print("Test 1: Permissions AdminToDocumentation 7 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.subcategory_url, {"test dict": "test"}, format="json"
        )
        print("Test 1: Permissions AdminToDocumentation 8 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Inputs
        response = self.client.get(self.input_url)
        print("Test 1: Permissions AdminToDocumentation 9 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.input_url, {"test dict": "test"}, format="json"
        )
        print("Test 1: Permissions AdminToDocumentation 10 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Salables
        response = self.client.get(self.salable_url)
        print("Test 1: Permissions AdminToDocumentation 11 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.salable_url, {"test dict": "test"}, format="json"
        )
        print("Test 1: Permissions AdminToDocumentation 12 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Salables_Compositions
        response = self.client.get(self.salables_compositions_url)
        print("Test 1: Permissions AdminToDocumentation 13 de 14 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.salables_compositions_url, {"test dict": "test"}, format="json"
        )
        print("Test 1: Permissions AdminToDocumentation 14 de 14 - Resposta HTTP = 403")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #####################################################
    #####################################################
    ################ Admin.CategoryTypes ################
    #####################################################
    #####################################################

    def test_2_1_create_categorytype(self):
        # Dados do novo tipo de categoria
        category_type_data = {"name": "New Type"}

        # Teste de status HTTP
        response = self.client.post(self.type_url, category_type_data, format="json")
        print("\nTest 2.1: Create CategoryType 1 de 3 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        category_type = CategoryTypes.objects.get(name="New Type")
        print("Test 2.1: Create CategoryType 2 de 3 - Category Name")
        self.assertEqual(category_type.name, "New Type")
        print("Test 2.1: Create CategoryType 3 de 3 - Category IsActive")
        self.assertTrue(category_type.is_active)

    def test_2_2_get_categorytype(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.type_url)
        print("\nTest 2.2: Get CategoryType 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 2.2: Get CategoryType 2 de 4 - Resposta Com 3 Valores Padrões")
        self.assertEqual(len(response.data["results"]["category_types"]), 3)

        # Teste de resposta com um registro
        new_type = {"name": "New Type\n"}
        self.client.post(self.type_url, new_type, format="json")
        response = self.client.get(self.type_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["category_types"])):
            del response.data["results"]["category_types"][i]["links"]

        print("Test 2.2: Get CategoryType 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 2.2: Get CategoryType 4 de 4 - GET CategoryType")
        self.assertEqual(len(response.data["results"]["category_types"]), 4)

    def test_2_3_patch_categorytype(self):
        # Inclusão de dado para teste posterior
        new_type = {"name": "New Type\n"}
        self.client.post(self.type_url, new_type, format="json")

        # Teste de atualização de um campo
        type_url_detail = reverse("admin-types-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated CategoryType\n"}
        response = self.client.patch(type_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]
        print("\nTest 2.3: Patch CategoryType 1 de 2 - Respota HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 2.3: Patch CategoryType 2 de 2 - PATCH CategoryType")
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated CategoryType", "is_active": True},
        )

    def test_2_4_delete_categorytype(self):
        # Inclusão de dado para teste posterior
        new_type = {"name": "New Type\n"}
        self.client.post(self.type_url, new_type, format="json")

        # Teste de exclusão de um registro
        type_url_detail = reverse("admin-types-detail", kwargs={"pk": 1})
        response = self.client.delete(type_url_detail)
        print("\nTest 2.4: Delete CategoryType 1 de 1 - Respota HTTP = 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    ################## Admin.Categories ##################
    #####################################################
    #####################################################

    def test_3_1_create_category(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Dados da nova categoria
        category_data = {"name": "New Category", "type": type.id}

        # Teste de status HTTP
        response = self.client.post(self.category_url, category_data, format="json")
        print("\nTest 3.1: Create Category 1 de 3 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        category = Categories.objects.get(name="New Category")
        print("Test 3.1: Create Category 2 de 3 - Category Name")
        self.assertEqual(category.name, "New Category")
        print("Test 3.1: Create Category 3 de 3 - Category IsActive")
        self.assertTrue(category.is_active)

    def test_3_2_get_category(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.category_url)
        print("\nTest 3.2: Get Category 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 3.2: Get Category 2 de 4 - Resposta Vazia")
        self.assertEqual(response.data["results"]["categories"], [])

        # Teste de resposta com um registro
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Dados da nova categoria
        new_category = {"name": "New Category", "type": type.id}
        self.client.post(self.category_url, new_category, format="json")
        response = self.client.get(self.category_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["categories"])):
            del response.data["results"]["categories"][i]["links"]

        print("Test 3.2: Get Category 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 3.2: Get Category 4 de 4 - GET Category")
        self.assertEqual(
            response.data["results"]["categories"],
            [{"id": 1, "name": "New Category", "type": type.id, "is_active": True}],
        )

    def test_3_3_patch_category(self):
        # Inclusão de dado para teste posterior
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        new_category = {"name": "New Category", "type": type.id}
        self.client.post(self.category_url, new_category, format="json")

        # Teste de atualização de um campo
        category_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Category"}
        response = self.client.patch(category_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]
        print("\nTest 3.3: Patch Category 1 de 2 - Respota HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 3.3: Patch Category 2 de 2 - PATCH Category")
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Category", "type": type.id, "is_active": True},
        )

    def test_3_4_delete_category(self):
        # Inclusão de dado para teste posterior
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        new_category = {"name": "New Category", "type": type.id}
        self.client.post(self.category_url, new_category, format="json")

        # Teste de exclusão de um registro
        category_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        response = self.client.delete(category_url_detail)
        print("\nTest 3.4: Delete Category 1 de 1 - Respota HTTP = 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    ################# Admin.Subcategories ################
    #####################################################
    #####################################################

    def test_4_1_create_subcategory(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Dados da nova subcategoria
        subcategory_data = {"name": "New Subcategory", "category": category.id}

        # Teste de status HTTP
        response = self.client.post(
            self.subcategory_url, subcategory_data, format="json"
        )
        print("\nTest 4.1: Create Subcategory 1 de 4 - Respota HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        subcategory = SubCategories.objects.get(name="New Subcategory")
        print("Test 4.1: Create Subcategory 2 de 4 - Subcategory Name")
        self.assertEqual(subcategory.name, "New Subcategory")
        print("Test 4.1: Create Subcategory 3 de 4 - Subcategory Category")
        self.assertEqual(subcategory.category, category)
        print("Test 4.1: Create Subcategory 4 de 4 - Subcategory IsActive")
        self.assertTrue(subcategory.is_active)

    def test_4_2_get_subcategory(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.subcategory_url)
        print("\nTest 4.2: Get Subcategory 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 4.2: Get Subcategory 2 de 4 - Resposta Vazia")
        self.assertEqual(response.data["results"]["subcategories"], [])

        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)

        # Teste de resposta com um registro
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")
        response = self.client.get(self.subcategory_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["subcategories"])):
            del response.data["results"]["subcategories"][i]["links"]

        print("Test 4.2: Get Subcategory 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 4.2: Get Subcategory 4 de 4 - GET Subcategory")
        self.assertEqual(
            response.data["results"]["subcategories"],
            [{"id": 1, "name": "New Subcategory", "category": 1, "is_active": True}],
        )

    def test_4_3_patch_subcategory(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)

        # Inclusão de dado para teste posterior
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")

        # Teste de atualização de um campo
        subcategory_url_detail = reverse("admin-subcategories-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Subcategory"}
        response = self.client.patch(subcategory_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]

        print("\nTest 4.3: Patch Subcategory 1 de 2 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 4.3: Patch Subcategory 2 de 2 - PATCH Subcategory")
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Subcategory", "category": 1, "is_active": True},
        )

    def test_4_4_delete_subcategory(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Inclusão de dado para teste posterior
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")

        # Teste de exclusão de um registro
        subcategory_url_detail = reverse("admin-subcategories-detail", kwargs={"pk": 1})
        response = self.client.delete(subcategory_url_detail)
        print("\nTest 4.4: Delete Subcategory 1 de 1 - DELETE Subcategory")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    #################### Admin.Inputs ###################
    #####################################################
    #####################################################

    def test_5_1_create_input(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Category", category=category
        )

        # Dados do novo input
        input_data = {
            "name": "New Input",
            "price": 1.5,
            "quantity": 2,
            "unit": "unidade",
            "subcategory": subcategory.id,
        }

        # Teste de status HTTP

        # Teste de validação do campo "unit"
        response = self.client.post(self.input_url, input_data, format="json")
        print("\nTest 5.1: Create Input 1 de 5 - Resposta HTTP = 400")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Teste de com campo "unit" correto
        input_data.update({"unit": "und"})
        response = self.client.post(self.input_url, input_data, format="json")
        print("Test 5.1: Create Input 2 de 5 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        input = Inputs.objects.get(name="New Input")
        print("Test 5.1: Create Input 3 de 5 - Input Name")
        self.assertEqual(input.name, "New Input")
        print("Test 5.1: Create Input 4 de 5 - Input Subcategory")
        self.assertEqual(input.subcategory, subcategory)
        print("Test 5.1: Create Input 5 de 5 - Input IsActive")
        self.assertTrue(input.is_active)

    def test_5_2_get_input(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.input_url)
        print("\nTest 5.2: Get Input 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 5.2: Get Input 2 de 4 - Resposta Vazia")
        self.assertEqual(response.data["results"]["inputs"], [])

        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Category", category=category
        )

        # Teste de resposta com um registro
        new_input = {
            "name": "New Input",
            "price": 1.5,
            "quantity": 2,
            "unit": "und",
            "subcategory": subcategory.id,
        }
        self.client.post(self.input_url, new_input, format="json")
        response = self.client.get(self.input_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["inputs"])):
            del response.data["results"]["inputs"][i]["links"]

        print("Test 5.2: Get Input 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 5.2: Get Input 4 de 4 - GET Input")
        self.assertEqual(
            response.data["results"]["inputs"],
            [
                {
                    "id": 1,
                    "name": "New Input",
                    "subcategory": 1,
                    "quantity": 2,
                    "price": 1.5,
                    "unit": "und",
                    "is_active": True,
                }
            ],
        )

    def test_5_3_patch_input(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )

        # Inclusão de dado para teste posterior
        new_input = {
            "name": "New Input",
            "price": 1.5,
            "quantity": 2,
            "unit": "und",
            "subcategory": subcategory.id,
        }
        self.client.post(self.input_url, new_input, format="json")

        # Teste de atualização de um campo
        input_url_detail = reverse("admin-inputs-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Input", "unit": "g"}
        response = self.client.patch(input_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]

        print("\nTest 5.3: Patch Input 1 de 2 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 5.3: Patch Input 2 de 2 - PATCH Input")
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Updated Input",
                "price": 1.5,
                "quantity": 2,
                "unit": "g",
                "subcategory": 1,
                "is_active": True,
            },
        )

    def test_5_4_delete_input(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )
        # Inclusão de dado para teste posterior
        new_input = {
            "name": "New Input",
            "price": 1.5,
            "quantity": 2,
            "unit": "und",
            "subcategory": subcategory.id,
        }
        self.client.post(self.input_url, new_input, format="json")

        # Teste de exclusão de um registro
        input_url_detail = reverse("admin-inputs-detail", kwargs={"pk": 1})
        response = self.client.delete(input_url_detail)
        print("\nTest 5.4: Delete Input 1 de 1 - DELETE Input")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    ################### Admin.Salables ##################
    #####################################################
    #####################################################

    def test_6_1_create_salable(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Category", category=category
        )

        # Dados do novo salable
        salable_data = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 2.5,
            "subcategory": subcategory.id,
            "inputs": [],
        }

        # Teste de status HTTP
        response = self.client.post(self.salable_url, salable_data, format="json")
        print("\nTest 6.1: Create Salable 1 de 4 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        salable = Salables.objects.get(name="New Salable")
        print("Test 6.1: Create Salable 2 de 4 - Salable Name")
        self.assertEqual(salable.name, "New Salable")
        print("Test 6.1: Create Salable 3 de 4 - Salable Subcategory")
        self.assertEqual(salable.subcategory, subcategory)
        print("Test 6.1: Create Salable 4 de 4 - Salable IsActive")
        self.assertTrue(salable.is_active)

    def test_6_2_get_salables(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.salable_url)
        print("\nTest 6.2: Get Salable 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 6.2: Get Salable 2 de 4 - Resposta Vazia")
        self.assertEqual(response.data["results"]["salables"], [])

        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Category", category=category
        )

        # Teste de resposta com um registro
        new_salable = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 2.5,
            "subcategory": subcategory.id,
            "inputs": [],
        }

        self.client.post(self.salable_url, new_salable, format="json")
        response = self.client.get(self.salable_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["salables"])):
            del response.data["results"]["salables"][i]["links"]

        print("Test 6.2: Get Salable 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 6.2: Get Salable 4 de 4 - GET Salable")
        self.assertEqual(
            response.data["results"]["salables"],
            [
                {
                    "id": 1,
                    "name": "New Salable",
                    "description": "New Salable Description",
                    "price": 2.5,
                    "subcategory": subcategory.id,
                    "is_active": True,
                }
            ],
        )

    def test_6_3_patch_salables(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )

        # Inclusão de dado para teste posterior
        new_salable = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 2.5,
            "subcategory": subcategory.id,
            "inputs": [],
        }

        self.client.post(self.salable_url, new_salable, format="json")

        # Teste de atualização de um campo
        salable_url_detail = reverse("admin-salables-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Salable"}
        response = self.client.patch(salable_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]

        print("\nTest 6.3: Patch Salable 1 de 2 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 6.3: Patch Salable 2 de 2 - PATCH Salable")
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Updated Salable",
                "description": "New Salable Description",
                "price": 2.5,
                "subcategory": subcategory.id,
                "is_active": True,
            },
        )

    def test_6_4_delete_input(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )

        # Inclusão de dado para teste posterior
        new_salable = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 2.5,
            "subcategory": subcategory.id,
            "inputs": [],
        }
        self.client.post(self.salable_url, new_salable, format="json")

        # Teste de exclusão de um registro
        salable_url_detail = reverse("admin-salables-detail", kwargs={"pk": 1})
        response = self.client.delete(salable_url_detail)
        print("\nTest 6.4: Delete Salable 1 de 1 - DELETE Salable")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    ############ Admin.Salables_Compositions ############
    #####################################################
    #####################################################

    def test_7_1_create_salable_composition(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )
        input1 = Inputs.objects.create(
            name="Test Input 1",
            subcategory=subcategory,
            price=5.5,
            quantity=4.1,
            unit="und",
        )
        input2 = Inputs.objects.create(
            name="Test Input 2",
            subcategory=subcategory,
            price=7,
            quantity=5.1,
            unit="l",
        )

        # Criando Salables_Composition a partir de um Salable
        salable_data = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 30,
            "subcategory": subcategory.id,
            "inputs": [
                {
                    "input": input1.id,
                    "quantity": 2.1,
                },
                {
                    "input": input2.id,
                    "quantity": 5,
                },
            ],
        }

        # Teste de status HTTP
        response = self.client.post(self.salable_url, salable_data, format="json")
        print("\nTest 7.1: Create Salable_Composition 1 de 3 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(
            "Test 7.1: Create Salable_Composition 2 de 3 - Quantidade de Salables_Compositions = 2"
        )
        self.assertEqual(
            Salables_Compositions.objects.filter(salable=response.data["id"]).count(), 2
        )

        # Criando Salables_Composition a partir do endpoint admin-salables_compositions-list
        salable_composition_data = {
            "salable": response.data["id"],
            "input": input2.id,
            "quantity": 5.9,
        }
        response = self.client.post(
            self.salables_compositions_url, salable_composition_data, format="json"
        )
        print("Test 7.1: Create Salable_Composition 3 de 4 - Resposta HTTP = 400")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Criação de um terceiro input para teste posterior
        input3 = Inputs.objects.create(
            name="Test Input 3",
            subcategory=subcategory,
            price=3.99,
            quantity=9,
            unit="l",
        )

        salable_composition_data = {
            "salable": 1,
            "input": input3.id,
            "quantity": 5.9,
        }
        response = self.client.post(
            self.salables_compositions_url, salable_composition_data, format="json"
        )

        print("Test 7.1: Create Salable_Composition 4 de 4 - Resposta HTTP = 201")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_7_2_get_salables_compositions(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.salables_compositions_url)
        print("\nTest 7.2: Get Salables_Compositions 1 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 7.2: Get Salables_Compositions 2 de 4 - Resposta Vazia")
        self.assertEqual(response.data["results"]["salables_compositions"], [])

        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )
        input1 = Inputs.objects.create(
            name="Test Input 1",
            subcategory=subcategory,
            price=5.5,
            quantity=4.1,
            unit="und",
        )
        input2 = Inputs.objects.create(
            name="Test Input 2",
            subcategory=subcategory,
            price=7,
            quantity=5.1,
            unit="l",
        )

        # Criando Salables_Composition a partir de um Salable
        salable_data = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 30,
            "subcategory": subcategory.id,
            "inputs": [
                {
                    "input": input1.id,
                    "quantity": 2.1,
                },
                {
                    "input": input2.id,
                    "quantity": 5,
                },
            ],
        }

        self.client.post(self.salable_url, salable_data, format="json")
        response = self.client.get(self.salables_compositions_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["salables_compositions"])):
            del response.data["results"]["salables_compositions"][i]["links"]

        print("Test 7.2: Get Salables_Compositions 3 de 4 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 7.2: Get Salables_Compositions 4 de 4 - GET Salable_Composition")
        self.assertEqual(response.data["count"], 2)

    def test_7_3_patch_salables_compositions(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )
        input1 = Inputs.objects.create(
            name="Test Input 1",
            subcategory=subcategory,
            price=5.5,
            quantity=4.1,
            unit="und",
        )
        input2 = Inputs.objects.create(
            name="Test Input 2",
            subcategory=subcategory,
            price=7,
            quantity=5.1,
            unit="l",
        )

        # Criando Salables_Composition a partir de um Salable
        salable_data = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 30,
            "subcategory": subcategory.id,
            "inputs": [
                {
                    "input": input1.id,
                    "quantity": 2.1,
                },
                {
                    "input": input2.id,
                    "quantity": 5,
                },
            ],
        }

        self.client.post(self.salable_url, salable_data, format="json")

        # Teste de atualização de um campo
        salable_composition_url_detail = reverse(
            "admin-salables_compositions-detail", kwargs={"pk": 1}
        )
        new_data = {"quantity": 2}
        response = self.client.patch(
            salable_composition_url_detail, new_data, format="json"
        )

        # Deletando o campo "links" da resposta
        del response.data["links"]

        print("\nTest 7.3: Patch Salable_Composition 1 de 2 - Resposta HTTP = 200")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test 7.3: Patch Salable_Composition 2 de 2 - PATCH Salable_Composition")
        self.assertEqual(
            response.data,
            {"id": 1, "salable": 1, "input": input1.id, "quantity": 2},
        )

    def test_7_4_delete_salables_compositions(self):
        # Criação de um novo tipo
        type = CategoryTypes.objects.create(name="Test Type")
        # Criação de uma nova categoria
        category = Categories.objects.create(name="Test Category", type=type)
        # Criação de uma nova subcategoria
        subcategory = SubCategories.objects.create(
            name="Test Subcategory", category=category
        )
        input1 = Inputs.objects.create(
            name="Test Input 1",
            subcategory=subcategory,
            price=5.5,
            quantity=4.1,
            unit="und",
        )
        input2 = Inputs.objects.create(
            name="Test Input 2",
            subcategory=subcategory,
            price=7,
            quantity=5.1,
            unit="l",
        )

        # Criando Salables_Composition a partir de um Salable
        salable_data = {
            "name": "New Salable",
            "description": "New Salable Description",
            "price": 30,
            "subcategory": subcategory.id,
            "inputs": [
                {
                    "input": input1.id,
                    "quantity": 2.1,
                },
                {
                    "input": input2.id,
                    "quantity": 5,
                },
            ],
        }

        self.client.post(self.salable_url, salable_data, format="json")

        # Teste de exclusão de um registro
        salable_url_detail = reverse(
            "admin-salables_compositions-detail", kwargs={"pk": 1}
        )
        response = self.client.delete(salable_url_detail)
        print("\nTest 7.4: Delete Salable_Composition 1 de 1 - Resposta HTTP = 204")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
