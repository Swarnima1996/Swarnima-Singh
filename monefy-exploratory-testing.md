# Monefy App — Exploratory Testing Session

**Tester:** Swarnima Singh 
**Platform:** iOS  
**App Version:** Latest (as of Feb 2026)  
**Date:** 26 February 2026  
**Testing Duration:** ~2 hours  

---

## Table of Contents
1. [Testing Charters](#testing-charters)
2. [Findings & Bug Report](#findings--bug-report)
3. [Charter Prioritisation](#charter-prioritisation)
4. [Risk Assessment](#risk-assessment)

---

## Testing Charters

> This charter defines the **focus**, **goal**, and **approach** of exploratory testing session of Monefy iOS Mobile App.
> Format: *"Explore [area] to discover [goal] by [approach]"*

---

### Charter 1: Core Expense Entry & Calculator Input
**Area:** New Expense flow: amount entry, category selection, notes
**Goal:** Verify that the expense entry flow correctly captures, saves, and displays transactions with accurate amounts & categories with appropriate notes. 
Verify that on the home page, the **+** button allows user to add new income to desired categoy and **-** button allows user to add new expense to desired categoy. 
Verify that Balance button correctly calculates the overall Balance for selected period. 
**Approach:** Add expenses across multiple categories using various input methods that includes whole numbers, decimals, and using the built-in arithmetic operators (+, -, *, /). Verify each transaction appears correctly in the transaction list and that the donut chart updates accordingly.

---

### Charter 2: Balance Accuracy & Carry Over Behaviour
**Area:** Home screen balance, Carry Over setting and period-based balance display  
**Goal:** Confirm the app correctly calculates and displays balances across time periods, and that the "Carry over" feature behaves transparently and accurately. The user can opt for and out of carry over feature.
**Approach:** Record known expense amounts, then manually verify the balance. Toggle the "Carry over" setting on/off and observe how the balance and donut chart respond. Check whether the donut correctly shows €0 activity for periods with no new transactions while carry-over balance persists. 

---

### Charter 3: Time Period Filtering & Date Navigation
**Area:** Left-panel filters — Day, Week, Month, Year, All, Interval, Choose Date  
**Goal:** Verify that each time period filter correctly scopes the transaction list and donut chart, and that navigating between dates updates data accurately.  
**Approach:** Apply each filter type in sequence. Swipe between dates. Add transactions on different dates and verify they appear only under the correct filter period. Test edge cases such as the last day of a month and the first day of a new year.

---

### Charter 4: Multi-Account Management & Account Filtering, Search functionality & Transfer feature
**Area:** Accounts: creating, editing accounts and filtering transactions by account,  Search functionality and Transfer feature.
**Goal:** Verify that multiple accounts (e.g. Cash, Payment card) can be managed independently, and that the account filter correctly isolates transactions per account. Verify that Search functionality works as expected. Transfer feature allows user to transfer desired funds between cash & payment card accounts & that reflects correctly on the home page. 
**Approach:** Create a new account (e.g. "Payment card" with Visa icon), add transactions to both accounts, then switch between "All accounts", "Cash", and "Payment card" filters. Verify balances and transaction lists reflect only the selected account's data. Use Search functioanlity to search for desired amount or category to check if it functions properly. Use the Transfer feature to toggle desired amount between cash & payment card accounts & that reflects correctly on the home page for multiple account selections.

---

### Charter 5: Recurring Transactions (Schedule Feature)
**Area:** Schedule / recurring transaction setup: frequency, start date, end date, reminders  
**Goal:** Verify that recurring transaction scheduling works correctly across available frequencies and that reminders and end dates behave as configured.  
**Approach:** Create a recurring weekly expense (e.g. every Monday starting 23 Feb). Verify it appears on the correct dates. Test setting an end date and confirm no entries are created past it. Check whether the "Future recurring records" setting in Settings affects balance display. Test special cases such as the last day of a month, setting reminders & scheduling an end date for the recurring expense. This should be a premium feature available only in paid version of the app. 

---

### Charter 6: Settings, Currency & Security Configuration
**Area:** Settings panel: Currency, First day of month/week, Passcode protection, Budget mode, Export, Synchronization & Data Backup
**Goal:** Verify that global settings are correctly applied across the app and that security features function as expected.  
**Approach:** Change currency and verify it updates on all screens. Change the "First day of month" value and confirm the monthly summary period shifts. Enable passcode protection and verify it triggers on app reopen. Test the "Export to file" feature and verify data integrity in the exported file. Verify Budget mode can be implemented with desired amount. 

---

### Charter 7: Premium Upsell & Freemium Boundary Testing
**Area:** Premium features gate: custom categories, recurring records, multi-device sync, password protection & Synchronization
**Goal:** Understand and document which features are restricted in the free tier, verify the paywall triggers consistently, and check that pricing is displayed correctly for the user's selected App Store region.
**Approach:** Attempt to use custom categories, recurring records, and sync features without a premium subscription. Verify the upsell screen appears at the correct moments. Check that pricing on the upsell screen matches the user's regional App Store.

## Findings & Bug Report

> ✅ = Works as expected | 🐛 = Bug found | ⚠️ = Unexpected behaviour / UX concern/Testing Limitation | 💡 = Observation / improvement suggestion

---

### Charter 1 — Core Expense Entry & Calculator Input

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 1.1 | Tapping the **−** (minus) button on the home screen opens the "New expense" screen with the correct date pre-populated & categories available for selection | ✅ | — |
| 1.2 | Tapping the **+** (plus) button on the home screen opens the "New income" screen with the correct date pre-populated & categories available for selection| ✅ | — |
| 1.3 | The amount input uses a **custom calculator keypad** with arithmetic operators (+, −, ×, ÷, =). This however doesn't allow users to enter expressions like `50+25` or `365/4` that would give the calculated value. The operators have no function|  🐛 | High|
| 1.4 | The selected category (e.g. "Entertainment") is shown **at the bottom of the entry screen** as a large tappable button labelled "ADD 'ENTERTAINMENT'" for saving | ✅ | — |
| 1.5 | The **backspace button** (◀×) on the amount field is visible and accessible, allowing correction without clearing the full amount | ✅ | — |
| 1.6 | There is **Direct editing** option available after adding an expense. The transaction is saved immediately with no undo option visible and editing is only possible through Balance button which might be confusing & frustrating for the user as there is no information provided about EDIT feature specifically| ⚠️ | Medium |
| 1.7 | Entering `0` as the amount and attempting to save — the app behaviour with a zero-amount expense was validated and user couldn't save a meaningless record | ✅ | — |

---

### Charter 2 — Balance Accuracy & Carry Over Behaviour

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 2.1 | In **Day view (26 Feb)**, the donut chart is entirely grey showing **€0.00 income and €0.00 expenses**, yet the balance bar displays **−€239.00**. This is caused by "Carry over" being enabled in Settings — but the visual mismatch between an empty donut and a large negative balance is highly confusing for new users | ⚠️ | High |
| 2.2 | The centre of the donut displays **three separate values**: income (green), expenses (red), and carry over. In day view this reads €0.00 / €0.00 / −€239.00 — presenting a negative balance with zero activity is unintuitive and lacks explanation | ⚠️ | Medium |
| 2.3 | The **"Carry over" setting is enabled by default** in Settings. Users unaware of this will not understand why their balance shows a large negative number with no visible transactions in the current day | ⚠️ | High |
| 2.4 | In the **transaction list for e.g, Mon 23 Feb**, only a single "Carry over" entry (in my case €239.00) is shown with a badge of "1" — the actual other transactions all reside on 5 February. Carry over correctly aggregates prior period balances. | ✅ | — |
| 2.5 | Manual verification: In my sample dashboard, 5 transactions on 5 Feb (Toiletry €150 + Sports €55 + Entertainment €19 + Transport €10 + Communications €5 = **€239.00**) matches the displayed balance of **−€239.00** — calculation is correct | ✅ | — |

---

### Charter 3 — Time Period Filtering & Date Navigation

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 3.1 | The left panel correctly offers: **Day, Week, Month, Year, All, Interval, Choose date** which is a comprehensive range of filter options | ✅ | — |
| 3.2 | Switching from **Month (February)** to **Year (2026)** view shows an **identical donut chart** with the same percentages (Toiletry 63%, Sports 23%, Entertainment 8%, Transport 4%, Communications 2%). Since all transactions are from one day, this is mathematically correct | ✅ | — |
| 3.3 | The **header label correctly updates** — "February" appears in month view and "2026" in year view — confirming the filter scope is applied | ✅ | — |
| 3.4 | Date navigation by **horizontal swiping** works between days (25 Feb ← 26 Feb → next date is visible). Navigation is smooth and intuitive | ✅ | — |
| 3.5 | In **Day view**, the balance bar turns **red** (−€239.00) even though no transactions occurred that day — the carry-over balance colours the bar red, which could mislead users into thinking they overspent today specifically | ⚠️ | Medium |

---

### Charter 4 — Multi-Account Management & Account Filtering, Search functionality & Transfer feature

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 4.1 | A second account **"Payment card"** was successfully created with a Visa icon. The left panel correctly lists: All accounts / Cash / Payment card — all in EUR | ✅ | — |
| 4.2 | The **Edit Account screen** includes: account name, "Included in balance" toggle, currency selector, exchange rate link, initial account balance, and initial balance date which presents a thorough account configuration screen although certain features are premium| ✅ | — |
| 4.3 | The **"Included in balance" toggle** is ON by default for new accounts. The effect of toggling it OFF on overall balance display was not visible |🐛  | Medium |
| 4.4 | When **"Payment card" account is selected**, the balance bar correctly turns **green** (indicating no deficit/expense recorded for that account) | ✅ | — |
| 4.5 | The **Exchange rate field** on the Edit Account screen allows custom rates for foreign currency accounts but no validation was done as it was a premium feature| ⚠️ |— 
| 4.6 | There is a feature to **add new accounts** in the left panel and accounts appear in creation order | ✅ | — |
| 4.7| The **Search** is not properly functional. On searching Car, no results was visible, eventhough there is an expense category named Car. Additionally on typing 2, all expenses beginning with 2 are not displayed, only exact amount search is applicable |🐛  | Medium |
| 4.8| The Transfer feature allows user to transfer funds between accounts which is convenient incase of credit card payments or deposits & other investments | ✅ | — |

---

### Charter 5 — Recurring Transactions (Schedule Feature)

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 5.1 | The **Schedule screen** offers rich recurrence options: Every week (with day-of-week picker), Every two weeks, Every four weeks, Every month, Every two/three/six months, Every year | ✅ | — |
| 5.2 | Recurring records are a **premium-only feature**. The exact blocking behaviour when a free-tier user tries to save a recurring entry was not fully confirmed | ⚠️ | High |
| 5.3 | **"End on: NEVER"** is the default, so recurring transactions continue indefinitely unless manually stopped. Users who forget to set an end date may generate unexpected entries far into the future | 🐛   | Medium |
| 5.4 | **Reminder options** are limited to "Event date" or "Day before" only and no option exists for earlier reminders (e.g. 1 week before a large recurring bill) | 💡 | Low |
| 5.5 | **"Future recurring records"** is **unchecked by default** in Settings meaning scheduled future transactions do not appear in the balance until they actually occur. Users may underestimate upcoming liabilities | 💡 | Low |


---

### Charter 6 — Settings, Currency & Security Configuration

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 6.1 | Settings are organised into two clear sections: **BALANCE** (Budget mode, Carry over, Future recurring records) and **GENERAL SETTINGS** (Language, Currency, Passcode, Export, etc.) | ✅ | — |
| 6.2 | **Passcode protection shows an unlocked padlock icon**, indicating it is NOT enabled by default. For a financial data application, leaving security as Premium feature rather than default available feature is a significant data protection breach | 🐛 | High |
| 6.3 | **"Budget mode"** is unchecked by default and no inline description or tooltip explains what it does. Users have no way to understand this feature without tapping through | ⚠️ | High |
| 6.3 | **"Budget mode"** amount can be entered & toggled ON by the user but it doesn't get reflected on dashboard. Additionally no alert or display informs the user incase the budget amount is exceeded| 🐛 | High |
| 6.4 | Currencies displayed with **$** sign above Settings is provided as a premium feature for user to be able to select different currency options while Currency option within Settings menu lets the user change currency with ease. This is misleading for the user & a potential conflicting feature. |🐛 | High |
| 6.5 | **"First day of week"** defaults to **Sunday**, while for European users (N26's primary market), Monday is the standard. This is a localisation concern | 💡 | Low |
| 6.6 | **"Export to file"** is present in Settings but was not tested — export format, completeness of data, and whether the file is unencrypted plain text (a security risk) remain unverified | ⚠️ | Medium |

---

### Charter 7 — Premium Upsell & Freemium Boundary Testing

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 7.1 | The premium upsell screen promotes four gated features: **unlock everything, custom categories, recurring records, and multi-device sync** | ✅ | — |
| 7.2 | **Currency Ambiguity:** The upsell screen displays pricing in the user's App Store region currency (INR in this case), which is correct behaviour. However, the app's configured currency (EUR) is displayed everywhere else in the app — no label clarifies that the purchase price is in a different currency to the one used within the app. For users in regions with a different currency to their tracking currency, this could cause confusion." | 💡 | Low |
| 7.3 | The **"SAVE 90%"** badge is misleading: ₹599 is a discounted introductory first-year price; the ongoing price is ₹5,900. The 90% saving only applies to year one — the label does not communicate this, which may constitute deceptive pricing. The cancellation rule after one year of service at INR599 is also not specified which breaks user trust| 🐛 | High |
| 7.4 | The **CONTINUE button** does not clearly indicate whether tapping it initiates a purchase immediately or leads to a confirmation step — risk of accidental purchase | ⚠️ | High |
| 7.5 | The upsell can be **dismissed via the X button** in the top-right corner — confirming the app remains usable without premium | ✅ | — |
| 7.6 | **"Unlock Monefy"** in Settings (with a diamond icon) provides a consistent second entry point to the premium upgrade | ✅ | — |

---
## Charter Prioritisation
> Prioritisation is based on **bug severity**, **user impact**, and **frequency of the affected feature** in day-to-day usage.

| Priority | Charter | Bugs Found | Reason |
|----------|---------|-----------|--------|
| **P1 — Critical** | Charter 6: Settings, Currency & Security | 🐛 High (6.2), 🐛 High (6.3 ×2), 🐛 High (6.4) | The highest-severity charter with four confirmed high-severity bugs, the most in any single charter. Passcode protection being locked behind a paywall rather than freely available (6.2) is a serious data protection concern for a financial app. Budget mode is silently non-functional with no on-screen feedback (6.3). Users set a budget believing it is enforced when it is not. The conflicting Currency entry points one free & one premium, creates genuine confusion about which setting is actually applied (6.4). These bugs collectively undermine security, trust, and the app's core budgeting purpose. |
| **P2 — High** | Charter 1: Core Expense Entry & Calculator Input | 🐛 High (1.3), ⚠️ Medium (1.6) | The arithmetic operators on the custom keypad are non-functional (Finding 1.3) this is the most-used input screen in the entire app. A user cannot enter `150/2` or `55+19` expecting a calculated result, as they cannot use the logical operators. This affects every single expense entry and is rated the highest-impact functional bug after Charter 6. The lack of visible edit guidance (1.6) further compounds frustration after a wrong entry. |
| **P2 — High** | Charter 2: Balance Accuracy & Carry Over | ⚠️ High (2.1), ⚠️ High (2.3), ⚠️ Medium (2.2) | No data integrity bugs were found & balance calculations are mathematically correct (Finding 2.5). However, carry-over is enabled by default with no explanation, causing every new user to see a large negative balance against an empty donut chart on first launch (2.1, 2.3). This is a first-impression failure that will drive user drop-off and support queries at scale. Rated P2 rather than P1 because the underlying data is accurate, the problem is presentation, not calculation. |
| **P3 — Medium** | Charter 4: Multi-Account, Search & Transfer | 🐛 Medium (4.3), 🐛 Medium (4.7) | Two functional bugs in secondary flows: the "Included in balance" toggle has no visible effect when turned off (4.3), and Search does not support category name lookup or partial amount matching (4.7), making it practically unusable. Both affect features users would rely on as their data grows, but neither blocks the core expense-tracking flow. |
| **P3 — Medium** | Charter 7: Premium Upsell & Freemium Boundary | 🐛 High (7.3), ⚠️ High (7.4), 💡 Low (7.2) | The misleading "SAVE 90%" badge that only applies to year one with no cancellation terms disclosed (7.3), and the ambiguous CONTINUE button that may trigger an immediate purchase (7.4) are genuine concerns at the payment boundary but do not constitute functional defects. |
| **P3 — Medium** | Charter 5: Recurring Transactions | ⚠️ High (5.2), 🐛 Medium (5.3) | Recurring transactions are premium-only, which limits their immediate free-tier impact. However, the "End on: NEVER" default (5.3) is a silent data integrity risk for paying users who set up bills and forget to specify an end date. The unconfirmed premium blocking behaviour (5.2) also needs verification to ensure free-tier users see a clear paywall rather than a silent failure. |
| **P4 — Lower** | Charter 3: Time Period Filtering & Date Navigation | ⚠️ Medium (3.5) | The cleanest charter as all core filter and navigation behaviours work correctly (3.1–3.4). The only concern is the carry-over balance colouring the day-view bar red even on days with no transactions (3.5), which is a cosmetic consequence of the carry-over UX issue identified in Charter 2 and not an independent defect. Lowest priority because no functional bugs were found. |

---

## Risk Assessment

### 1. Financial Calculation & Display Risk
**Risk:** Confusing balance displays (empty donut + large negative balance due to carry-over) could cause users to misread their financial position and make incorrect spending decisions.  
**Impact:** High because users rely on this app for real financial decisions.  
**Mitigation:** Add an explanatory tooltip or visual indicator when carry-over is active. Automate regression tests on balance calculations across all period filter combinations, including carry-over toggled on/off with budget-mode switched on/off.

---

### 2. Payment Transparency & Pricing Clarity Risk
**Risk:** The "SAVE 90%" badge on the premium upsell screen only applies to the introductory first-year price the ongoing annual cost is 10x higher and no cancellation terms are disclosed. Additionally, users whose App Store region differs from their in-app tracking currency receive no label clarifying which currency they will actually be charged in.  
**Impact:** Medium while App Store region pricing is technically correct behaviour, the lack of transparency around the promotional pricing and auto-renewal terms could erode user trust and may fall foul of App Store review guidelines on clear pricing disclosure.  
**Mitigation:** Add explicit labelling of the purchase currency on the upsell screen. Rewrite the "SAVE 90%" badge to communicate that it applies to year one only, and include a summary of renewal terms before the CONTINUE button. Test the upsell screen across multiple App Store regions to verify pricing and currency labels render correctly in each.

---

### 3. Data Privacy & Security Risk
**Risk:** Passcode protection is not enabled by default. All personal financial data is immediately accessible on an unlocked or shared device.  
**Impact:** High because on a lost or shared device, full spending history is exposed with no barrier.  
**Mitigation:** Prompt users during onboarding to configure passcode or biometric lock. Test that once enabled, the passcode is consistently enforced on app reopen, return from background, and after device restart.

---

### 4. Data Loss & Accidental Entry Risk
**Risk:** No undo mechanism is visible after adding a transaction. Accidental entries have no quick recovery path. Only an indirect manual edit & delete functionality through Balance button.
**Impact:** High accidental entries corrupt financial records. The indirect edit & delete functionality without any indicators, might be frustrating & inconvenient for the user & increase the dropout rates.
**Mitigation:** Test the full edit and delete flow for transactions. Verify that deleted transactions update all affected period balances immediately. Consider recommending an undo action within a short post-save window & navigation indicators for frequently used functionalities like edit & delete. 

---

### 5. Recurring Transaction Integrity Risk
**Risk:** Recurring transactions default to "End on: NEVER" and are excluded from the balance by default until the event date. Users budgeting for upcoming bills will not see them reflected in forward-looking balance views.  
**Impact:** Medium as it leads to understated future liability, undermining the app's budgeting purpose.  
**Mitigation:** Test recurring entry creation on correct dates. Test toggling "Future recurring records" on/off and verify balance updates reflect the change immediately. Validate behaviour at period boundaries (month-end, year-end).

---

### 6. Localisation & Regional Settings Risk
**Risk:** Default "First day of week" is Sunday (not Monday, standard for Europe). Decimal separators and date formats may not adapt to all locales. 
**Impact:** Medium because incorrect regional defaults create confusion and data misinterpretation for international users. 
**Mitigation:** Test with device locale set to German, French, and Indian regional settings. Verify date formats, currency symbols, decimal separators, and week-start defaults adapt correctly to device locale.

---

*End of Exploratory Testing Report — Monefy iOS App*  
*Testing performed manually on iOS device, session duration approximately 2 hours.*

