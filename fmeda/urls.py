from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, SafetyFunctionViewSet, ComponentViewSet, FailureModeViewSet,
    FMEDACalculateView, ProjectResultsView, ProjectImportCSVView, ProjectExportCSVView,
    ProjectDebugView, ProjectClearAllView
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'safety-functions', SafetyFunctionViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'failure-modes', FailureModeViewSet)

urlpatterns = [
    # Custom URLs (must come before router URLs to avoid conflicts)
    path('projects/import-csv/', ProjectImportCSVView.as_view(), name='project-import-csv'),
    path('projects/clear-all/', ProjectClearAllView.as_view(), name='project-clear-all'),
    path('projects/<int:project_id>/export-csv/', ProjectExportCSVView.as_view(), name='project-export-csv'),
    path('projects/<int:project_id>/debug/', ProjectDebugView.as_view(), name='project-debug'),
    path('fmeda/calculate/', FMEDACalculateView.as_view(), name='fmeda-calculate'),
    path('fmeda/results/<int:project_id>/', ProjectResultsView.as_view(), name='project-results'),
    # Router URLs (must come after custom URLs)
    path('', include(router.urls)),
] 