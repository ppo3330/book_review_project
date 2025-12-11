from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from .forms import ReviewForm

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