from rest_framework import serializers

from django.conf import settings
from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Слишком много студентов на курсе')
        return value
