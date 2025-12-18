from .models import PricingRule

class PricingEngine:
    def calculate(self, base_price, quantity, user_tier=None):
        price = base_price * quantity
        breakdown = []

        rules = PricingRule.objects.filter(is_active=True).order_by("priority")

        for rule in rules:
            if rule.rule_type == "BULK":
                if quantity >= rule.config["min_qty"]:
                    discount = price * rule.config["discount_percent"] / 100
                    price -= discount
                    breakdown.append({
                        "type": "BULK",
                        "discount": float(discount)
                    })

            if rule.rule_type == "USER_TIER" and user_tier:
                if user_tier == rule.config["tier"]:
                    discount = price * rule.config["discount_percent"] / 100
                    price -= discount
                    breakdown.append({
                        "type": "USER_TIER",
                        "discount": float(discount)
                    })

            if rule.rule_type == "SEASONAL":
                if self._is_seasonal_active(rule):
                    discount = price * rule.config["discount_percent"] / 100
                    price -= discount
                    breakdown.append({
                        "type": "SEASONAL",
                        "discount": float(discount)
                    })

        return round(price, 2), breakdown

    def _is_seasonal_active(self, rule):
        from django.utils import timezone
        from datetime import datetime
        
        if not rule.config.get("start_date") or not rule.config.get("end_date"):
            return False
            
        now = timezone.now()
        start = datetime.fromisoformat(rule.config["start_date"])
        end = datetime.fromisoformat(rule.config["end_date"])
        
        # Ensure primitive comparison works by making naive datetimes aware if needed
        if timezone.is_aware(now) and timezone.is_naive(start):
            start = timezone.make_aware(start)
        if timezone.is_aware(now) and timezone.is_naive(end):
            end = timezone.make_aware(end)
            
        return start <= now <= end
