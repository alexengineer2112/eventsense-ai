# EventSense AI Extension - Complete Beginner's Guide

## 🎯 What This Extension Does

This Chrome extension reads emails in Gmail and automatically:

1. **Categorizes** them as "Placement", "Workshop", or "General"
2. **Extracts deadlines** in multiple date formats
3. **Displays** the results in a popup window

---

## 📁 File Structure Explained

### 1. **manifest.json** - The Extension's ID Card

Think of this as the extension's "ID card" that tells Chrome:

- What the extension is called
- What permissions it needs
- Which files to use
- Where it can run (only on Gmail)

**Key Parts:**

- `"permissions": ["activeTab", "scripting"]` - Allows reading the current tab
- `"matches": ["https://mail.google.com/*"]` - Only works on Gmail
- `"default_popup": "popup.html"` - Shows this HTML when you click the extension icon

---

### 2. **popup.html** - The User Interface

This is what you see when you click the extension icon. It contains:

- A button to analyze emails
- A display area for results
- Styling (CSS) to make it look nice

**How it works:**

- When you click "Analyze Email", it triggers the JavaScript in `popup.js`
- The results appear in the `<pre id="output">` element

---

### 3. **content.js** - The Email Reader

This script runs **inside** Gmail pages (like a spy that can read the page).

**What it does:**

1. Waits for a message from `popup.js`
2. Finds the email content on the Gmail page
3. Extracts the text
4. Sends it back to `popup.js`

**Why multiple selectors?**
Gmail changes its HTML structure sometimes, so we try different ways to find the email:

- `div[role='main']` - Main email area
- `.a3s` - Gmail's email body class
- `[data-message-id]` - Alternative selector

---

### 4. **popup.js** - The Brain

This is where the magic happens! It:

1. Listens for button clicks
2. Communicates with `content.js` to get email text
3. Analyzes the text to find category and deadline
4. Displays results

**Key Functions:**

#### `categorizeEmail(text)`

Checks if the email contains keywords:

- **Placement**: "placement", "recruitment", "internship", "job"
- **Workshop**: "workshop", "training", "seminar"
- **General**: Everything else

#### `extractDeadline(text)`

Uses **Regular Expressions (Regex)** to find dates in multiple formats:

**Supported Date Formats:**

1. `15th January 2026` or `15 January 2026`
2. `January 15, 2026` or `Jan 15, 2026`
3. `15/01/2026` or `15-01-2026` or `15.01.2026`
4. `2026-01-15` (ISO format)
5. `15th Jan 2026`
6. `Deadline: 15 January` (without year)

**How Regex Works (Simple Explanation):**

- `\d{1,2}` = 1 or 2 digits (day)
- `(?:st|nd|rd|th)?` = Optional suffix like "st", "nd", "rd", "th"
- `\s+` = One or more spaces
- `\w+` = One or more word characters (month name)
- `\d{4}` = Exactly 4 digits (year)
- `i` = Case-insensitive matching

---

## 🔄 How Everything Works Together

```
1. User opens Gmail and clicks on an email
   ↓
2. User clicks the extension icon → popup.html opens
   ↓
3. User clicks "Analyze Email" button
   ↓
4. popup.js sends a message to content.js
   ↓
5. content.js reads the email from Gmail page
   ↓
6. content.js sends email text back to popup.js
   ↓
7. popup.js analyzes the text:
   - Checks for keywords → Category
   - Searches for date patterns → Deadline
   ↓
8. Results displayed in popup.html
```

---

## 🐛 About the CSS Error

The error you saw (`Unknown word (CssSyntaxError)`) is a **false positive**.

**What happened:**

- Your linter/editor is incorrectly treating HTML and JavaScript files as CSS files
- The actual code is correct and will work fine

**Solution:**

- The code is fixed and ready to use
- You can ignore these linter warnings
- The extension will work perfectly in Chrome

---

## 🚀 How to Install and Test

1. **Open Chrome Extensions:**

   - Go to `chrome://extensions/`
   - Enable "Developer mode" (top right)

2. **Load the Extension:**

   - Click "Load unpacked"
   - Select the `extension` folder

3. **Test It:**
   - Go to Gmail (mail.google.com)
   - Open any email
   - Click the extension icon
   - Click "Analyze Email"
   - See the results!

---

## 📚 Learning Points for Beginners

### JavaScript Concepts Used:

1. **Event Listeners**: `addEventListener("click", ...)`

   - Waits for user actions (like button clicks)

2. **Chrome Extension API**: `chrome.tabs.query()`, `chrome.tabs.sendMessage()`

   - Special functions to interact with browser tabs

3. **Regular Expressions**: Patterns like `/\d{1,2}\s+\w+\s+\d{4}/`

   - Powerful way to find patterns in text

4. **DOM Manipulation**: `document.getElementById()`, `.textContent`

   - How to change what's displayed on the page

5. **Message Passing**: Communication between `popup.js` and `content.js`
   - Different parts of the extension talking to each other

---

## 🎓 Next Steps to Learn More

1. **Try modifying the keywords** in `categorizeEmail()` to detect other categories
2. **Add more date formats** to `extractDeadline()` if needed
3. **Style the popup** by editing the CSS in `popup.html`
4. **Add error handling** for edge cases
5. **Store results** using Chrome's storage API

---

## ✅ Summary

- **manifest.json**: Extension configuration
- **popup.html**: User interface
- **content.js**: Reads Gmail emails
- **popup.js**: Analyzes and displays results

The extension is now complete and ready to use! 🎉
