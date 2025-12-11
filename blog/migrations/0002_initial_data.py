from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Post = apps.get_model('blog', 'Post')
    Comment = apps.get_model('blog', 'Comment')

    # Create 3 users
    users = []
    user_data = [
        {'username': 'user1', 'email': 'user1@example.com', 'first_name': 'João', 'last_name': 'Silva', 'password': 'password123'},
        {'username': 'user2', 'email': 'user2@example.com', 'first_name': 'Maria', 'last_name': 'Santos', 'password': 'password123'},
        {'username': 'user3', 'email': 'user3@example.com', 'first_name': 'Pedro', 'last_name': 'Oliveira', 'password': 'password123'},
    ]
    
    for data in user_data:
        password = data.pop('password')
        hashed_password = make_password(password)
        user = User(**data, is_staff=False, is_active=True, password=hashed_password)
        user.save()
        users.append(user)

    # Create 10 posts
    posts = []
    for i in range(1, 11):
        author = users[(i - 1) % len(users)]
        post = Post.objects.create(title=f'Post {i}', content=f'Conteúdo do post {i}', author=author)
        posts.append(post)

    # Create 10 comments, assign to posts in round-robin
    for i in range(1, 11):
        post = posts[(i - 1) % len(posts)]
        author = users[(i - 1) % len(users)]
        Comment.objects.create(post=post, author=author, content=f'Comentário {i} no {post.title}')


def reverse_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Post = apps.get_model('blog', 'Post')
    Comment = apps.get_model('blog', 'Comment')
    
    Comment.objects.all().delete()
    Post.objects.all().delete()
    User.objects.filter(username__in=['user1', 'user2', 'user3']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
