# Rest Imports
from rest_framework                     import status
from rest_framework.authtoken.models    import Token
from rest_framework.views               import APIView
from rest_framework.response            import Response
from rest_framework.permissions         import IsAuthenticated, IsAdminUser

# Django Imports
from django.shortcuts               import get_object_or_404
from django.contrib.auth.models     import update_last_login

# Local Imports
from orders.models      import ServiceOrder
from ..                 import serializers


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        update_last_login(None, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": status.HTTP_200_OK, "Token": token.key})


class ServiceOrderAPIView(APIView):
    """
    This is a Python class named ServiceOrderAPIView that extends the APIView class from the rest_framework module. It contains four methods - get(), post(), put(), and delete() - which correspond to the HTTP GET, POST, PUT, and DELETE methods respectively.

    The serializer attribute is set to ServiceOrderSerializer, which is a serializer class defined elsewhere in the module. The permission_classes attribute is a list of two permission classes - IsAuthenticated and IsAdminUser - which are required for accessing the view.
    """
    serializer = serializers.ServiceOrderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request) -> Response:
        """
        Retrieves a ServiceOrder instance with a given order_id parameter from the request's query string using the get_object_or_404() function, which raises a 404 Http404 exception if the object is not found. The method then returns a Response object containing the retrieved instance.
        """
        order = request.GET['order_id']
        return get_object_or_404(order)

    def post(self, request) -> Response:
        """
        Creates a new ServiceOrder instance with the data from the request's POST parameters, using the create() method of the ServiceOrder model. It then returns a Response object with the created instance and a HTTP_201_CREATED status code.
        """
        service_order = request.POST['service_order']
        so = ServiceOrder.objects.create(
            customer = service_order.customer,
            hardware = service_order.hardware,
            end_date = service_order.end_date,
            status = service_order.status
        )
        return Response(so, status=status.HTTP_201_CREATED)

    def put(self, request) -> Response:
        """
        Updates an existing ServiceOrder instance with the data from the request's POST parameters. It first retrieves the original instance with the given id parameter and then iterates over the POST parameters to update the instance's attributes. The method then returns a Response object with a HTTP_200_OK status code.
        """
        service_order = request.POST['service_order']
        original = ServiceOrder.objects.get(pk=service_order.id)
        
        for k, v in service_order.items():
            if k == 'id':
                continue
            original.k = v
        return Response(status=status.HTTP_200_OK)

    def delete(self, request) -> Response:
        """
        Deletes a ServiceOrder instance with a given order_id parameter from the request's DELETE parameters. It uses the delete() method of the ServiceOrder model to delete the instance and returns a Response object with a HTTP_204_NO_CONTENT status code.
        """
        ServiceOrder.objects.get(pk=request.DELETE['order_id']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

