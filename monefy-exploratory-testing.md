# Monefy App — Exploratory Testing Session

**Tester:** Swarnima Singh 
**Platform:** iOS  
**App Version:** 1.10.4  
**Date:** 27 February 2026  
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

> ✅ = Works as expected | 🐛 = Bug found | ⚠️ = Unexpected behaviour / UX concern/Testing Limitation |

---

### Charter 1 — Core Expense Entry & Calculator Input

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 1.1 | Tapping the **−** (minus) button on the home screen opens the "New expense" screen with the correct date pre-populated & categories available for selection | ✅ | — |
| 1.2 | Tapping the **+** (plus) button on the home screen opens the "New income" screen with the correct date pre-populated & categories available for selection| ✅ | — |
| 1.3 | The custom calculator keypad works correctly but lacks visual display when operators are entered| ⚠️ | Low |
| 1.4 | The selected category (e.g. "Entertainment") is shown **at the bottom of the entry screen** as a large tappable button labelled "ADD 'ENTERTAINMENT'" for saving | ✅ | — |
| 1.5 | The **backspace button** (◀×) on the amount field is visible and accessible, allowing correction without clearing the full amount | ✅ | — |
| 1.6 | There is **Direct editing** option available after adding an expense. The transaction is saved immediately with no undo option visible and editing is only possible through Balance button which might be confusing & frustrating for the user as there is no information provided about EDIT feature specifically| ⚠️ | Medium |
| 1.7 | Entering `0` as the amount and attempting to save — the app behaviour with a zero-amount expense was validated and user couldn't save a meaningless record | ✅ | — |

---

### Charter 2 — Balance Accuracy & Carry Over Behaviour

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 2.1 | The **"Carry over" setting is enabled by default** in Settings. Users unaware of this will not understand why their balance shows a large negative number with no visible transactions in the current day | ⚠️ | Medium |
| 2.2 | In the **transaction list for e.g, Mon 23 Feb**, only a single "Carry over" entry (in my case €239.00) is shown with a badge of "1" — the actual other transactions all reside on 5 February. Carry over correctly aggregates prior period balances. | ✅ | — |
| 2.3 | Manual verification: In my sample dashboard, 5 transactions on 5 Feb (Toiletry €150 + Sports €55 + Entertainment €19 + Transport €10 + Communications €5 = **€239.00**) matches the displayed balance of **−€239.00** — calculation is correct | ✅ | — |

---

### Charter 3 — Time Period Filtering & Date Navigation

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 3.1 | The left panel correctly offers: **Day, Week, Month, Year, All, Interval, Choose date** which is a comprehensive range of filter options | ✅ | — |
| 3.2 | Switching from **Month (February)** to **Year (2026)** view shows an **identical donut chart** with the same percentages (Toiletry 63%, Sports 23%, Entertainment 8%, Transport 4%, Communications 2%). Since all transactions are from one day, this is mathematically correct | ✅ | — |
| 3.3 | The **header label correctly updates** — "February" appears in month view and "2026" in year view — confirming the filter scope is applied | ✅ | — |
| 3.4 | Date navigation by **horizontal swiping** works between days (25 Feb ← 26 Feb → next date is visible). Navigation is smooth and intuitive | ✅ | — |

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
| 4.7| The **Search** is not properly functional. On searching Car, no results was visible, eventhough there is an expense category named Car. Additionally on typing 2, all expenses beginning with 2 are not displayed, only exact amount search is applicable. The ‘<' & '>‘ operator usage to expand search was redundant |🐛  | Medium |
| 4.8| The Transfer feature allows user to transfer funds between accounts which is convenient incase of credit card payments or deposits & other investments | ✅ | — |

---

### Charter 5 — Recurring Transactions (Schedule Feature)

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 5.1 | The **Schedule screen** offers rich recurrence options: Every week (with day-of-week picker), Every two weeks, Every four weeks, Every month, Every two/three/six months, Every year | ✅ | — |
| 5.2 | Recurring records are a **premium-only feature**. The exact blocking behaviour when a free-tier user tries to save a recurring entry was not fully confirmed | ⚠️ | — |

