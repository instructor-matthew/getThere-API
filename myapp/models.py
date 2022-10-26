from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
  def validation(self, postData):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(User.objects.filter(email=postData['email'])) > 0:
      errors['taken'] = "Email Address is already taken" 
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "You must enter a valid email address"
    if len(postData['name']) < 2:
      errors["name"] = "Name must be at least 2 characters"
    if len(postData['password']) < 8:
      errors['password'] = "Password must be 8 characters"
    return errors
  
  def register(self, postData):
    hashed_pw = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode()
    new_user = self.create(name=postData['name'],email=postData['email'],password=hashed_pw)
    print("successfully registered", new_user.name)
    return new_user.id

  def loginvalidation(self, postData):
    goodLogin = True
    user_info = User.objects.filter(email=postData['login_username'])
    if len(user_info) == 1 and bcrypt.checkpw(postData['login_password'].encode(), user_info[0].password.encode()):      
      return goodLogin
    else:
      goodLogin = False
      return goodLogin

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=45)
  email = models.CharField(max_length=30)
  pic = models.FileField(upload_to='pics')
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

  objects = UserManager()

  def __repr__(self):
    return f"<User object: {self.first_name} ({self.id})>"

