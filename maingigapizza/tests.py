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

    #####################################################
    #####################################################
    ################## Admin.Categorys ##################
    #####################################################
    #####################################################

    def test_create_category(self):
        # Dados da nova categoria
        category_url = reverse("admin-categorys-list")
        category_data = {"name": "New Category"}

        # Teste de status HTTP
        response = self.client.post(category_url, category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        category = Categorys.objects.get(name="New Category")
        self.assertEqual(category.name, "New Category")
        self.assertTrue(category.is_active)

    def test_get_category(self):
        # Teste de resposta sem nenhum registro
        category_url = reverse("admin-categorys-list")
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

        # Teste de resposta com um registro
        new_category = {"name": "New Category"}
        self.client.post(category_url, new_category, format="json")
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            [{"id": 1, "name": "New Category", "is_active": True}],
        )

    def test_patch_category(self):
        # Inclusão de dado para teste posterior
        category_url = reverse("admin-categorys-list")
        new_category = {"name": "New Category"}
        self.client.post(category_url, new_category, format="json")

        # Teste de atualização de um campo
        category_url = reverse("admin-categorys-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Category"}
        response = self.client.patch(category_url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Category", "is_active": True},
        )

    def test_delete_category(self):
        # Inclusão de dado para teste posterior
        category_url = reverse("admin-categorys-list")
        new_category = {"name": "New Category"}
        self.client.post(category_url, new_category, format="json")

        # Teste de exclusão de um registro
        category_url = reverse("admin-categorys-detail", kwargs={"pk": 1})
        response = self.client.delete(category_url)
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
        subcategory_url = reverse("admin-subcategorys-list")
        subcategory_data = {"name": "New Subcategory", "category": category.id}

        # Teste de status HTTP
        response = self.client.post(subcategory_url, subcategory_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de pesquisa direta no banco
        subcategory = SubCategorys.objects.get(name="New Subcategory")
        self.assertEqual(subcategory.name, "New Subcategory")
        self.assertEqual(subcategory.category, category)
        self.assertTrue(subcategory.is_active)

    def test_get_subcategory(self):
        # Teste de resposta sem nenhum registro
        subcategory_url = reverse("admin-subcategorys-list")
        response = self.client.get(subcategory_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")

        # Teste de resposta com um registro
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(subcategory_url, new_subcategory, format="json")
        response = self.client.get(subcategory_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            [{"id": 1, "name": "New Subcategory", "category": 1, "is_active": True}],
        )

    def test_patch_subcategory(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")

        # Inclusão de dado para teste posterior
        subcategory_url = reverse("admin-subcategorys-list")
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(subcategory_url, new_subcategory, format="json")

        # Teste de atualização de um campo
        subcategory_url = reverse("admin-subcategorys-detail", kwargs={"pk": 1})
        new_data = {"name": "Updated Subcategory"}
        response = self.client.patch(subcategory_url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 1, "name": "Updated Subcategory", "category": 1, "is_active": True},
        )

    def test_delete_subcategory(self):
        # Criação de uma nova categoria
        category = Categorys.objects.create(name="Test Category")
        # Inclusão de dado para teste posterior
        subcategory_url = reverse("admin-subcategorys-list")
        new_subcategory = {"name": "New Subcategory", "category": category.id}
        self.client.post(subcategory_url, new_subcategory, format="json")

        # Teste de exclusão de um registro
        subcategory_url = reverse("admin-categorys-detail", kwargs={"pk": 1})
        response = self.client.delete(subcategory_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