---

### Charter 6 — Settings, Currency & Security Configuration

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 6.1 | Settings are organised into two clear sections: **BALANCE** (Budget mode, Carry over, Future recurring records) and **GENERAL SETTINGS** (Language, Currency, Passcode, Export, etc.) | ✅ | — |
| 6.2 | **"Budget mode"** amount can be entered & toggled ON by the user but it doesn't get reflected on dashboard. Additionally no alert or display informs the user incase the budget amount is exceeded| 🐛 | High |
| 6.3 | Currencies displayed with **$** sign above Settings is provided as a premium feature for user to be able to select different currency options while Currency option within Settings menu lets the user change currency with ease. This is misleading for the user & a potential conflicting feature. |🐛 | High |
| 6.4 | **"Export to file"** is present in Settings but was not tested — export format, completeness of data, and whether the file is unencrypted plain text (a security risk) remain unverified | ⚠️ | Medium |

---

### Charter 7 — Premium Upsell & Freemium Boundary Testing

| # | Observation | Status | Severity |
|---|-------------|--------|----------|
| 7.1 | The premium upsell screen promotes four gated features: **unlock everything, custom categories, recurring records, and multi-device sync** | ✅ | — |
| 7.2 | The upsell can be **dismissed via the X button** in the top-right corner — confirming the app remains usable without premium | ✅ | — |
| 7.3 | **"Unlock Monefy"** in Settings (with a diamond icon) provides a consistent second entry point to the premium upgrade | ✅ | — |

---
## Charter Prioritisation
> Prioritisation is based on **criticality of the functionality to the app's core purpose** and **severity of findings discovered**. A charter covering a critical flow ranks highly regardless of whether bugs were found — because the cost of missing a defect there is highest.

| Priority | Charter | Reason |
|----------|---------|--------|
| **P1 — Critical** | Charter 1: Core Expense & Income Entry | This is the highest frequency user action in the entire app. Every user performs this multiple times daily. It is the foundation on which all other features depend. If expense or income entry is broken or confusing, the entire app fails its purpose regardless of how well everything else works. Must always be tested first and most thoroughly. |
| **P1 — Critical** | Charter 2: Balance Accuracy & Carry Over | A money management app that displays an incorrect or confusing balance fails at its single most important job. Users make real financial decisions based on this number. Even though no calculation bugs were found in this session, balance accuracy makes sense to be a P1 charter because the cost of missing a defect here is the highest of any feature. |
| **P2 — High** | Charter 6: Settings, Currency & Security | Settings apply globally & a misconfigured currency or a silently broken budget mode corrupts every piece of data the user sees across the entire app. Two high-severity bugs were found here: budget mode does not reflect on the dashboard (6.2) and conflicting currency entry points create confusion(6.3). The overall impact of settings makes this a P2 regardless of findings. |
| **P2 — High** | Charter 3: Time Period Filtering & Date Navigation | Filtering by time period is how users review and understand their spending patterns. It is used constantly alongside expense entry. Date and period logic is also one of the most common sources of edge case bugs in financial apps (month boundaries, leap years, timezone handling). Rated P2 because of how central it is to the user experience even though no bugs were found in this session. |
| **P3 — Medium** | Charter 4: Multi-Account, Search & Transfer | Important for users managing multiple payment methods, which is a common real-world scenario. Two functional bugs were found: The balance toggle has no visible effect (4.3) and search is limited to exact amount & text matching (4.7). Rated P3 rather than P2 because these features are secondary to the core single-account expense tracking flow. |
| **P3 — Medium** | Charter 5: Recurring Transactions | Recurring transactions are essential for users tracking regular bills and subscriptions, which is a core budgeting use case. However, this is a premium-only feature in Monefy, which limits its immediate impact on free-tier users. This untested functionality (5.2) remains an open test item. |
| **P4 — Lower** | Charter 7: Premium Upsell & Freemium Boundary | Important from a business and revenue perspective but does not affect the core money management experience. No functional bugs were found in this session. Lower priority for functional testing. |

