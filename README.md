Мне хочется дастать query_set который содержит все книги и аннотировать им райтинг когторый им поставил пользователь с id=1.
### python
query_set  = Book.objects.annotate(user_rate=Cast("book_like__rate", CharField()))
###
