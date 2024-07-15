from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from maingigapizza.models import Categorys, Inputs, Salables, SubCategorys, Users


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

    def test_permissions_adminToDocumentation(self):
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
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Autenticação de usuário com o response obtido
        self.access_token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Testes em Admin.Category
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.category_url, {"test dict": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Subcategory
        response = self.client.get(self.subcategory_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.subcategory_url, {"test dict": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Inputs
        response = self.client.get(self.input_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.input_url, {"test dict": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Salables
        response = self.client.get(self.salable_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.salable_url, {"test dict": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Testes em Admin.Salables_Compositions
        response = self.client.get(self.salables_compositions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.salables_compositions_url, {"test dict": "test"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #####################################################
    #####################################################
    ################## Admin.Categorys ##################
    #####################################################
    #####################################################

    def test_create_category(self):
        # Dados da nova categoria
        category_data = {"name": "New Category"}

        # Teste de status HTTP
        response = self.client.post(self.category_url, category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        category = Categorys.objects.get(name="New Category")
        self.assertEqual(category.name, "New Category")
        self.assertTrue(category.is_active)

    def test_get_category(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"]["categories"], [])

        # Teste de resposta com um registro
        new_category = {"name": "New Category"}
        self.client.post(self.category_url, new_category, format="json")
        response = self.client.get(self.category_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["categories"])):
            del response.data["results"]["categories"][i]["links"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"]["categories"],
            [{"id": 1, "name": "New Category", "is_active": True}],
        )

    def test_patch_category(self):
        # Inclusão de dado para teste posterior
        new_category = {"name": "New Category"}
        self.client.post(self.category_url, new_category, format="json")

        # Teste de atualização de um campo
        category_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Category"}
        response = self.client.patch(category_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Category", "is_active": True},
        )

    def test_delete_category(self):
        # Inclusão de dado para teste posterior
        new_category = {"name": "New Category"}
        self.client.post(self.category_url, new_category, format="json")

        # Teste de exclusão de um registro
        category_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        response = self.client.delete(category_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    ################# Admin.Subcategorys ################
    #####################################################
    #####################################################

    def test_create_subcategory(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Dados da nova subcategoria
        subcategory_data = {"name": "New Subcategory", "category": category.id}

        # Teste de status HTTP
        response = self.client.post(
            self.subcategory_url, subcategory_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        subcategory = SubCategorys.objects.get(name="New Subcategory")
        self.assertEqual(subcategory.name, "New Subcategory")
        self.assertEqual(subcategory.category, category)
        self.assertTrue(subcategory.is_active)

    def test_get_subcategory(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.subcategory_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"]["subcategories"], [])

        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")

        # Teste de resposta com um registro
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")
        response = self.client.get(self.subcategory_url)

        # Deletando o campo "links" da resposta
        for i in range(len(response.data["results"]["subcategories"])):
            del response.data["results"]["subcategories"][i]["links"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"]["subcategories"],
            [{"id": 1, "name": "New Subcategory", "category": 1, "is_active": True}],
        )

    def test_patch_subcategory(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")

        # Inclusão de dado para teste posterior
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")

        # Teste de atualização de um campo
        subcategory_url_detail = reverse("admin-subcategories-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Subcategory"}
        response = self.client.patch(subcategory_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Subcategory", "category": 1, "is_active": True},
        )

    def test_delete_subcategory(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Inclusão de dado para teste posterior
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(self.subcategory_url, new_subcategory, format="json")

        # Teste de exclusão de um registro
        subcategory_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        response = self.client.delete(subcategory_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #####################################################
    #####################################################
    #################### Admin.Inputs ###################
    #####################################################
    #####################################################

    def test_create_input(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Criação de uma nova subcategoria
        subcategory = SubCategorys.objects.create(
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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Teste de validação do campo "unit"
        input_data.update({"unit": "und"})
        response = self.client.post(self.input_url, input_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        input = Inputs.objects.get(name="New Input")
        self.assertEqual(input.name, "New Input")
        self.assertEqual(input.subcategory, subcategory)
        self.assertTrue(input.is_active)

    def test_get_inputs(self):
        # Teste de resposta sem nenhum registro
        response = self.client.get(self.input_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"]["inputs"], [])

        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Criação de uma nova subcategoria
        subcategory = SubCategorys.objects.create(
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
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

    def test_patch_inputs(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Criação de uma nova subcategoria
        subcategory = SubCategorys.objects.create(
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
        new_data = {"name": "Updated Input"}
        response = self.client.patch(input_url_detail, new_data, format="json")

        # Deletando o campo "links" da resposta
        del response.data["links"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Updated Input",
                "subcategory": 1,
                "quantity": 2,
                "price": 1.5,
                "unit": "und",
                "is_active": True,
            },
        )

    def test_delete_input(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Criação de uma nova subcategoria
        subcategory = SubCategorys.objects.create(
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
        input_url_detail = reverse("admin-categories-detail", kwargs={"pk": 1})
        response = self.client.delete(input_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
