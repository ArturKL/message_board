from django.test import TestCase

# Create your tests here.
from models import Post

post = Post.objects.get(pk=1)

print(post.serialize())