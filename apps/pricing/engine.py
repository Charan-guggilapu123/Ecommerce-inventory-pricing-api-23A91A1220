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

        return round(price, 2), breakdown
