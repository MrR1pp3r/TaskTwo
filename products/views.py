from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductImageSerialzier, ProductImagePSerializer
from .models import Product, ProductImage


class ProductView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        context = {
            "status": status.HTTP_200_OK,
            "error": None,
            "data": serializer.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "status": status.HTTP_201_CREATED,
                "error": None,
                "data": "Product Created.",
            }
            return Response(context, status=status.HTTP_201_CREATED)


class ProductImageView(APIView):
    def get(self, request):
        queryset = ProductImage.objects.all()
        serializer = ProductImageSerialzier(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductImagePSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            context = {
                "status": status.HTTP_201_CREATED,
                "error": None,
                "data": "Image Inserted."
            }
            return Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "error": True,
                "data": "Error"
            }
            return Response(data=context, status=status.HTTP_400_BAD_REQUEST)
