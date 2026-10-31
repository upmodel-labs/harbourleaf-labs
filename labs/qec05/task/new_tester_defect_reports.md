# The new tester's two defect reports (practice data)

Sent on Monday morning, after an hour of exploring the test bookshop.

---

## DR-NT-1: Total goes up when a voucher is added to a bundle

- **Reporter:** the new tester
- **Seen:** Monday 09:50
- **Build:** not stated
- **Steps to reproduce:**
  1. Open the bookshop on the QA environment.
  2. Add every book of one bundle to the basket. The basket shows a saving line.
  3. Enter the voucher code TESTVOUCHER.
  4. Look at the total.
- **Expected result:** the voucher is taken off once and the bundle saving stays.
- **Actual result:** the bundle saving line disappears and the total is higher than before the voucher.
- **Evidence:** screenshot `basket-voucher.png`
- **Severity:** High (I think)
- **How often:** not tried again

---

## DR-NT-2: Cart message is wrong

- **Reporter:** the new tester
- **Seen:** Monday 10:20
- **Build:** the QA build from Monday morning
- **Description:** The message under the basket said I saved more than I did. It looks wrong.
- **Steps to reproduce:** (none given)
- **Expected result:** the message should be right.
- **Actual result:** the message is wrong.
- **Evidence:** screenshot `cart-message.png`
- **Severity:** Medium
- **How often:** it happened once
