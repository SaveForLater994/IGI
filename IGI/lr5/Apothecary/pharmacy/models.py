from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.
class ActiveIngredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название вещества"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    
    class Meta:
        verbose_name = "Действующее вещество"
        verbose_name_plural = "Действующие вещества"
        ordering = ['name']
    
    def __str__(self):
        return self.name
class PharmacyDepartment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MedicationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+375 \(\d\d\) \d{3}-\d{2}-\d{2}$', message="Format: +375 (XX) XXX-XX-XX")])
    email = models.EmailField(blank=True)
    inn = models.CharField(max_length=12, blank=True)
    address = models.TextField(blank=True)
    medications = models.ManyToManyField(
        'Medication',
        related_name='suppliers',
        blank=True,
        verbose_name="Поставляемые лекарства"
    )
    
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ['name']
    def get_medications(self):
        return ', '.join([medication.name for medication in self.medications.all()[:3]])
    get_medications.short_description = 'Supplier'
    def __str__(self):
        return self.name

class Medication(models.Model):
    ndc = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='medications/', blank=True, null=True)
    department = models.ForeignKey(PharmacyDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(MedicationCategory, on_delete=models.SET_NULL, null=True, blank=True)
    last_api_update = models.DateTimeField(auto_now=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Цена"
    )
    requires_prescription = models.BooleanField(
        default=False,
        verbose_name="Рецептурный препарат"
    )
    manufacturer = models.CharField(
        max_length=200,
        verbose_name="Производитель"
    )
    active_ingredients = models.ManyToManyField(
        'ActiveIngredient',
        related_name='medications',
        verbose_name="Действующие вещества"
    )
    def get_active_ingredients(self):
        return ', '.join([act_ing.name for act_ing in self.active_ingredients.all()[:3]])
    get_active_ingredients.short_description = 'Medication'
    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.ForeignKey(PharmacyDepartment, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+375 \(\d\d\) \d{3}-\d{2}-\d{2}$', message="Format: +375 (XX) XXX-XX-XX")])
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(
    upload_to='employees/',
    blank=True,
    null=True,
    verbose_name="Фото"
)
    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return {self.user.username}

        

class Sale(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    buyer_name = models.CharField(max_length=100, blank=True)
    buyer_phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+375 \(\d\d\) \d{3}-\d{2}-\d{2}$', message="Format: +375 (XX) XXX-XX-XX")])

    def __str__(self):
        return f"{self.medication} sold by {self.employee}, total price: {self.total_price}"

class Vacancy(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_("Название вакансии")
    )
    description = models.TextField(
        verbose_name=_("Описание")
    )
    requirements = models.TextField(
        verbose_name=_("Требования")
    )
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Зарплата ($)"),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Активна")
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("Дата размещения")
    )

    class Meta:
        verbose_name = _("Вакансия")
        verbose_name_plural = _("Вакансии")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({'активна' if self.is_active else 'закрыта'})"
    
    def get_formatted_salary(self):
        if self.salary:
            return f"{self.salary:,.2f}".replace(',', ' ').replace('.', ',')
        return _("По договорённости")
   
class FAQ(models.Model):
    # Типы записей
    QUESTION = 'question'
    TERM = 'term'
    ENTRY_TYPE_CHOICES = [
        (QUESTION, 'Частый вопрос'),
        (TERM, 'Термин глоссария'),
    ]
    
    # Поля модели
    entry_type = models.CharField(
        max_length=10,
        choices=ENTRY_TYPE_CHOICES,
        default=QUESTION,
        verbose_name="Тип записи"
    )
    question = models.CharField(
        max_length=300,
        verbose_name="Вопрос/Термин"
    )
    answer = models.TextField(
        verbose_name="Ответ/Определение"
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Словарь терминов и FAQ"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entry_type']),
        ]

    def __str__(self):
        return self.question[:50] + ("..." if len(self.question) > 50 else "")
    
class PromoCode(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активный'
        INACTIVE = 'inactive', 'Неактивный'
        EXPIRED = 'expired', 'Истек'
        USED = 'used', 'Использован'
        PENDING = 'pending', 'Ожидает активации'
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Промокод"
    )
    discount = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Скидка (%)"
    )
    max_uses = models.PositiveIntegerField(
        default=1,
        verbose_name="Максимальное количество использований"
    )
    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество использований"
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Действует с"
    )
    end_date = models.DateTimeField(
        verbose_name="Действует до",
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    applied_promo = models.ForeignKey(
        'PromoCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Примененный промокод"
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Сумма скидки"
    )
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Итоговая цена со скидкой"
    )
    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} ({self.discount}%)"
    def apply_promo(self, promo_code):
        """Применить промокод к этой позиции"""
        if promo_code and promo_code.status == PromoCode.Status.ACTIVE:
            self.applied_promo = promo_code
            discount = self.total_price * (promo_code.discount / 100)
            self.discount_amount = discount
            self.final_price = self.total_price - discount
            self.save()
            return True
        return False
    @property
    def status(self):
        now = timezone.now()
        if not self.is_active:
            return self.Status.INACTIVE
        if self.used_count >= self.max_uses:
            return self.Status.USED
        if now < self.start_date:
            return self.Status.PENDING
        if now > self.end_date:
            return self.Status.EXPIRED
        return self.Status.ACTIVE
    
    @property
    def status_display(self):
        return dict(self.Status.choices).get(self.status, self.status)
    
    @property
    def remaining_uses(self):
        return max(0, self.max_uses - self.used_count)
    
