Мне хочется дастать query_set который содержит все книги и аннотировать им райтинг когторый им поставил пользователь с request.user.id.
``` python
q = Q(book_user__user=request.user)
query_set = Book.objects.annotate(user_rate=Case(When(q, then=F("book_user__rate"))))
```
но в таком случае дублируются книги, сколько юзеров в целом рэйтило эти книги - столько будет дублей.
тогда я (не без помощи) решил сделать фильтр
```python
q = Q(book_user__user=request.user)
query_se = Book.objects.filter(q).annotate(user_rate=F("book_user__rate"))
```
но в таком случае в ответе нет книг которые юзер не рэйтил. и тогда я добавил union
```python
q = Q(book_user__user=request.user)
sub_query = Book.objects.filter(~q).annotate(user_rate=Value(0, CharField()))
query = Book.objects.filter(q).annotate(user_rate=F("book_user__rate")).union(sub_query)
```
на мой взгляд данный запрос выглядит ужасно!! Так-же я хотел бы добавить аннотацию к комментариям каждой книги is_liked
которое которое равно True если данный коммент залайкан юзером request.user.id в противном случае False.

Красивое решение первой части задачи
---
```python
subquery = BookUser.objects.filter(book=OuterRef("pk"), user=request.user).values("rate")
content = Book.objects.annotate(user_rate=Subquery(subquery))
```
Красивое решение всей задачи
---
```python
subquery_1 = BookUser.objects.filter(book=OuterRef("pk"), user=request.user).values("rate")
subquery_2 = CommentUser.objects.filter(comment=OuterRef("pk"), user=request.user)
queryset = Comment.objects.annotate(isliked=Exists(subquery_2))
prefetch = Prefetch("comment", queryset=queryset)
content = Book.objects.annotate(user_rate=Subquery(subquery_1)).prefetch_related(prefetch)
```