---

## Risk Assessment

> This section identifies the categories of risk that must be mitigated in **any personal finance or budgeting application similar to Monefy**, based on the nature of the data handled and the expectations users bring to this type of product.

---

### 1. 💰 Financial Calculation Accuracy Risk
**Risk:** Incorrect calculations, rounding errors, or currency conversion mistakes lead to wrong balances, totals, or summaries being displayed to the user.
**Why it matters:** Users make real spending and saving decisions based on the numbers they see. A budgeting app that shows wrong figures creates false confidence.
**Mitigation:** Rigorous automated testing of all arithmetic operations including edge cases such as very large amounts, decimal precision, negative balances, and multi-currency conversions. Regression tests must run on every release to catch calculation regressions early.

---

### 2. 🔒 Data Privacy & Security Risk
**Risk:** Personal financial data spending habits, account balances, transaction history  is sensitive by nature. Risks include unauthorised access on shared devices, unencrypted local storage, insecure data export, and lack of app-level authentication.
**Why it matters:** Unlike a social or productivity app, a finance app holds information users consider highly private. A security breach or accidental exposure on a shared device has real personal consequences. In European markets, this is also a GDPR compliance concern.
**Mitigation:** Multi-factor authentication should be available to all users as a baseline. Local data storage should be encrypted. Exported files should not contain sensitive data in plain text. Security testing should be part of every release cycle.

---

### 3. 📊 Data Integrity & Persistence Risk
**Risk:** Transaction data entered by the user is lost, corrupted, or not saved correctly due to app crashes, unexpected backgrounding, OS updates, or device changes.
**Why it matters:** Financial history is irreplaceable. Data loss in a finance app destroys trust immediately and permanently.
**Mitigation:** Test data persistence across all app lifecycle events: backgrounding, force close, device restart, and OS update. Verify that backup and restore flows preserve all transaction data completely and without duplication. Automated tests should confirm data is written to storage immediately on entry & exit.

---

### 4. 🔄 Synchronisation & Consistency Risk
**Risk:** In apps that support multiple accounts, multi-device sync, or recurring transactions, data can become inconsistent. Duplicate entries, missing transactions, or balances that differ across views or devices.
**Why it matters:** Users trust that the balance they see on one screen matches what they see on another. Inconsistencies in financial data erode confidence and are difficult for users to diagnose themselves.
**Mitigation:** Test multi-account balance aggregation thoroughly, particularly when accounts are added, removed, or excluded from the overall balance. For apps with sync features, test conflict resolution when the same data is modified on two devices simultaneously.

---

### 5. 🌍 Localisation & Regional Compliance Risk
**Risk:** Financial apps are used across different regions with different currencies, date formats, decimal separators, tax rules, and regulatory requirements. An app that does not adapt correctly to locale settings can display misleading data or fail compliance requirements.
**Why it matters:** A date formatted as MM/DD vs DD/MM, or a decimal separator of comma vs period, can cause users to misread amounts. In regulated markets, incorrect currency handling can also have legal implications.
**Mitigation:** Test the app across multiple device locales covering at minimum the primary target markets. Verify that currency symbols, decimal separators, date formats all adapt to device locale. Pricing and subscription screens should always display the correct currency.

---

### 6. ♿ Accessibility & Usability Risk
**Risk:** Financial apps used daily must be clear, readable, and accessible to all users including those with visual impairments, colour blindness, or low digital literacy. Poor usability leads to data entry errors, which in a finance app means inaccurate financial records.
**Why it matters:** A user who misreads a balance due to low contrast, or accidentally enters the wrong amount due to a confusing UI, ends up with incorrect financial data. Usability failures in finance apps have a direct downstream impact on building a customer base.
**Mitigation:** Test colour contrast ratios for balance indicators, particularly the red/green balance bar which rely on colour to convey meaning. Verify that all interactive elements are accessible via screen readers. User testing with non-technical users should be part of the release process to catch discoverability issues like hidden edit and delete flows.

---

*End of Exploratory Testing Report — Monefy iOS App*
*Testing performed manually on iOS device*




