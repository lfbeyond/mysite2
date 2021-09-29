from django.db import models
from django.utils import timezone
# Create your models her
from django.db import models
from django.utils.six import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = UEditorField(verbose_name='评论',width=800, height=300, toolbars="full", imagePath="ueditor/ueditor/", filePath="ueditor/ueditor/", upload_settings={"imageMaxSize":1204000},default='')
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Article',on_delete=models.CASCADE)
    def publish(self):
        self.created_time = timezone.now()
        self.save()

    def __str__(self):
        return self.text