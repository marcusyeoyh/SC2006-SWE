from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from rest_framework import status
import json
import time
import googlemaps
import pandas as pd
from geopy.distance import geodesic



"""
Class based view for base search function. Accepts 1 parameter: search_val from GoogleMaps searchbar.
"""
class SearchView(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            search_val = request.GET['search_val']

            queryset = models.AllFlat.objects.using('flats').filter(street_name__contains=search_val).values('id', 'block', 'street_name', 'flat_type', 'storey_range', 'floor_area_sqm', 'flat_model', 'remaining_lease', 'predictedprice', 'likes')[:5]
            if not queryset:
                return Response({})
            else:
                query_list = list(queryset)

            return Response(query_list, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})


"""
Class based view for comparison function. Accepts 2 parameters: search_val from GoogleMaps searchbar, and flat_type from custom user select
"""
class ComparisonView(APIView):  
    def get(self, request):
        if 'search_val' and 'flat_type' in request.GET: 
            search_val = request.GET['search_val']
            flat_type = request.GET['flat_type']

            queryset = models.AllFlat.objects.using('flats').filter(street_name__contains=search_val, flat_type__contains=flat_type).values('predictedprice')[:1]
            if not queryset:
                return Response({})
            else:
                price = queryset[0]

            return Response(price, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})


"""
Endpoint to increment LIKES value by 1 with each call. Accepts 1 parameter: id
"""
class UpdateLikesView(APIView):
    def get(self, request):
        if 'id' in request.GET:
            id = request.GET['id']

            query = models.AllFlat.objects.using('flats').get(id=id)

            if not query:
                print("no query")
                return Response({})
            else:
                query.likes = query.likes + 1
                query.save(update_fields=["likes"])

            return Response(query.likes, status=status.HTTP_200_OK, content_type='application/json')
    
        print("no param in request.GET")
        return Response({})



"""
Amenities endpoints
"""        
class Airport(APIView):
    def get(self, request):
        if 'search_val' in request.GET:

            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'airport' #this is the value which you are gna be searching
            distance = 10 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 3: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1


            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})


class ATM(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'ATM' #this is the value which you are gna be searching
            distance = 5 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 40: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})


class Buses(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'bus stop' #this is the value which you are gna be searching
            distance = 0.2 * 1_609.344  #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 3: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})



class Clinic(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'clinic' #this is the value which you are gna be searching
            distance = 1 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 15: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})



class Grocery(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'super market' #this is the value which you are gna be searching
            distance = 0.2 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 10: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            result = json.dumps(nearby_buses)

            print(result)

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})



class Hospital(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'hospital' #this is the value which you are gna be searching
            distance = 1.5 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 3: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})



class Mall(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'mall' #this is the value which you are gna be searching
            distance = 2 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 10: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})




class MRT(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'mrt' #this is the value which you are gna be searching
            distance = 1.5 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 3: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})



class Restaurant(APIView):
    def get(self, request):
        if 'search_val' in request.GET:
            API_KEY = 'AIzaSyAJy82TVP3JryIg444dv-DfcDUnFoG-tt4'
            map_client = googlemaps.Client(API_KEY)

            address = request.GET['search_val'] #this is the location u wish to search
            geocode = map_client.geocode(address=address)
            (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

            input_lat = lat
            input_lng = lng

            search_string = 'restaurant' #this is the value which you are gna be searching
            distance = 1 * 1_609.344 #this is the radius in miles that you wanna search
            business_list = [] 


            response = map_client.places_nearby(
                location=(lat, lng),
                keyword=search_string,
                radius=distance
            )   


            business_list.extend(response.get('results'))
            next_page_token = response.get('next_page_token')

            while next_page_token:
                time.sleep(2)
                response = map_client.places_nearby(
                    location=(lat, lng),
                    keyword=search_string,
                    radius=distance,
                    page_token=next_page_token
                )   
                business_list.extend(response.get('results'))
                next_page_token = response.get('next_page_token')

            df = pd.DataFrame(business_list)
            df.drop(df.columns[[0, 2, 3, 4, 6, 7,8,9,10,11,12,13,14]], axis=1, inplace=True)
            df['Latitude'] = df.loc[:, 'geometry']
            df['Longitude'] = df.loc[:, 'geometry']
            df.drop(df.columns[[0]], axis=1, inplace=True)

            i=0
            name = []
            latitude = []
            longitude = []
            calculated_dist = []
            while i < 10: 
                name.append(df.at[i, 'name'])
                x = df.at[i,'Latitude']
                lat_lng = x["location"]
                latitude.append(lat_lng["lat"])
                longitude.append(lat_lng["lng"])
                coord1 = (lat_lng["lat"],lat_lng["lng"])
                coord2 = (input_lat, input_lng)
                calculated_dist.append(geodesic(coord1,coord2).km)
                i = i + 1

            i = 0

            nearby_bus = {"names":name, "latitudes": lat, "longitudes":lng, "distance":calculated_dist}
            buses_df = pd.DataFrame(nearby_bus)
            buses_df = buses_df.sort_values(by=['distance'], ascending=True)

            nearby_buses = [1,2,3]

            while i < 3:
                name_dist = buses_df.iloc[i,0] + ', ' + str(round(buses_df.iloc[i,3], 3)) + 'km'
                nearby_buses[i] = {"label":name_dist, "latitude": buses_df.iloc[i,1], "longitude": buses_df.iloc[i,2], 
                "distance":round(buses_df.iloc[i,3], 3)}
                i = i+1

            return Response(nearby_buses, status=status.HTTP_200_OK, content_type='application/json')

        return Response({})