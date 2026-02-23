from django.shortcuts import render
from .models import Ticket
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializer import TicketSerializer
@api_view(['GET','POST'])

def description_list(request):
    if request.method=='GET':
        tickets=Ticket.objects.all()
        category=request.query_params.get('category')
        status=request.query_params.get('search')
        if category:
            tickets=tickets.filter(category=category)
        if status:
            tickets=tickets.filter(status=status)
        search=request.query_params.get('search')
        if search:
            tickets = tickets.filter(title__icontains=search)

        ordering=request.query_params.get('ordering')
        if ordering=='priority':
            tickets=tickets.order_by('priority')
        if ordering=='created-at':
            tickets=tickets.order_by('created_at')
        

        paginator=PageNumberPagination()
        paginator.page_size=3
        paginated_tickets=paginator.paginate_queryset(tickets,request)
        if paginated_tickets is not None:
            serializer = TicketSerializer(paginated_tickets, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer=TicketSerializer(paginated_tickets,many=True)
        return paginator.get_paginated_response(serializer.data)
    

    if request.method=='POST':
        serializer=TicketSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

@api_view(['GET','PUT','DELETE','PATCH'])
@permission_classes([IsAuthenticated])
def ticket_detail(request,id):
    try:
        tickets=Ticket.objects.get(id=id)
    except Ticket.DoesNotExist:
        return Response({'error': 'not found'},status=404)
    
    if request.method=='GET':
        serializer=TicketSerializer(Ticket)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = TicketSerializer(Ticket, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
        
    if request.method == 'PATCH':
        serializer = TicketSerializer(Ticket, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    
    if request.method == 'DELETE':
        Ticket.delete()
        return Response({'message': 'deleted successfully'}, status=204)