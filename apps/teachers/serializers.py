from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment,GRADE_CHOICES


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Student Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        if 'content' in attrs and attrs['content']:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')
        if self.instance.teacher != attrs['teacher']:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')
        if 'grade' in attrs:
            if self.instance.state == 'DRAFT':
                raise serializers.ValidationError('SUBMITTED assignments can only be graded')
            elif self.instance.state == 'GRADED':
                raise serializers.ValidationError('GRADED assignments cannot be graded again')
        if self.partial:
            return attrs
        return super().validate(attrs)