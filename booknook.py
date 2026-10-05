"""
BookNook Order System  --  Practice Round 1 (Easy)
==================================================

WRITE-UP (this is the spec; the code is supposed to follow it)
--------------------------------------------------------------
BookNook is a tiny shop backend. All money is stored as integer cents.

Inventory
  1. add_stock(sku, qty, price_cents=None)
       - qty must be > 0, otherwise ValueError.
       - A brand-new SKU requires a price, otherwise ValueError.
       - An existing SKU gets its quantity increased; if a price is given,
         the price is updated too.
  2. remove_stock(sku, qty)
       - Unknown SKU -> UnknownSkuError.
       - Asking for more than is available -> OutOfStockError.
       - Removing exactly the amount available is allowed (stock becomes 0).
  3. low_stock(threshold)
       - Returns SKUs whose quantity is strictly below threshold,
         sorted alphabetically.

Pricing pipeline (applied in this order)
  subtotal -> bulk discount -> coupon -> tax -> total
  4. Bulk discount: if subtotal >= 10000 cents, take 10% off.
       discount = subtotal * 10 // 100   (integer division)
  5. Coupons: "SAVE5" takes 500 cents off, but the amount never goes
     below 0. Any other non-None coupon -> InvalidCouponError.
  6. Tax: 8% of the post-coupon amount, rounded down to a whole cent.
     total = post-coupon amount + tax.

Orders
  7. place_order(items, coupon=None)
       - items is a non-empty list of (sku, qty); every qty must be > 0,
         otherwise ValueError.
       - The same SKU may appear on several lines; the quantities add up.
       - All-or-nothing: if any part of the order cannot be fulfilled,
         an exception is raised and inventory is left unchanged.
       - Returns the new order id (1, 2, 3, ...).
  8. refund_order(order_id)
       - Unknown id -> KeyError. Already refunded -> ValueError.
       - Puts the items back in stock, marks the order refunded,
         and returns the order total.

Reports
  9. total_revenue(): sum of totals of orders that are NOT refunded.
 10. top_sellers(n): units sold per SKU across non-refunded orders,
     highest first, ties broken alphabetically by SKU, first n entries.
 11. format_cents(cents): 12345 -> "$123.45", 5 -> "$0.05".
"""


class OutOfStockError(Exception):
    pass


class UnknownSkuError(Exception):
    pass


class InvalidCouponError(Exception):
    pass


