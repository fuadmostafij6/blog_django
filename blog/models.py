from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=150, default=1)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, models.CASCADE,related_name='post', )
    user = models.ForeignKey(User, models.CASCADE, related_name='post',)

    title = models.CharField(max_length=150)
    code = models.TextField(blank=True, null=True)
    content = models.TextField()
    SPAM = 1
    HAM = 0
    IS_SPAM_OR_NAH = [(SPAM, 'spam'), (HAM, 'not_spam')]
    messageClassified = models.IntegerField(choices=IS_SPAM_OR_NAH, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    title = models.TextField()
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    title = models.TextField()
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User={self.user.username}||comment={self.comment}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    like_type= models.CharField(default="Like", max_length=50)

    def __str__(self):
        return f"Post={self.post.id}||User={self.user.username}||Like={self.like}"
