from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from author.models import Author
from author.serializers import AuthorSerializer

AUTHORS_URL = reverse("author:manage-list")


class AuthorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        Author.objects.create(
            first_name="Joanne",
            last_name="Rowling",
            pseudonym="J. K. Rowling",
            age=57,
            retired=False,
        )
        Author.objects.create(
            first_name="Dan", last_name="Brown", age=58, retired=False
        )

    def test_get_authors(self):
        authors = self.client.get(AUTHORS_URL)
        serializer = AuthorSerializer(Author.objects.all(), many=True)
        self.assertEqual(authors.status_code, status.HTTP_200_OK)
        self.assertEqual(authors.data, serializer.data)

    def test_post_authors(self):
        authors = self.client.post(
            AUTHORS_URL,
            {
                "first_name": "Serhii",
                "last_name": "Zhadan",
                "age": 47,
                "retired": False,
            },
        )
        db_authors = Author.objects.all()
        self.assertEqual(authors.status_code, status.HTTP_201_CREATED)
        self.assertEqual(db_authors.count(), 3)
        self.assertEqual(db_authors.filter(first_name="Serhii").count(), 1)

    def test_post_invalid_author(self):
        authors = self.client.post(
            AUTHORS_URL,
            {
                "first_name": "Serhii",
                "last_name": "Zhadan",
                "age": "extremely young",
                "retired": False,
            },
        )
        not_created_author = Author.objects.filter(first_name="Serhii")
        self.assertEqual(authors.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(not_created_author.count(), 0)

    def test_get_author(self):
        response = self.client.get(f"{AUTHORS_URL}1/")
        serializer = AuthorSerializer(
            Author(
                id=1,
                first_name="Joanne",
                last_name="Rowling",
                pseudonym="J. K. Rowling",
                age=57,
                retired=False,
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_author(self):
        response = self.client.get(f"{AUTHORS_URL}50/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_author(self):
        self.client.put(
            f"{AUTHORS_URL}1/",
            {
                "first_name": "Serhii",
                "last_name": "Zhadan",
                "age": 47,
                "retired": True,
            },
        )
        db_author = Author.objects.get(id=1)
        self.assertEqual(
            [
                db_author.first_name,
                db_author.last_name,
                db_author.age,
                db_author.retired,
            ],
            ["Serhii", "Zhadan", 47, True],
        )

    def test_put_invalid_author(self):
        response = self.client.put(
            f"{AUTHORS_URL}1/",
            {
                "first_name": "Serhii",
                "last_name": "Zhadan",
                "age": "hundred years",
            },
        )
        db_author = Author.objects.get(id=1)
        self.assertEqual(db_author.age, 57)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_author(self):
        response = self.client.patch(
            f"{AUTHORS_URL}1/",
            {
                "first_name": "Serhii",
            },
        )
        db_author = Author.objects.get(id=1)
        self.assertEqual(db_author.first_name, "Serhii")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_author(self):
        response = self.client.patch(
            f"{AUTHORS_URL}1/",
            {
                "age": "hundred years",
            },
        )
        db_author = Author.objects.get(id=1)
        self.assertEqual(db_author.age, 57)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_author(self):
        response = self.client.delete(
            f"{AUTHORS_URL}1/",
        )
        db_author_id_1 = Author.objects.filter(id=1)
        self.assertEqual(db_author_id_1.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_author(self):
        response = self.client.delete(
            f"{AUTHORS_URL}50/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
