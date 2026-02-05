# 🔧 Troubleshooting Guide

## Error: "Could not establish connection. Receiving end does not exist."

### 🎯 What This Means (Simple Explanation)

Think of it like this:
- **popup.js** (the button) is trying to call **content.js** (the email reader)
- But **content.js** isn't running on the Gmail page
- It's like trying to call someone who isn't there!

### ✅ Solution (Do This First!)

**The most common fix:** Refresh the Gmail page after installing the extension.

1. **Go to your Gmail tab**
2. **Press `F5` (Windows) or `Cmd+R` (Mac)** to refresh
3. **Wait for Gmail to fully load**
4. **Open an email** (click on any email)
5. **Click the extension icon** again
6. **Click "Analyze Email"**

This should fix it 90% of the time!

---

## Why Does This Happen?

When you install a Chrome extension:
- The extension files are loaded
- But if Gmail was **already open**, the content script doesn't automatically run
- Chrome only injects content scripts into **new pages** or **refreshed pages**

**Analogy:** It's like installing a new app on your phone - you need to restart it for the changes to take effect!

---

## Step-by-Step Fix

### Method 1: Refresh Gmail (Easiest)
1. ✅ Make sure extension is installed
2. ✅ Go to Gmail tab
3. ✅ Press `F5` or `Cmd+R` to refresh
4. ✅ Open any email
5. ✅ Try the extension again

### Method 2: Reload Extension
1. Go to `chrome://extensions/`
2. Find "EventSense AI Demo"
3. Click the **reload icon** (circular arrow) 🔄
4. Go back to Gmail
5. **Refresh Gmail** (F5 or Cmd+R)
6. Open an email
7. Try again

### Method 3: Full Reset
1. Go to `chrome://extensions/`
2. Remove the extension (click "Remove")
3. Close all Gmail tabs
4. Reload the extension (Load unpacked)
5. Open a **new** Gmail tab
6. Open an email
7. Try the extension

---

## How to Verify Content Script is Running

1. Open Gmail
2. Press `F12` (or right-click → Inspect)
3. Go to **Console** tab
4. You should see: `"EventSense AI: Content script loaded!"`
5. If you don't see this, the script isn't running → **Refresh the page**

---

## Other Common Issues

### Issue: "No email content found"
**Cause:** You're not viewing an email, or Gmail's structure changed
**Fix:** 
- Make sure you clicked on an email (not just the inbox)
- The email should be fully loaded
- Try a different email

### Issue: Extension icon doesn't appear
**Fix:**
- Go to `chrome://extensions/`
- Make sure extension is enabled (toggle is ON)
- Click the puzzle piece icon in Chrome toolbar
- Pin "EventSense AI Demo" if needed

### Issue: Button doesn't work
**Fix:**
- Check browser console for errors (F12 → Console)
- Make sure popup.html and popup.js are in the extension folder
- Reload the extension

---

## Still Not Working?

1. **Check Chrome Console:**
   - Press F12 on Gmail page
   - Look for red error messages
   - Take a screenshot and check what it says

2. **Check Extension Console:**
   - Go to `chrome://extensions/`
   - Click "Service worker" or "Inspect views: popup"
   - Look for errors

3. **Verify Files:**
   - Make sure all files are in the `extension` folder:
     - ✅ manifest.json
     - ✅ popup.html
     - ✅ popup.js
     - ✅ content.js

---

## Quick Checklist

Before asking for help, make sure:
- [ ] Extension is installed and enabled
- [ ] Gmail page was refreshed AFTER installing extension
- [ ] You have an email open (not just the inbox)
- [ ] You're on mail.google.com (not a different email service)
- [ ] No ad blockers are interfering
- [ ] Chrome is up to date

---

## Need More Help?

If none of this works, check:
1. Chrome version (should be recent)
2. Any error messages in the console
3. Whether other extensions might be interfering

The code has been updated to automatically try to inject the script if it's missing, but refreshing Gmail is still the most reliable solution!
