from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField

class Article(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    author_name = models.CharField(max_length=200,default="")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True)
    #text = models.TextField()
    text= UEditorField(verbose_name='正文',width=800, height=300, toolbars="full", imagePath="ueditor/pic/", filePath="ueditor/file/", upload_settings={"elementPathEnabled":True},blank=True,default='')

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings
class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/image/%Y/%m', default='static/image/default.jpg', max_length=200,
                              blank=True, null=True, verbose_name='用户头像')
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username


from django.core.paginator import Paginator
class myPaginator(Paginator):
    """
    是自定制django分页类的方法
    :page_num_range 显示返回页数范围
    :current_page  当前页数
    :max_page_num 最大显示的页码数
    """
    def __init__(self, current_page, max_pager_num, *args, **kwargs):
        # 当前页
        self.current_page = int(current_page)
        # 最多显示的页码数量
        self.max_pager_num = int(max_pager_num)
        super(myPaginator,self).__init__(*args, **kwargs)

    def page_num_range(self):
        # 当前页
        # self.current_page
        # 最多显示的页码数量 11
        # self.per_pager_num
        # 总页数
        # self.num_pages

        # 判断如果页面总数量小于显示页面的总数量，那么返回最大的页面总数量。
        if self.num_pages < self.max_pager_num:
            return range(1, self.num_pages + 1)
        part = int(self.max_pager_num / 2)

        # 判断当前页小于等于最大显示页的一半，那么返回1到最大显示页数量。
        if self.current_page <= part:
            return range(1, self.max_pager_num + 1)

        # 当选择页数加上显示页数的一半的时候，说明越界了，例如最大也数是15，显示页数是10，我选择11页，那么11+5等于16，大于15，那么就显示总页数15-11+1，15+1
        if (self.current_page + part) > self.num_pages:
            # 那么返回总页数前去当前显示页数个数+1的值，和总页数+1的值。
            return range(self.num_pages - self.max_pager_num + 1, self.num_pages + 1)

        # 当选择页大于当前总页数的一半的时候，返回当前选择页的前五个和后五个页数。
        return range(self.current_page - part, self.current_page + part + 1)


