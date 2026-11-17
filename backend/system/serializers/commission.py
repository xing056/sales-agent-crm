from ..models import Commission
from .serializer import BaseSerializer,UserBriefSerializer
# 员工提成表模型类序列化器
class CommissionSerializer(BaseSerializer):
    # user_id字段关联数据序列化器（只要姓名和 id，不带手机/邮箱/角色）
    user=UserBriefSerializer(read_only=True)
    class Meta:
        model=Commission
        fields='__all__'
