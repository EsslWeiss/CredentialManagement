from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Customer
from .serializers import CustomerSerializer


@api_view(['GET', 'POST'])
def customers_list(request):
    """
        Представление получение списка пользователей и создания пользователя.
    """
    if request.method == 'GET':
        paginate_data = []
        nextPage = 1
        prevPage = 1
        customers = Customer.objects.all()
        current_page = request.GET.get('page', 1)  # Получаем страницу из GET параментров
        paginator = Paginator(customers, 5)

        try:  # Получаем текушую страницу из GET параметров
            paginate_data = paginator.get_page(current_page)
        except PageNotAnInteger:  # Если GET параметр не является целочисленным полем, то берем первую страницу
            paginate_data = paginator.get_page(1)
        except EmptyPage:  # Если текущая страница пустая, то возвращаем последнюю страницу
            paginate_data = paginator.get_page(paginator.num_pages)

        serializer = CustomerSerializer(paginate_data, context={'request': request}, many=True)  # Сериализация Queryset структуры
        if paginate_data.has_next():  # Если для текущей страницы есть следующая страница, то добавляем её в nextPages
            nextPage = paginate_data.next_page_number()
        if paginate_data.has_previous():  # Если для текущей страницы есть предыдущая страница, то добавляем её в prevPages
            prevPage = paginate_data.previous_page_number()

        context = {
            'data': serializer.data,  # Данные представленные в OrderedDict
            'count': paginator.count,  # Общее количество данных 
            'numpages': paginator.num_pages,  # Общее количество страниц
            'nextlink': '/api/customers/?page=' + str(nextPage),  # Ссылка на следующуу страницу
            'prevlink': '/api/customers/?page=' + str(prevPage)  # Ссылка на предыдущюю страницу
        }
        print('NEXTLINK: ', context['nextlink'])
        print('PREVLINK: ', context['prevlink'])
        return Response(context)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)  # Десериализация данных
        if serializer.is_valid():  # Если десериализованные данные валидны, сохраняем их возвращаем сохранённые данные
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)  # Данные не валидны. возвращаем ошибки и сататус 404

@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    """
        Представление взятия, обновления и удаления пользователя по первичному ключу
    """
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        print(request.data)
        serializer = CustomerSerializer(customer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

