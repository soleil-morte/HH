from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998xxxxxxx fromatida bo'lishi kerak."
    )
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True, validators=[phone_regex])
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    profile_picture = models.ImageField(upload_to='', blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    is_employer = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.phone:
            cleaned_number = ''.join(filter(str.isdigit, self.phone))
            if cleaned_number.startswith('998') and len(cleaned_number) == 12:
                self.phone = f"+{cleaned_number}"
            elif not cleaned_number.startswith('+998'):
                raise ValueError("Telefon raqam noto'g'ri formatda")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    JOB_TYPES = (
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("remote", "Remote"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ManyToManyField(Location)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

# class JobApplication(BaseModel):
#     STATUS_CHOICES = (
#         ("pending", "Pending"),
#         ("reviewed", "Reviewed"),
#         ("accepted", "Accepted"),
#         ("rejected", "Rejected"),
#     )
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
#     cover_letter = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.email} -> {self.job.title}"    
    

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    last_message = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат {self.id} - {self.user.username} и {self.company.name}"
    

class Message(models.Model):
    content = models.CharField(max_length=120)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    cv_file = models.FileField(upload_to="chat_cvs/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} -> {self.content}"    