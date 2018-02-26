from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class Review(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reviewText = models.CharField(max_length=300)
    rating = models.IntegerField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Comment(models.Model):
    REVIEW_TYPES = (('U','University'),('C','Course'),('T','Teacher'))
    
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reviewType = models.CharField(max_length=1, choices = REVIEW_TYPES)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=120)
    def __str__(self):
        return self.name

class Course(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    convener = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="course_convener")
    teachers = models.ManyToManyField(Teacher)
    def __str__(self):
        return self.name

class CourseReview(Review):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
	

class UniReview(Review):
    university = models.ForeignKey(University, on_delete=models.CASCADE)

class TeacherReview(Review):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
