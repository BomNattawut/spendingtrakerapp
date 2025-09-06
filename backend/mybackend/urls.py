from django.urls import path
from .views import RegisterView,Login,BudgetCreateView,BudgetListView,ExpenseCategoryListView,ExpenseFormView,ExpenseListView,BudgetDeleteView,ExpenseDeleteView,ProfileView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('Register/', RegisterView.as_view(), name='Register'),
    path('Login/',Login.as_view(),name='Login'),
    path('BudgetCreatview/',BudgetCreateView.as_view(),name='ButgetCreatview'),
    path('budgets/', BudgetListView.as_view(), name='budget-list'), 
    path('expense-categories/', ExpenseCategoryListView.as_view(), name='expense-category-list'),
    path('expenses/',ExpenseFormView.as_view(),name='expenses'),
    path('expenseslist/',ExpenseListView.as_view(),name='expenseslist'),
    path('budgets/<int:budgetId>/', BudgetDeleteView.as_view(), name='budget-delete'),
    path('expenses/<int:expenseId>/', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
