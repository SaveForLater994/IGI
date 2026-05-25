from django.contrib import admin
from .models import ActiveIngredient, PharmacyDepartment, MedicationCategory, Supplier, Medication, Employee, Sale, Vacancy, FAQ, PromoCode, News, Contact, Review, CompanyInfo, Profile, CartItem, Cart, PickupPoint
#admin.site.register(ActiveIngredient)
#admin.site.register(PharmacyDepartment)
#admin.site.register(MedicationCategory)
#admin.site.register(Supplier)
#admin.site.register(Medication)
#admin.site.register(Employee)
#admin.site.register(Sale)
#admin.site.register(Vacancy)
#admin.site.register(FAQ)
#admin.site.register(PromoCode)
#admin.site.register(News)
#admin.site.register(Contact)
#admin.site.register(Review)
#admin.site.register(CompanyInfo)
# Register your models here.

@admin.register(ActiveIngredient)
class ActiveIngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
@admin.register(PharmacyDepartment)
class PharmacyDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
@admin.register(MedicationCategory)
class MedicationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'inn', 'address', 'get_medications')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('ndc', 'name','image','department','category','last_api_update','requires_prescription','manufacturer','get_active_ingredients')
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position','department','phone','hire_date','salary', 'photo')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('medication', 'employee', 'quantity', 'price_per_unit', 'total_price', 'sale_date', 'buyer_name', 'buyer_phone')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title','description','requirements','get_formatted_salary','is_active','created_at')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('entry_type','question','answer','created_at','updated_at')
    
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code','discount','max_uses','status_display','remaining_uses','start_date','end_date','is_active','created_at', 'updated_at')
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','summary','image','full_text','publish_date','is_published')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('company_name','address','phone','email','requisites')
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','text','rating','created_at','updated_at','is_published')

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title','content','history','requisites','updated_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'phone')
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('medication', 'quantity', 'added_at')
    list_filter = ('medication', 'added_at')
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'applied_promo', 'discount_amount', 'get_total', 'get_final_total', 'created_at')
    list_filter = ('applied_promo', 'created_at')
    search_fields = ('user__username', 'applied_promo__code')
    readonly_fields = ('get_total', 'get_final_total')
    
    def get_total(self, obj):
        return f"{obj.get_total()} BYN"
    get_total.short_description = "Общая сумма"
    
    def get_final_total(self, obj):
        return f"{obj.get_final_total()} BYN"
    get_final_total.short_description = "Итоговая сумма"

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('name','address', 'latitude', 'longitude', 'is_active')
    list_filter = ('name', 'is_active')