class News(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    summary = models.CharField(
        max_length=200,
        verbose_name="Краткое описание"
    )
    image = models.ImageField(
        upload_to='news/',
        verbose_name="Изображение"
    )
    full_text = models.TextField(
        verbose_name="Полный текст"
    )
    publish_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано"
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

class Contact(models.Model):
    company_name = models.CharField(
        max_length=100,
        verbose_name="Название компании"
    )
    address = models.TextField(
        verbose_name="Адрес"
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                message="Формат: +375 (29) XXX-XX-XX"
            )
        ],
        verbose_name="Телефон"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    requisites = models.TextField(
        verbose_name="Реквизиты",
        help_text="Банковские реквизиты компании"
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.company_name

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звёзд'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Пользователь"
    )
    text = models.TextField(
        max_length=2000,
        verbose_name="Текст отзыва"
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.user.username} ({self.created_at.date()})"
    
class CompanyInfo(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    content = models.TextField(
        verbose_name="Основной текст"
    )
    history = models.TextField(
        blank=True,
        verbose_name="История по годам"
    )
    requisites = models.TextField(
        blank=True,
        verbose_name="Реквизиты"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    
    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"
    
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.birth_date}"
    
class CartItem(models.Model):
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Лекарство"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Корзина",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
    
    def __str__(self):
        return f"{self.medication.name} (x{self.quantity})"
    
    @property
    def total_price(self):
        """Общая стоимость этой позиции"""
        return self.medication.price * self.quantity
    
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Пользователь"
    )
    applied_promo = models.ForeignKey(
        'PromoCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Примененный промокод"
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Сумма скидки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создана"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлена"
    )
    
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def get_total(self):
        """Общая стоимость корзины без скидки"""
        return sum(item.total_price for item in self.cart_items.all())
    
    def get_final_total(self):
        """Итоговая стоимость со скидкой"""
        return self.get_total() - self.discount_amount
    
    def apply_promo(self, promo_code):
        """Применить промокод к корзине"""
        if promo_code and promo_code.status == PromoCode.Status.ACTIVE:
            self.applied_promo = promo_code
            discount = self.get_total() * (promo_code.discount / 100)
            self.discount_amount = discount
            self.save()
            return True
        return False
    
class PickupPoint(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    address = models.CharField(max_length=300, verbose_name="Адрес")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        verbose_name = "Точка самовывоза"
        verbose_name_plural = "Точки самовывоза"
    
    def __str__(self):
        return self.name