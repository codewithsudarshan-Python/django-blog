from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('travel', 'Travel'),
        ('tech', 'Tech'),
        ('personal', 'Personal'),
        ('food', 'Food'),
        ('lifestyle', 'Lifestyle'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    DEGREE_CHOICES = [
        ('BCA', 'BCA'),
        ('BSc', 'BSc'),
        ('BCom', 'BCom'),
        ('BE/BTech', 'BE/BTech'),
        ('MCA', 'MCA'),
        ('MSc', 'MSc'),
    ]
    COURSE_CHOICES = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('Web Development', 'Web Development'),
        ('Django', 'Django'),
        ('Data Structures', 'Data Structures'),
        ('C++', 'C++'),
        ('JavaScript', 'JavaScript'),
        ('Machine Learning', 'Machine Learning'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES, blank=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class PageVisit(models.Model):
    path = models.CharField(max_length=255)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    device_info = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path} - {self.visited_at.strftime('%Y-%m-%d %H:%M')}"