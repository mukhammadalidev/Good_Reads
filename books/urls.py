from django.urls import path
from .views import List,Detail,BookReviewView,EditReviewView,ConfirmDeleteReviewView,DeleteReviewView

app_name = "book"

urlpatterns = [
    path('',List.as_view(),name="list"),
    path('<int:id>/',Detail.as_view(),name="detail"),
    path('<int:id>/review/',BookReviewView.as_view(),name="review"),
    path('<int:book_id>/review/<int:review_id>/edit',EditReviewView.as_view(),name="edit_review"),
    path(
        "<int:book_id>/reviews/<int:review_id>/delete/confirm/",
        ConfirmDeleteReviewView.as_view(),
        name="confirm-delete-review"
    ),
    path(
        "<int:book_id>/reviews/<int:review_id>/delete/",
        DeleteReviewView.as_view(),
        name="delete-review"
    ),
]