from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ActiveIngredient, PharmacyDepartment, MedicationCategory, Supplier, Medication, Employee, Sale, Vacancy, FAQ, PromoCode, News, Contact, Review, CompanyInfo,CartItem, Cart, PickupPoint
from django.utils import timezone
from django.db.models import F, Q
from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from calendar import monthcalendar
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Sum
from django.core.serializers import serialize
from django.http import JsonResponse
import json
import requests
from tzlocal import get_localzone
def index(request):
    latest_new = News.objects.first()
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    current_month_name = today.strftime('%B')
    today_day = today.day
    local_tz = get_localzone()
    local_time = datetime.now(local_tz)
    calendar_weeks = monthcalendar(current_year, current_month)
    return render(request, 'index.html', context={'u_title':latest_new.title, 'u_content':latest_new.full_text,'u_date':latest_new.publish_date,'u_image':latest_new.image, 'today':today, 'current_year': current_year,
        'current_month_name': current_month_name,
        'today_day': today_day,
        'calendar_weeks': calendar_weeks,'local_time': local_time,},)

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'about.html', {
        'company_info': company_info,
    })

def news_list(request):
    news_list = News.objects.filter(is_published=True)
    return render(request, 'news_list.html', {
        'news_list': news_list,
    })

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'news_detail.html', {
        'news': news,
    })
@login_required
def faq(request):
    faq_list = FAQ.objects.all()
    drug_info = None
    search_query = None
    
    if request.method == 'POST' and 'search_drug' in request.POST:
        search_query = request.POST.get('drug_name', '').strip()
        if search_query:
            # Формируем запрос к OpenFDA
            url = f"https://api.fda.gov/drug/label.json?search={search_query}&limit=1"
            
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'results' in data and data['results']:
                    result = data['results'][0]
                    
                    # Извлекаем нужные поля
                    drug_info = {
                        'brand_name': result.get('openfda', {}).get('brand_name', ['Не указано'])[0],
                        'generic_name': result.get('openfda', {}).get('generic_name', ['Не указано'])[0],
                        'manufacturer': result.get('openfda', {}).get('manufacturer_name', ['Не указано'])[0],
                        'description': result.get('description', 'Описание не найдено'),
                        'warnings': result.get('warnings', 'Предупреждения не указаны'),
                        'indications_and_usage': result.get('indications_and_usage', 'Показания не указаны'),
                        'dosage_and_administration': result.get('dosage_and_administration', 'Дозировка не указана'),
                        'adverse_reactions': result.get('adverse_reactions', 'Побочные реакции не указаны'),
                    }
                else:
                    drug_info = {'error': f'Лекарство "{search_query}" не найдено в OpenFDA'}
                    
            except requests.exceptions.RequestException as e:
                drug_info = {'error': f'Ошибка при запросе к OpenFDA: {str(e)}'}
    
    return render(request, 'faq.html', {
        'faq_list': faq_list,
        'drug_info': drug_info,
        'search_query': search_query,
    })
def contacts(request):
    """Страница контактов со списком сотрудников"""
    employees = Employee.objects.all()
    return render(request, 'contacts.html', {
        'employees': employees,
    })

def privacy(request):
    return render(request, 'privacy.html')

def vacancies(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'vacancies.html', {
        'vacancies': vacancies,
    })

def reviews(request):
    reviews = Review.objects.filter(is_published=True)
    return render(request, 'reviews.html', {
        'reviews': reviews,
    })

@login_required
def add_review(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text and rating:
            Review.objects.create(
                user=request.user,
                text=text,
                rating=int(rating),
                is_published=True
            )
            messages.success(request, 'Отзыв успешно добавлен!')
        else:
            messages.error(request, 'Заполните все поля!')
        return redirect('reviews')
    return render(request, 'review_form.html')

def promocodes(request):
    nw = datetime.now()
    active_promocodes = PromoCode.objects.filter(
        is_active=True,
        start_date__lte=nw,
        end_date__gte=nw,
        used_count__lt=F('max_uses')
    )
    expired_promocodes = PromoCode.objects.filter(
        Q(end_date__lt=nw) | 
        Q(used_count__gte=F('max_uses')) |
        Q(is_active=False)
    )
    return render(request, 'promo_codes.html', {
        'active_promocodes': active_promocodes,
        'expired_promocodes': expired_promocodes,
    })
class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Введите дату рождения (для проверки возраста)'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date')
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        
        if not birth_date:
            raise ValidationError('Пожалуйста, укажите дату рождения')
        
        # Вычисляем возраст
        today = datetime.now().date()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        if age < 18:
            raise ValidationError('Регистрация разрешена только лицам старше 18 лет')
        
        return birth_date

# Функция регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            buyer_group = Group.objects.get(name='Customer')
            user.groups.add(buyer_group)
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
def is_buyer(user):
    return user.groups.filter(name='Customer').exists() or user.is_superuser

