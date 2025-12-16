from django.db import models

class PricingRule(models.Model):
    RULE_TYPES = (
        ("SEASONAL", "Seasonal"),
        ("BULK", "Bulk"),
        ("USER_TIER", "User Tier"),
    )

    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    priority = models.IntegerField()
    config = models.JSONField()
    is_active = models.BooleanField(default=True)
