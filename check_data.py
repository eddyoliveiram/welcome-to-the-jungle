from django.contrib.auth.models import User
from blog.models import Post, Comment

print(f'Users: {User.objects.count()}')
print(f'Posts: {Post.objects.count()}')
print(f'Comments: {Comment.objects.count()}')

print("\nUsers:")
for user in User.objects.all():
    print(f"  - {user.username}")

print("\nPosts:")
for post in Post.objects.all():
    print(f"  - {post.title} by {post.author.username}")

print("\nComments:")
for comment in Comment.objects.all():
    print(f"  - Comment on '{comment.post.title}' by {comment.author.username}")
