from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from users.models import CustomUser
from .models import Book, BookReview, BookAuthor


class BookList(TestCase):
    def test_no_list(self):
        response = self.client.get(reverse("book:list"))
        self.assertContains(response,'No books found.')

    def test_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="111111")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="333333")

        response = self.client.get(reverse("book:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("book:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)




    def test_detail(self):
        book = Book.objects.create(title='My history', description="khfsdhfudufsdufs", isbn="111111")
        response = self.client.get(reverse("book:list"),kwargs={"id":book.id})

        self.assertContains(response,book.title)

    def test_search(self):
        book1 = Book.objects.create(title="sport", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="good", description="Description2", isbn="111111")
        book3 = Book.objects.create(title="like", description="Description3", isbn="333333")

        response = self.client.get(reverse("book:list")+'?q=sport')

        self.assertContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response,book3.title)




class AddReview(TestCase):

    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        user = CustomUser.objects.create(username='mukhammadali', first_name='Jakhongir')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='mukhammadali',password='somepassword')

        self.client.post(
            reverse("book:review",kwargs={"id":book.id}),
            data = {
                "stars_given":5,
                "comment":"nice"
            }
        )
        book_review = book.reviews.all()
        self.assertEqual(book_review.count(),1)
        self.assertEqual(book_review[0].stars_given,5)
        self.assertEqual(book_review[0].comment,'nice')


class HomePage(TestCase):
    def test_pagination(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        user = CustomUser.objects.create(username='mukhammadali', first_name='Jakhongir')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='mukhammadali',password='somepassword')


        review1 = BookReview.objects.create(book=book,user=user,comment="very nice",stars_given=5)
        review2 = BookReview.objects.create(book=book,user=user,comment="very nice2",stars_given=5)
        review3 = BookReview.objects.create(book=book,user=user,comment="very nice3",stars_given=5)

        response = self.client.get(
            reverse("home")+"?page_size=2",

        )

        self.assertContains(response,review3.comment)
        self.assertContains(response,review2.comment)
        self.assertNotContains(response,review1.comment)

