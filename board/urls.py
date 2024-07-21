from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('', views.main, name='main'),
    path('<int:typeid>/excel_export', views.excel_export, name='excel_export'),
    path('<int:typeid>/excel_import', views.excel_import, name='excel_import'),

    path('code_index/', views.code_index, name='code_index'),
    path('code_add/', views.code_add, name='code_add'),
    path('code_add/code_add_exec', views.code_add_exec, name='code_add_exec'),
    path('code_index/<int:codeid>', views.code_detail, name='code_detail'),
    path('code_index/<int:codeid>/edit_code', views.edit_code, name='edit_code'),
    path('code_index/<int:codeid>/delete_code', views.delete_code, name='delete_code'),
    
    path('cluster_index/', views.cluster_index, name='cluster_index'),
    path('cluster_add/', views.cluster_add, name='cluster_add'),
    path('cluster_add/cluster_add_exec', views.cluster_add_exec, name='cluster_add_exec'),
    path('cluster_index/<int:clusterid>', views.cluster_detail, name='cluster_detail'),
    path('cluster_index/<int:clusterid>/edit_cluster', views.edit_cluster, name='edit_cluster'),
    path('cluster_index/<int:clusterid>/delete_cluster', views.delete_cluster, name='delete_cluster'),

    path('host_index/', views.host_index, name='host_index'),
    path('host_add/', views.host_add, name='host_add'),
    path('host_add/host_add_exec', views.host_add_exec, name='host_add_exec'),
    path('host_index/<int:hostid>', views.host_detail, name='host_detail'),
    path('host_index/<int:hostid>/host_edit', views.host_edit, name='host_edit'),
    path('host_index/<int:hostid>/delete_host', views.delete_host, name='delete_host'),

    path('storage_index/', views.storage_index, name='storage_index'),
    path('storage_add/', views.storage_add, name='storage_add'),
    path('storage_add/storage_add_exec', views.storage_add_exec, name='storage_add_exec'),
    path('storage_index/<int:storageid>', views.storage_detail, name='storage_detail'),
    path('storage_index/<int:storageid>/storage_edit', views.storage_edit, name='storage_edit'),
    path('storage_index/<int:storageid>/delete_storage', views.delete_storage, name='delete_storage'),

]


