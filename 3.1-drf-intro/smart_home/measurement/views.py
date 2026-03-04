from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, \
    CreateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, FullSensorSerializer, \
    MeasurementSerializer


class SensorsView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class OneSensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = FullSensorSerializer


class TempAdd(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer