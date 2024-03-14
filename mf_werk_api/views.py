from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from .models import Part
from .serializers import PartSerializer
from .utils.mf_werk_utils import Mf_werk_drawing

#################

class PartListApiView(APIView):

    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the part items for given requested user
        '''
        parts = Part.objects.filter(user = request.user.id)
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the part with given part data
        '''

        part_name = request.data.get('name')
        truncated_part_name = part_name[:80]
        uploaded_file = request.data.get('org_file')
        #truncated_filename = uploaded_file.name[:100]
        #uploaded_file.name = truncated_filename
        uploaded_file.name = truncated_part_name + '-org-file.pdf'

        data = {
            'name': part_name, 
            'mf_id': request.data.get('mf_id'), 
            'org_file': uploaded_file, 
            'user': request.user.id
        }
        serializer = PartSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. Delete
    def delete(self, request, *args, **kwargs):
        '''
        Delete all the part items for given requested user
        '''
        parts = Part.objects.filter(user = request.user.id)
        parts.delete()
        return Response(
            {"res": "Objects deleted!"},
            status=status.HTTP_200_OK
        )

class PartDetailApiView(APIView):

    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, part_id, user_id):

        '''
        Helper method to get the object with given part_id, and user_id
        '''
        try:
            return Part.objects.get(id=part_id, user = user_id)
        except Part.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, part_id, *args, **kwargs):

        '''
        Retrieves the part with given part_id
        '''

        part_instance = self.get_object(part_id, request.user.id)
        if not part_instance:
            return Response(
                {"res": "Object with part id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PartSerializer(part_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, part_id, *args, **kwargs):

        '''
        Updates the part item with given part_id if exists
        '''

        part_instance = self.get_object(part_id, request.user.id)
        if not part_instance:
            return Response(
                {"res": "Object with part id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {}

        serializer = PartSerializer(instance = part_instance, data=data, partial = True)

        if serializer.is_valid():

            #serializer.save()
            task = request.data.get('task')

            if task == 'drawing_data':
                    
                base_dir = settings.BASE_DIR
                name = serializer.data['name']
                mf_id = serializer.data['mf_id']
                org_file_full_url = str(base_dir) + serializer.data['org_file']

                mf_werk_drawing = Mf_werk_drawing(name, mf_id, org_file_full_url, "", "", "")
                drawing_data = mf_werk_drawing.get_drawing_data()

                werk_data = {
                    'drawing_id': drawing_data.get('drawing_id'),
                    'material': drawing_data.get('material'),
                    'part_ids': drawing_data.get('part_ids'),
                    'weight': drawing_data.get('weight'),
                    'designation': drawing_data.get('designation'),
                    'general_tolerances': drawing_data.get('general_tolerances')
                }

                serializer = PartSerializer(instance = part_instance, data=werk_data, partial = True)

                if serializer.is_valid():

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif task == 'branded_drawing':

                print("branded drawing")

                base_dir = settings.BASE_DIR
                name = serializer.data['name']
                mf_id = serializer.data['mf_id']

                requested_material_title = request.data.get('material_title')
                requested_part_number_title = request.data.get('part_number_title')
                requested_designation_title = request.data.get('designation_title')

                org_file_full_url = str(base_dir) + serializer.data['org_file']

                mf_werk_drawing = Mf_werk_drawing(name, mf_id, org_file_full_url, requested_material_title, requested_part_number_title, requested_designation_title)
                branded_file_url = mf_werk_drawing.get_branded_drawing()

                werk_data = {
                    'branded_file_url': branded_file_url,
                }

                serializer = PartSerializer(instance = part_instance, data=werk_data, partial = True)

                if serializer.is_valid():

                    serializer.save()

                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, part_id, *args, **kwargs):

        '''
        Deletes the part item with given part_id if exists
        '''

        part_instance = self.get_object(part_id, request.user.id)
        if not part_instance:
            return Response(
                {"res": "Object with part id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        part_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

###########################



