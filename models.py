from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(verbose_name="текст")
    rate = models.ManyToManyField(User, through="managebook.BookRate", related_name="user")
    cached_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, verbose_name="рэйтинг")



class Comment(models.Model):
    text = models.TextField(verbose_name="текст")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь", related_name="comment")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга", related_name="comment")
    like = models.ManyToManyField(User, through='managebook.CommentLike', related_name="liked_comment")
    cached_likes = models.PositiveIntegerField(default=0)
    


class BookRate(models.Model):
    class Meta:
        unique_together = ("user", 'book')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_like")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_like")
    rate = models.PositiveIntegerField(default=0)



class CommentLike(models.Model):
    class Meta:
        unique_together = ("user", 'comment')

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