def get_or_create_cart(user):
    """Получить или создать корзину для пользователя"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@user_passes_test(is_buyer)
@login_required
def cart_view(request):
    """Отображение корзины"""
    cart = get_or_create_cart(request.user)
    cart_items = cart.cart_items.all()
    total = cart.get_total()
    final_total = cart.get_final_total()
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'final_total': final_total,
        'discount_amount': cart.discount_amount,
        'applied_promo': cart.applied_promo,
    })

@user_passes_test(is_buyer)
@login_required
def add_to_cart(request, medication_id):
    """Добавление товара в корзину"""
    medication = get_object_or_404(Medication, id=medication_id)
    
    # Получаем корзину пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Создаём или обновляем позицию в корзине
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medication=medication
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество "{medication.name}" увеличено.')
    else:
        messages.success(request, f'"{medication.name}" добавлен в корзину.')
    
    return redirect('cart')

@user_passes_test(is_buyer)
@login_required
def remove_from_cart(request, cart_item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, 'Товар удалён из корзины.')
    return redirect('cart')

@user_passes_test(is_buyer)
@login_required
def update_cart_quantity(request, cart_item_id, action):
    """Увеличение/уменьшение количества"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            messages.success(request, 'Товар удалён из корзины.')
            return redirect('cart')
    
    cart_item.save()
    return redirect('cart')
@user_passes_test(is_buyer)
@login_required
def apply_promo(request):
    """Применение промокода к корзине"""
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code', '').strip().upper()
        cart = get_or_create_cart(request.user)
        
        if not cart.cart_items.exists():
            messages.error(request, 'Корзина пуста!')
            return redirect('cart')
        
        try:
            promo = PromoCode.objects.get(code=promo_code)
        except PromoCode.DoesNotExist:
            messages.error(request, 'Промокод не найден')
            return redirect('cart')
        
        if promo.status != PromoCode.Status.ACTIVE:
            messages.error(request, f'Промокод неактивен: {promo.status_display}')
            return redirect('cart')
        
        if cart.apply_promo(promo):
            messages.success(request, f'Промокод "{promo_code}" применен! Скидка: {promo.discount}%')
        else:
            messages.error(request, 'Не удалось применить промокод')
        
        return redirect('cart')
    
    return redirect('cart')


def medication_list(request):
    medications = Medication.objects.all()
    
    q = request.GET.get('q')
    if q:
        medications = medications.filter(name__icontains=q)

    category_id = request.GET.get('category')
    if category_id:
        medications = medications.filter(category_id=category_id)
    
    prescription = request.GET.get('prescription')
    if prescription == 'yes':
        medications = medications.filter(requires_prescription=True)
    elif prescription == 'no':
        medications = medications.filter(requires_prescription=False)

    categories = MedicationCategory.objects.all()
    
    return render(request, 'medication_list.html', {
        'medications': medications,
        'categories': categories,
    })
@user_passes_test(is_buyer)
@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.cart_items.all()
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pickup_point_id = request.POST.get('pickup_point')
        
        if not pickup_point_id and not address:
            messages.error(request, 'Выберите точку самовывоза или укажите адрес доставки!')
            return redirect('checkout')
        if not address or not phone:
            messages.error(request, 'Заполните все поля!')
            return redirect('checkout')
        
        with transaction.atomic():
            # Создаём продажи
            for item in cart_items:
                Sale.objects.create(
                    medication=item.medication,
                    employee=None,  # Пока нет сотрудника
                    quantity=item.quantity,
                    price_per_unit=item.medication.price,
                    total_price=item.total_price,
                    buyer_name=request.user.username,
                    buyer_phone=phone
                )
            
            # Очищаем корзину
            cart.cart_items.all().delete()
            cart.discount_amount = 0
            cart.applied_promo = None
            cart.save()
        
        messages.success(request, 'Заказ оформлен!')
        return redirect('index')
    pickup_points = list(PickupPoint.objects.filter(is_active=True).values('latitude', 'longitude', 'address', 'name'))
    pickup_points_json = json.dumps(pickup_points)
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': cart.get_final_total(),
        'discount_amount': cart.discount_amount,
        'applied_promo': cart.applied_promo,
        'pickup_points': pickup_points_json,
    })
def is_employee(user):
    return user.groups.filter(name='Employee').exists() or user.is_superuser

@user_passes_test(is_employee)
def sales_chart(request):
    """Страница с графиком продаж и таблицей поставщиков для сотрудников"""
    # 1. Данные для круговой диаграммы
    sales_data = (
        Sale.objects.values('medication__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )
    
    labels = [item['medication__name'] for item in sales_data]
    sizes = [item['total_sold'] for item in sales_data]
    
    suppliers = Supplier.objects.all()
    
    chart_image = None
    if labels:
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Распределение продаж по лекарствам')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        chart_image = image_base64
    
    return render(request, 'sales_chart.html', {
        'chart': chart_image,
        'suppliers': suppliers,
        'message': 'Нет данных о продажах' if not labels else None,
    })
def create_superuser(request):
    """Создать суперпользователя (только для первого запуска)"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        return JsonResponse({'status': 'superuser created'})
    else:
        return JsonResponse({'status': 'superuser already exists'})