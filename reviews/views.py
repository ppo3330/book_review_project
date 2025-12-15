from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from .forms import ReviewForm
from django.http import HttpResponseForbidden

def home(request):
    books = Book.objects.all().order_by('-id')
    return render(request, 'reviews/home.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book 
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/detail.html', context)

def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.user != review.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/review_edit.html', {
    'form': form,
    'review': review,
})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.user != review.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == "POST":
        book_pk = review.book.pk
        review.delete()
        return redirect('book_detail', pk=book_pk)
        
    return render(request, 'reviews/review_delete.html', {
        'review': review,
})