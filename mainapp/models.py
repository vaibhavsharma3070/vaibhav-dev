from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create App data models here.
class AppData(models.Model): 
    ROW_ID = models.AutoField(primary_key=True)
    KEY = models.CharField(max_length=50, unique=True)
    VALUE = models.TextField() 
    CREATED = models.DateTimeField(auto_now_add=True)
    UPDATED = models.DateTimeField(auto_now=True)
    CREATEDBY = models.CharField(max_length=50)
    UPDATEDBY = models.CharField(max_length=50)

    def __str__(self):
        return self.KEY




class CustomUserManager(BaseUserManager):
	def create_user(self, name, email,birthday, phone,gender, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not name:
			raise ValueError("Users must have an username")

		user  = self.model(
				email=self.normalize_email(email),
				name=name,
                birthday=birthday,
                phone =phone,
                gender =gender,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, name, password,birthday,phone,gender):
            user  = self.create_user(
                    email=self.normalize_email(email),
                    password=password,
                    name=name,
                    birthday=birthday,
                    phone =phone,
                    gender =gender
                )

            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.name = name
            user.save(using=self._db)
            return user


class CustomUser(AbstractBaseUser):
        email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
        username 				= None
        date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
        last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
        is_admin				= models.BooleanField(default=False)
        is_active				= models.BooleanField(default=True)
        is_staff				= models.BooleanField(default=False)
        is_superuser			= models.BooleanField(default=False)
        name                    = models.CharField(max_length = 100, default="")
        birthday                = models.DateField(auto_now=False, null=True, blank=True)
        phone                   = models.CharField(max_length = 100,default="")
        gender                  = models.CharField(max_length = 1,default="")
        spacialist              = models.CharField(max_length = 150,default="")
        currentwork             = models.CharField(max_length = 150,default="")
        company                 = models.CharField(max_length = 150,default="")
        Country                 =models.CharField(max_length = 150,default="")
        state                   = models.CharField(max_length = 1,default="")
        # tags_of_used_technology =models.CharField(max_length = 150,default="")
        type                     =models.CharField(max_length = 150,default="Normal Member")
        short_description       =models.TextField(default="") 


        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['name','birthday','phone','gender']

        objects = CustomUserManager()

        def __str__(self):
            return self.name
        # this methods are require to login super user from admin panel
        def has_perm(self, perm, obj=None):
            return self.is_admin
        # this methods are require to login super user from admin panel
        def has_module_perms(self, app_label):
            return True
        

class userFiles(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='user_Files')
    doc = models.FileField()
    img = models.ImageField( )
    type =models.CharField(max_length = 150,default="User")


