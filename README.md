Мне хочется дастать query_set который содержит все книги и аннотировать им райтинг когторый им поставил пользователь с request.user.id.
``` python
q = Q(book_like__user_id=request.user.id)
query_set = Book.objects.annotate(user_rate=Case(When(q, then=Cast("book_like__rate", CharField()))))
```
но в таком случае дублируются книги, сколько юзеров в целом рэйтило эти книги - столько будет дублей.
тогда я (не без помощи) решил сделать фильтр
```python
q = Q(book_like__user_id=request.user.id)
query_se = Book.objects.filter(q).annotate(user_rate=Cast("book_like__rate", CharField()))
```
но в таком случае в ответе нет книг которые юзер не рэйтил. и тогда я добавил union
```python
q = Q(book_like__user_id=request.user.id)
            sub_query = Book.objects.filter(~q) \
                .annotate(user_rate=Value(0, CharField()))
            query = Book.objects.filter(q) \
                .annotate(user_rate=Cast("book_like__rate", CharField())) \
                .union(sub_query)
```
на мой взгляд данный запрос выглядит ужасно!! Так-же я хотел бы добавить аннотацию к комментариям каждой книги is_liked
которое которое равно True если данный коммент залайкан юзером request.user.id в противном случае False.
