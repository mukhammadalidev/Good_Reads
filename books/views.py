from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect,reverse

# Create your views here.
from django.views import View
from django.views.generic import ListView

from books.forms import BookReviewForm
from books.models import Book, BookReview


# class List(ListView):
#     template_name = 'list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 4

class List(View):
    def get(self,request):
        books = Book.objects.all().order_by("id")
        page_size = request.GET.get('page_size',4)
        paginator = Paginator(books,page_size)
        page_num = request.GET.get('page')
        book_page = paginator.get_page(page_num)

        search_query = request.GET.get('q','')

        if search_query:
            book_page = books.filter(title__icontains=search_query)


        context = {
            "books":book_page,
            "search_query":search_query
        }
        return render(request,'list.html',context)


class Detail(View):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        book_review = BookReviewForm()

        context = {
            "book":book,
            "review":book_review
        }
        return render(request,'detail.html',context)

class BookReviewView(View):
    def post(self,request,id):
       book = Book.objects.get(id=id)
       review_form = BookReviewForm(request.POST)

       if review_form.is_valid():
           BookReview.objects.create(
               book=book,
               user = request.user,
               comment = review_form.cleaned_data['comment'],
               stars_given = review_form.cleaned_data['stars_given']
           )
           return redirect(reverse("book:detail",kwargs={"id":book.id}))
       else:
           context = {
               "book": book,
           }
           return render(request, 'detail.html', context)




class EditReviewView(View):
    def get(self,request,book_id,review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        return render(request,'edit_review.html',{"book":book,"review":review,"form":review_form})
    def post(self,request,book_id,review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review_form = BookReviewForm(instance=review,data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("book:detail", kwargs={"id": book.id}))

        return render(request, "edit_review.html",
                          {"book": book, "review": review, "review_form": review_form})




class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)

        return render(request, "confirm_delete_review.html", {"book": book, "review": review})



class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("book:detail", kwargs={"id": book.id}))