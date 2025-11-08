from django.urls import path
from loanApp import views


app_name = 'loanApp'
urlpatterns = [
    path('loan-request/', views.LoanRequest, name='loan_request'),
    path('application/<int:loan_id>/', views.application_details_view, name='application_details'),
    path('loan-payment/', views.LoanPayment, name='loan_payment'),
    path('user-transaction/', views.UserTransaction, name='user_transaction'),
    path('user-loan-history/', views.UserLoanHistory, name='user_loan_history'),
    path('user-dashboard/', views.UserDashboard, name='user_dashboard'),
    path('terms/', views.terms_conditions, name='terms_conditions'),

]
