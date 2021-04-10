from django.contrib import admin

from reversion.admin import VersionAdmin

from core.models import BenefitsType, InformationDocuments, RequiredDocuments, Benefit, Requirement, RequirementsValue, BenefitRequrements, BenefitsGroup, Periodicity


@admin.register(BenefitsType)
class BenefitsTypeAdmin(VersionAdmin):
    list_display = ['id', 'title']

@admin.register(InformationDocuments)
class InformationDocumentsAdmin(VersionAdmin):
    list_display = ['id', 'title', 'link']

@admin.register(RequiredDocuments)
class RequiredDocumentsAdmin(VersionAdmin):
    list_display = ['id', 'title', 'description']


@admin.register(Benefit)
class BenefitAdmin(VersionAdmin):
    list_display = ['id', 'title', 'value']


@admin.register(Requirement)
class RequirementAdmin(VersionAdmin):
    list_display = ['id', 'title']


@admin.register(RequirementsValue)
class RequirementsValueAdmin(VersionAdmin):
    list_display = ['id', 'requirement', "value"]


@admin.register(BenefitRequrements)
class BenefitRequrementsAdmin(VersionAdmin):
    list_display = ['id', 'requirement_value', "benefit", "sign"]

@admin.register(Periodicity)
class PeriodicityAdmin(VersionAdmin):
    list_display = ['id', "title"]


@admin.register(BenefitsGroup)
class BenefitsGroupAdmin(VersionAdmin):
    list_display = ['id', "title"]
