# 🚀 How to Install the Extension - Step by Step

## ❌ The Problem

You're getting "Manifest file is missing or unreadable" because Chrome is looking for `manifest.json` in the folder you selected, but it can't find it.

## ✅ The Solution

You need to select the **`extension` folder**, NOT the root project folder!

---

## 📁 Folder Structure Explained

Your project looks like this:
```
eventsense-ai-demo/          ← ❌ DON'T SELECT THIS (root folder)
├── extension/                ← ✅ SELECT THIS FOLDER!
│   ├── manifest.json         ← Chrome needs this file
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   └── ...
├── src/
├── data/
└── ...
```

**Why?** Chrome looks for `manifest.json` in the folder you select. If you select the root folder, Chrome looks for `manifest.json` in the root, but it's actually inside the `extension` folder!

---

## 🎯 Step-by-Step Installation

### Step 1: Open Chrome Extensions Page
1. Open Google Chrome
2. Type in address bar: `chrome://extensions/`
3. Press Enter

### Step 2: Enable Developer Mode
- Look for a toggle switch in the **top-right corner** that says "Developer mode"
- Turn it **ON** (it should be blue/highlighted)

### Step 3: Load the Extension
1. Click the button **"Load unpacked"** (appears after enabling Developer mode)
2. A file browser window will open
3. **Navigate to:** `/Users/sanjaybala/Desktop/Alex/eventsense-ai-demo/`
4. **Click on the `extension` folder** (the one that contains manifest.json)
5. Click **"Select"** or **"Open"**

### Step 4: Verify It Worked
- You should see "EventSense AI Demo" appear in your extensions list
- No error messages should appear
- The extension icon should appear in your Chrome toolbar

---

## 🔍 How to Know You Selected the Right Folder

**✅ CORRECT:** When you select the `extension` folder, you should see these files:
- manifest.json
- popup.html
- popup.js
- content.js

**❌ WRONG:** If you selected the root folder, you'll see:
- extension/ (folder)
- src/ (folder)
- data/ (folder)
- README.md
- etc.

**Remember:** Chrome needs to see `manifest.json` directly in the folder you select, not inside a subfolder!

---

## 🐛 If You Still Get Errors

### Error: "Manifest file is missing or unreadable"
- **Cause:** You selected the wrong folder
- **Fix:** Make sure you select the `extension` folder, not the root folder

### Error: "Could not load manifest"
- **Cause:** The manifest.json file has syntax errors
- **Fix:** The file is already correct, so this shouldn't happen. If it does, try:
  1. Close and reopen Chrome
  2. Remove the extension and reload it

### Error: "This extension may have been corrupted"
- **Cause:** Sometimes Chrome caches old data
- **Fix:** 
  1. Remove the extension
  2. Restart Chrome
  3. Load it again

---

## 📝 Quick Checklist

Before clicking "Load unpacked", make sure:
- [ ] You're in Developer mode
- [ ] You navigate to: `Desktop/Alex/eventsense-ai-demo/`
- [ ] You select the **`extension`** folder (not the root)
- [ ] You can see `manifest.json` in the folder you're about to select
- [ ] You click "Select" or "Open"

---

## 🎉 Success!

Once loaded successfully, you should see:
- Extension name: "EventSense AI Demo"
- Version: 1.0
- A toggle switch to enable/disable it
- An icon in your Chrome toolbar

Then test it:
1. Go to Gmail (mail.google.com)
2. Open any email
3. Click the extension icon
4. Click "Analyze Email"
5. See the magic happen! ✨
