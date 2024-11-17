from django.shortcuts import render
from django.core.paginator import Paginator
from books.models import BookReview


def landing(request):
    return render(request,'landing.html')




def HomePageView(request):
    book_review = BookReview.objects.all().order_by('-created_time')
    page_size = request.GET.get('page_size', 10)
    pagination = Paginator(book_review,page_size)
    page_num = request.GET.get('page')
    page_obj = pagination.get_page(page_num)

    return render(request,'home.html',{"page_obj":page_obj})