def format_cents(cents):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------
class Inventory:
    def __init__(self):
        self._items = {}  # sku -> {"qty": int, "price": int}

    def _get(self, sku) -> dict[str, int]:
        if sku not in self._items:
            raise UnknownSkuError(sku)
        return self._items[sku]

    def add_stock(self, sku, qty, price_cents=None):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if sku in self._items:
            self._items[sku]["qty"] += qty
            if price_cents is not None:
                self._items[sku]["price"] = price_cents
        else:
            if price_cents is None:
                raise ValueError("price required for new sku")
            self._items[sku] = {"qty": qty, "price": price_cents}

    def remove_stock(self, sku, qty):
        item: dict[str, int] = self._get(sku)
        if qty > item["qty"]:
            raise OutOfStockError(f"{sku}: wanted {qty}, have {item['qty']}")
        item["qty"] -= qty

    def get_quantity(self, sku):
        return self._get(sku)["qty"]

    def get_price(self, sku):
        return self._get(sku)["price"]

    def low_stock(self, threshold):
        result = []
        for sku, item in self._items.items():
            if item["qty"] < threshold:
                result.append(sku)
        return sorted(result)


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------
class OrderService:
    DISCOUNT_THRESHOLD = 10000
    DISCOUNT_PERCENT = 10
    TAX_PERCENT = 8
    SAVE5_AMOUNT = 500

    def __init__(self, inventory):
        self.inventory: Inventory = inventory
        self._orders = {}
        self._next_id = 1

    # -- pricing helpers ----------------------------------------------------
    def calculate_subtotal(self, order: dict[str, int]):
        subtotal = 0
        for sku, qty in order.items():
            subtotal += self.inventory.get_price(sku) * qty
        return subtotal

    def apply_discount(self, subtotal):
        if subtotal >= self.DISCOUNT_THRESHOLD:
            discount = subtotal * self.DISCOUNT_PERCENT // 100
            return subtotal - discount
        return subtotal

    def apply_coupon(self, amount, coupon = None):
        if coupon is None:
            return amount
        if coupon == "SAVE5":
            after_coup =  amount - self.SAVE5_AMOUNT

            if after_coup < 0:
                return 0
            else:
                return after_coup

        raise InvalidCouponError(coupon)

    def calculate_tax(self, amount):
        return amount * self.TAX_PERCENT // 100

    # -- order lifecycle ----------------------------------------------------
    def place_order(self, items, coupon=None):
        order: dict[str, int] = {}
        if not items:
            raise ValueError("order must have at least one item")
        for sku, qty in items:
            if qty <= 0:
                raise ValueError("qty must be positive")

            if sku not in order:
                order[sku] = qty

            else:
                order[sku] += qty

        for sku, qty in order.items():
            if qty > self.inventory.get_quantity(sku):
                raise OutOfStockError()

        subtotal = self.calculate_subtotal(order)
        after_discount = self.apply_discount(subtotal)
        after_coupon = self.apply_coupon(after_discount, coupon)
        total = after_coupon + self.calculate_tax(after_coupon)

        for sku, qty in order.items():
            self.inventory.remove_stock(sku, qty)

        order_id = self._next_id
        self._next_id += 1
        self._orders[order_id] = {
            "id": order_id,
            "items": list(items),
            "subtotal": subtotal,
            "total": total,
            "status": "placed",
        }
        return order_id

    def get_order(self, order_id):
        return self._orders[order_id]

    def refund_order(self, order_id):
        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(order_id)
        if order["status"] == "refunded":
            raise ValueError("order already refunded")
        for sku, qty in order["items"]:
            self.inventory.add_stock(sku, qty)
        order["status"] = "refunded"
        return order["total"]

    # -- reports ------------------------------------------------------------
    def total_revenue(self):
        revenue = 0
        for order in self._orders.values():
            if order["status"] != "refunded":
                revenue += order["total"]
        return revenue

    def top_sellers(self, n):
        units = {}
        for order in self._orders.values():
            if order["status"] == "refunded":
                continue
            for sku, qty in order["items"]:
                units[sku] = units.get(sku, 0) + qty
        ranked = sorted(units.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:n]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def main():
    def make_shop():
        inv = Inventory()
        inv.add_stock("BK-101", 10, 2500)
        inv.add_stock("BK-202", 5, 1200)
        inv.add_stock("BK-303", 2, 9900)
        inv.add_stock("PN-001", 50, 150)
        return inv, OrderService(inv)

    def expect_equal(got, want):
        if got != want:
            raise AssertionError(f"expected {want!r}, got {got!r}")

    def expect_raises(exc_type, fn, *args, **kwargs):
        try:
            fn(*args, **kwargs)
        except exc_type:
            return
        except Exception as e:
            raise AssertionError(
                f"expected {exc_type.__name__}, got {type(e).__name__}: {e}"
            )
        raise AssertionError(f"expected {exc_type.__name__}, nothing was raised")

    # ---- inventory tests ----
    def test_add_stock_new_and_existing():
        inv, _ = make_shop()
        inv.add_stock("BK-101", 5, 2600)
        expect_equal(inv.get_quantity("BK-101"), 15)
        expect_equal(inv.get_price("BK-101"), 2600)


    def test_add_stock_no_price():

        inv, _ = make_shop()
        try:
            inv.add_stock("EM-001", 7)
        except ValueError as e:
            expect_equal(str(e), "price required for new sku")
        else:
            raise AssertionError("expected ValueError, Nothing was raised")

        
        

    def test_add_stock_rejects_zero_qty():
        inv, _ = make_shop()
        expect_raises(ValueError, inv.add_stock, "BK-101", 0)

    def test_remove_stock_basic():
        inv, _ = make_shop()
        inv.remove_stock("BK-101", 3)
        expect_equal(inv.get_quantity("BK-101"), 7)

    def test_remove_all_stock():
        inv, _ = make_shop()
        inv.remove_stock("BK-303", 2)
        expect_equal(inv.get_quantity("BK-303"), 0)

    def test_remove_too_much():
        inv, _ = make_shop()
        expect_raises(OutOfStockError, inv.remove_stock, "BK-303", 3)

    def test_low_stock_report():
        inv, _ = make_shop()
        expect_equal(inv.low_stock(5), ["BK-303"])

    # ---- pricing tests ----
    def test_order_with_bulk_discount():
        _, svc = make_shop()
        oid = svc.place_order([("BK-101", 4)])
        # 10000 -> 9000 after discount -> +720 tax
        expect_equal(svc.get_order(oid)["total"], 9720)
    
    def test_empty_order_fails():

        _, svc = make_shop()
        try:
            svc.place_order([])

        except ValueError as e:
             expect_equal(str(e), "order must have at least one item")

        else:
            raise AssertionError("expected ValueError, Nothing was raised")
    

    def test_order_with_coupon():
        _, svc = make_shop()
        oid = svc.place_order([("BK-202", 2)], coupon="SAVE5")
        # 2400 - 500 = 1900, tax 152
        expect_equal(svc.get_order(oid)["total"], 2052)

    def test_coupon_never_goes_negative():
        _, svc = make_shop()
        oid = svc.place_order([("PN-001", 2)], coupon="SAVE5")
        expect_equal(svc.get_order(oid)["total"], 0)

    def test_invalid_coupon():
        _, svc = make_shop()
        expect_raises(InvalidCouponError, svc.place_order, [("BK-101", 1)], "FREEBIE")

    def test_unknown_sku_in_order():
        _, svc = make_shop()
        expect_raises(UnknownSkuError, svc.place_order, [("NOPE-1", 1)])

    # ---- order lifecycle tests ----
    def test_order_is_all_or_nothing():
        inv, svc = make_shop()
        expect_raises(OutOfStockError, svc.place_order, [("PN-001", 5), ("BK-303", 3)])
        expect_equal(inv.get_quantity("PN-001"), 50)

    def test_refund_restores_stock():
        inv, svc = make_shop()
        oid = svc.place_order([("BK-101", 2)])
        expect_equal(inv.get_quantity("BK-101"), 8)
        expect_equal(svc.refund_order(oid), 5400)
        expect_equal(inv.get_quantity("BK-101"), 10)

    def test_refund_twice_fails():
        _, svc = make_shop()
        oid = svc.place_order([("BK-101", 1)])
        svc.refund_order(oid)
        expect_raises(ValueError, svc.refund_order, oid)

    def test_duplicate_sku_lines_are_summed():
        inv, svc = make_shop()                                 
        svc.place_order([("BK-101", 3), ("BK-101", 4)])        
        expect_equal(inv.get_quantity("BK-101"), 3) 



    def test_duplicate_sku_lines_exceeding_stock_fail_cleanly():
        inv, svc = make_shop()                                   
        expect_raises(OutOfStockError, svc.place_order, [("BK-101", 6), ("BK-101", 6)])
        expect_equal(inv.get_quantity("BK-101"), 10)

    def test_duplicate_sku_failure_leaves_other_skus_untouched():
        inv, svc = make_shop()
        expect_raises(OutOfStockError, svc.place_order, [("PN-001", 5), ("BK-101", 6), ("BK-101", 6)])
        expect_equal(inv.get_quantity("PN-001"), 50)


    # ---- report tests ----
    def test_revenue_excludes_refunded():
        _, svc = make_shop()
        a = svc.place_order([("BK-101", 2)])      # total 5400
        svc.place_order([("PN-001", 10)])         # total 1620
        svc.refund_order(a)
        expect_equal(svc.total_revenue(), 1620)

    def test_top_sellers():
        _, svc = make_shop()
        svc.place_order([("PN-001", 10)])
        svc.place_order([("BK-202", 1)])
        svc.place_order([("BK-101", 1)])
        expect_equal(svc.top_sellers(2), [("PN-001", 10), ("BK-101", 1)])

    def test_format_cents():
        expect_equal(format_cents(5), "$0.05")
        expect_equal(format_cents(12345), "$123.45")


   
    tests = [
        test_add_stock_new_and_existing,
        test_add_stock_rejects_zero_qty,
        test_remove_stock_basic,
        test_remove_all_stock,
        test_remove_too_much,
        test_low_stock_report,
        test_order_with_bulk_discount,
        test_order_with_coupon,
        test_coupon_never_goes_negative,
        test_invalid_coupon,
        test_unknown_sku_in_order,
        test_order_is_all_or_nothing,
        test_refund_restores_stock,
        test_refund_twice_fails,
        test_revenue_excludes_refunded,
        test_top_sellers,
        test_format_cents,
        test_empty_order_fails,
        test_add_stock_no_price,
        test_duplicate_sku_lines_are_summed,
        test_duplicate_sku_lines_exceeding_stock_fail_cleanly,
        test_duplicate_sku_failure_leaves_other_skus_untouched

    ]

    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")


if __name__ == "__main__":
    main()