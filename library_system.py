"""
LibraryHub Lending System  --  Practice Round 2 (Medium)
========================================================

WRITE-UP (this is the spec; the code is supposed to follow it)
--------------------------------------------------------------
LibraryHub tracks books, members, loans, fines and holds.
Dates are plain integers ("day numbers"). Money is integer cents.

Tiers (every member has exactly one tier)
  Tier       loan limit   loan period   fine per overdue day
  STANDARD        3         14 days           25 cents
  PREMIUM         5         21 days           10 cents

Setup
  1. add_book(isbn, title, copies)
       - copies must be > 0, otherwise ValueError.
       - Adding an existing isbn increases both its total and available copies.
  2. register_member(member_id, tier)
       - Unknown tier -> ValueError. Duplicate member_id -> ValueError.

Checkout
  3. checkout(member_id, isbn, today) returns the due date.
     Checks are applied in this order, the first failure wins:
       a. Unknown member -> UnknownMemberError; unknown book -> UnknownBookError.
       b. Member's fine balance >= 500 -> BlockedMemberError.
       c. Member already has loans equal to their tier limit -> LimitError.
       d. Member already has this isbn on loan -> ValueError.
       e. No copies available -> NoCopiesError.
       f. Copies are reserved for the hold queue, in order. Count the people
          ahead of the member in the queue (if the member is not in the
          queue, that is everybody in it). If that count is >= the number of
          available copies -> HoldPendingError.
     On success: if the member had a hold on this book, the hold is removed;
     available copies drop by 1; due date = today + loan period of the tier.

Returns and fines
  4. return_book(member_id, isbn, today) returns the fine charged.
       - No such loan -> ValueError.
       - A loan is overdue when today > due. Days overdue = today - due
         (never negative). Fine = days overdue * tier rate, capped at
         2000 cents per loan.
       - The fine is added to the member's balance, the loan is closed and
         the copy becomes available again.
  5. pay_fine(member_id, amount) returns the remaining balance.
       - amount must be > 0 and no more than the balance, otherwise ValueError.

Renewals
  6. renew(member_id, isbn, today) returns the new due date.
     Checks are applied in this order:
       a. No such loan -> ValueError.
       b. Loan is overdue (today > due) -> OverdueError.
       c. Anyone is waiting in the hold queue for the book -> HoldPendingError.
       d. The loan has already been renewed 2 times -> RenewalLimitError.
     On success: new due date = OLD due date + loan period of the tier, and
     the loan's renewal count goes up by 1.

Holds
  7. place_hold(member_id, isbn) returns the member's 1-based queue position.
       - Only allowed when the member could not check the book out right now
         (copies available <= number of people already in the queue);
         otherwise ValueError.
       - Member already in the queue, or already has the book on loan
         -> ValueError.

Reports
  8. overdue_report(today): list of (member_id, isbn, days_overdue) for every
     overdue loan, most days overdue first; ties broken by member_id, then
     isbn, both ascending.
  9. outstanding_fines(): total of all member balances.
 10. books_on_loan(member_id): sorted list of the isbns the member has out.
"""

from dataclasses import dataclass, field


class UnknownMemberError(Exception):
    pass


class UnknownBookError(Exception):
    pass


class BlockedMemberError(Exception):
    pass


class LimitError(Exception):
    pass


class NoCopiesError(Exception):
    pass


class HoldPendingError(Exception):
    pass


class OverdueError(Exception):
    pass


class RenewalLimitError(Exception):
    pass


TIERS = {
    "STANDARD": {"limit": 3, "loan_days": 14, "fine_per_day": 25},
    "PREMIUM": {"limit": 5, "loan_days": 21, "fine_per_day": 10},
}
BLOCK_THRESHOLD = 500
FINE_CAP = 2000
MAX_RENEWALS = 2


# ---------------------------------------------------------------------------
# Data records
# ---------------------------------------------------------------------------
@dataclass
class Book:
    isbn: str
    title: str
    total: int
    available: int


