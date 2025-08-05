from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    lifetime = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SafetyFunction(models.Model):
    project = models.ForeignKey(Project, related_name='safety_functions', on_delete=models.CASCADE)
    sf_id = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_integrity_level = models.CharField(max_length=20, blank=True)
    # Calculated metrics
    RF = models.FloatField(default=0)
    MPFL = models.FloatField(default=0)
    MPFD = models.FloatField(default=0)
    MPHF = models.FloatField(default=0)
    SPFM = models.FloatField(default=0)
    LFM = models.FloatField(default=0)
    safetyrelated = models.FloatField(default=0)

    class Meta:
        unique_together = ('project', 'sf_id')

class Component(models.Model):
    project = models.ForeignKey(Project, related_name='components', on_delete=models.CASCADE)
    comp_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True)
    failure_rate = models.FloatField(default=0)
    is_safety_related = models.BooleanField(default=False)
    related_sfs = models.ManyToManyField(SafetyFunction, related_name='related_components', blank=True)

    class Meta:
        unique_together = ('project', 'comp_id')

class FailureMode(models.Model):
    component = models.ForeignKey(Component, related_name='failure_modes', on_delete=models.CASCADE)
    description = models.TextField()
    Failure_rate_total = models.FloatField(default=0)
    system_level_effect = models.TextField(blank=True)
    is_SPF = models.BooleanField(default=False)
    is_MPF = models.BooleanField(default=False)
    SPF_safety_mechanism = models.CharField(max_length=255, blank=True)
    MPF_safety_mechanism = models.CharField(max_length=255, blank=True)
    SPF_diagnostic_coverage = models.FloatField(default=0)
    MPF_diagnostic_coverage = models.FloatField(default=0)
    RF = models.FloatField(default=0)
    MPFL = models.FloatField(default=0)
    MPFD = models.FloatField(default=0)
    # Optionally, add timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 