@dataclass
class Loan:
    isbn: str
    due: int
    renewals: int = 0


@dataclass
class Member:
    member_id: str
    tier: str
    balance: int = 0
    loans: dict = field(default_factory=dict)  # isbn -> Loan


# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------
class Library:
    def __init__(self):
        self._books = {}    # isbn -> Book
        self._members = {}  # member_id -> Member
        self._holds = {}    # isbn -> [member_id, ...] in queue order

    # -- lookups ------------------------------------------------------------
    def _member(self, member_id):
        if member_id not in self._members:
            raise UnknownMemberError(member_id)
        return self._members[member_id]

    def _book(self, isbn):
        if isbn not in self._books:
            raise UnknownBookError(isbn)
        return self._books[isbn]

    def get_available(self, isbn):
        return self._book(isbn).available

    def get_balance(self, member_id):
        return self._member(member_id).balance

    def get_due_date(self, member_id, isbn):
        return self._member(member_id).loans[isbn].due

    def hold_queue(self, isbn):
        self._book(isbn)
        return list(self._holds[isbn])

    def books_on_loan(self, member_id):
        return sorted(self._member(member_id).loans.keys())

    # -- setup --------------------------------------------------------------
    def add_book(self, isbn, title, copies):
        if copies <= 0:
            raise ValueError("copies must be positive")
        if isbn in self._books:
            book = self._books[isbn]
            book.total += copies
            book.available += copies
        else:
            self._books[isbn] = Book(isbn, title, copies, copies)
            self._holds[isbn] = []

    def register_member(self, member_id, tier):
        if tier not in TIERS:
            raise ValueError(f"unknown tier {tier}")
        if member_id in self._members:
            raise ValueError(f"duplicate member {member_id}")
        self._members[member_id] = Member(member_id, tier)

    # -- checkout / return --------------------------------------------------
    def checkout(self, member_id, isbn, today):
        member = self._member(member_id)
        book = self._book(isbn)
        rules = TIERS[member.tier]

        if member.balance > BLOCK_THRESHOLD:
            raise BlockedMemberError(member_id)
        if len(member.loans) > rules["limit"]:
            raise LimitError(member_id)
        if isbn in member.loans:
            raise ValueError("member already has this book")
        if book.available <= 0:
            raise NoCopiesError(isbn)

        queue = self._holds[isbn]
        ahead = queue.index(member_id) if member_id in queue else len(queue)
        if ahead >= book.available:
            raise HoldPendingError(isbn)

        if queue:
            queue.pop(0)

        book.available -= 1
        due = today + rules["loan_days"]
        member.loans[isbn] = Loan(isbn, due)
        return due

    def _compute_fine(self, member, loan, today):
        overdue = today - loan.due
        rate = TIERS[member.tier]["fine_per_day"]
        return min(overdue, FINE_CAP) * rate

    def return_book(self, member_id, isbn, today):
        member = self._member(member_id)
        loan = member.loans.get(isbn)
        if loan is None:
            raise ValueError("no such loan")

        fine = self._compute_fine(member, loan, today)
        member.balance += fine
        del member.loans[isbn]
        self._books[isbn].available += 1
        return fine

    def pay_fine(self, member_id, amount):
        member = self._member(member_id)
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > member.balance:
            raise ValueError("amount exceeds balance")
        member.balance -= amount
        return member.balance

    # -- renewals -----------------------------------------------------------
    def renew(self, member_id, isbn, today):
        member = self._member(member_id)
        loan = member.loans.get(isbn)
        if loan is None:
            raise ValueError("no such loan")
        if today > loan.due:
            raise OverdueError(isbn)
        if loan.renewals >= MAX_RENEWALS:
            raise RenewalLimitError(isbn)

        loan.due = today + TIERS[member.tier]["loan_days"]
        loan.renewals += 1
        return loan.due

    # -- holds --------------------------------------------------------------
    def place_hold(self, member_id, isbn):
        member = self._member(member_id)
        book = self._book(isbn)
        queue = self._holds[isbn]

        if book.available > len(queue):
            raise ValueError("a copy is available, check it out instead")
        if member_id in queue:
            raise ValueError("already in the queue")
        if isbn in member.loans:
            raise ValueError("member already has this book")

        queue.append(member_id)
        return len(queue)

    # -- reports ------------------------------------------------------------
    def overdue_report(self, today):
        rows = []
        for member in self._members.values():
            for loan in member.loans.values():
                if today > loan.due:
                    rows.append((member.member_id, loan.isbn, today - loan.due))
        rows.sort(key=lambda r: (r[2], r[0], r[1]), reverse=True)
        return rows

    def outstanding_fines(self):
        return sum(m.balance for m in self._members.values())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def main():
    def make_library():
        lib = Library()
        lib.add_book("111", "Dune", 2)
        lib.add_book("222", "Emma", 1)
        lib.add_book("333", "Ulysses", 1)
        lib.add_book("444", "Hamlet", 5)
        lib.register_member("alice", "STANDARD")
        lib.register_member("bob", "PREMIUM")
        lib.register_member("cara", "STANDARD")
        lib.register_member("dan", "STANDARD")
        return lib

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

    # ---- setup tests ----
    def test_add_book_merges_copies():
        lib = make_library()
        lib.add_book("111", "Dune", 3)
        expect_equal(lib.get_available("111"), 5)

    def test_register_duplicate_member():
        lib = make_library()
        expect_raises(ValueError, lib.register_member, "alice", "PREMIUM")

    def test_register_unknown_tier():
        lib = make_library()
        expect_raises(ValueError, lib.register_member, "eve", "GOLD")

    # ---- checkout tests ----
    def test_checkout_standard_due_date():
        lib = make_library()
        due = lib.checkout("alice", "111", 10)
        expect_equal(due, 24)
        expect_equal(lib.get_available("111"), 1)

    def test_checkout_premium_due_date():
        lib = make_library()
        due = lib.checkout("bob", "111", 10)
        # 10 + 14 = 24
        expect_equal(due, 24)

    def test_checkout_unknown_member_and_book():
        lib = make_library()
        expect_raises(UnknownMemberError, lib.checkout, "zed", "111", 0)
        expect_raises(UnknownBookError, lib.checkout, "alice", "999", 0)

    def test_checkout_same_book_twice():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        expect_raises(ValueError, lib.checkout, "alice", "111", 1)

    def test_checkout_no_copies_left():
        lib = make_library()
        lib.checkout("alice", "222", 0)
        expect_raises(NoCopiesError, lib.checkout, "cara", "222", 1)

    def test_standard_loan_limit():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.checkout("alice", "222", 0)
        lib.checkout("alice", "333", 0)
        expect_raises(LimitError, lib.checkout, "alice", "444", 0)

    def test_member_with_500_in_fines_is_blocked():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.return_book("alice", "111", 34)      # 20 days late * 25 = 500
        expect_equal(lib.get_balance("alice"), 500)
        expect_raises(BlockedMemberError, lib.checkout, "alice", "444", 40)

    # ---- return / fine tests ----
    def test_late_return_fine():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        fine = lib.return_book("alice", "111", 17)   # due 14, 3 days late
        expect_equal(fine, 75)
        expect_equal(lib.get_balance("alice"), 75)

    def test_early_return_has_no_fine():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        fine = lib.return_book("alice", "111", 5)
        expect_equal(fine, 0)
        expect_equal(lib.get_balance("alice"), 0)

    def test_fine_is_capped():
        lib = make_library()
        lib.checkout("bob", "111", 0)                # due 21
        fine = lib.return_book("bob", "111", 321)    # 300 days late
        expect_equal(fine, 2000)

    def test_return_restores_copy():
        lib = make_library()
        lib.checkout("alice", "222", 0)
        expect_equal(lib.get_available("222"), 0)
        lib.return_book("alice", "222", 3)
        expect_equal(lib.get_available("222"), 1)

    def test_return_without_loan():
        lib = make_library()
        expect_raises(ValueError, lib.return_book, "alice", "111", 3)

    def test_pay_fine_partial():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.return_book("alice", "111", 17)          # balance 75
        expect_equal(lib.pay_fine("alice", 50), 25)

    # ---- renewal tests ----
    def test_renew_extends_due_date():
        lib = make_library()
        lib.checkout("alice", "111", 0)              # due 14
        new_due = lib.renew("alice", "111", 5)
        # renewed on day 5 -> 5 + 14 = 19
        expect_equal(new_due, 19)

    def test_renew_overdue_loan_rejected():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        expect_raises(OverdueError, lib.renew, "alice", "111", 15)

    def test_renew_blocked_by_waiting_hold():
        lib = make_library()
        lib.checkout("alice", "222", 0)
        lib.place_hold("cara", "222")
        expect_raises(HoldPendingError, lib.renew, "alice", "222", 3)

    def test_renewal_limit():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.renew("alice", "111", 1)
        lib.renew("alice", "111", 2)
        expect_raises(RenewalLimitError, lib.renew, "alice", "111", 3)

    # ---- hold tests ----
    def test_hold_rejected_when_copy_available():
        lib = make_library()
        expect_raises(ValueError, lib.place_hold, "alice", "444")

    def test_hold_queue_positions():
        lib = make_library()
        lib.checkout("alice", "222", 0)
        expect_equal(lib.place_hold("cara", "222"), 1)
        expect_equal(lib.place_hold("dan", "222"), 2)

    def test_hold_reserves_copy_for_queue_head():
        lib = make_library()
        lib.checkout("alice", "222", 0)
        lib.place_hold("cara", "222")
        lib.place_hold("dan", "222")
        lib.return_book("alice", "222", 5)
        expect_raises(HoldPendingError, lib.checkout, "dan", "222", 6)
        lib.checkout("cara", "222", 6)
        expect_equal(lib.hold_queue("222"), ["dan"])

    def test_walk_up_member_does_not_steal_a_hold():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.checkout("bob", "111", 0)
        lib.place_hold("cara", "111")
        lib.return_book("alice", "111", 1)
        lib.return_book("bob", "111", 2)             # 2 copies free, 1 hold
        lib.checkout("dan", "111", 3)
        expect_equal(lib.hold_queue("111"), ["cara"])

    # ---- report tests ----
    def test_overdue_report_order():
        lib = make_library()
        lib.checkout("alice", "111", 0)              # due 14
        lib.checkout("bob", "222", 0)                # due 21
        lib.checkout("cara", "333", 0)               # due 14
        expect_equal(
            lib.overdue_report(30),
            [("alice", "111", 16), ("cara", "333", 16), ("bob", "222", 9)],
        )

    def test_outstanding_fines_total():
        lib = make_library()
        lib.checkout("alice", "111", 0)
        lib.return_book("alice", "111", 17)          # 75
        lib.checkout("cara", "333", 0)
        lib.return_book("cara", "333", 15)           # 25
        expect_equal(lib.outstanding_fines(), 100)

    tests = [
        test_add_book_merges_copies,
        test_register_duplicate_member,
        test_register_unknown_tier,
        test_checkout_standard_due_date,
        test_checkout_premium_due_date,
        test_checkout_unknown_member_and_book,
        test_checkout_same_book_twice,
        test_checkout_no_copies_left,
        test_standard_loan_limit,
        test_member_with_500_in_fines_is_blocked,
        test_late_return_fine,
        test_early_return_has_no_fine,
        test_fine_is_capped,
        test_return_restores_copy,
        test_return_without_loan,
        test_pay_fine_partial,
        test_renew_extends_due_date,
        test_renew_overdue_loan_rejected,
        test_renew_blocked_by_waiting_hold,
        test_renewal_limit,
        test_hold_rejected_when_copy_available,
        test_hold_queue_positions,
        test_hold_reserves_copy_for_queue_head,
        test_walk_up_member_does_not_steal_a_hold,
        test_overdue_report_order,
        test_outstanding_fines_total,
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