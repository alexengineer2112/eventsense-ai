// This script runs on Gmail pages and extracts email content
// It listens for messages from popup.js and sends back the email text

console.log("EventSense AI: Content script loaded!");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getEmailText") {
    console.log("EventSense AI: Received request to extract email text");
    
    // Try multiple selectors to find the email body in Gmail
    // Gmail uses different selectors depending on the view
    let emailBody = null;
    let text = "";
    
    // Method 1: Try the main email content area
    emailBody = document.querySelector("div[role='main'] div[dir='ltr']");
    
    // Method 2: Try Gmail's email body class
    if (!emailBody || emailBody.innerText.trim() === "") {
      emailBody = document.querySelector(".a3s");
    }
    
    // Method 3: Try the message body
    if (!emailBody || emailBody.innerText.trim() === "") {
      emailBody = document.querySelector("[data-message-id]");
    }
    
    // Method 4: Try finding by aria-label
    if (!emailBody || emailBody.innerText.trim() === "") {
      emailBody = document.querySelector("[aria-label*='Message Body']");
    }
    
    // Method 5: Try the email view container
    if (!emailBody || emailBody.innerText.trim() === "") {
      const containers = document.querySelectorAll("div[role='main']");
      for (let container of containers) {
        const innerText = container.innerText.trim();
        if (innerText.length > 100) { // Likely the email body
          emailBody = container;
          break;
        }
      }
    }
    
    // Extract text
    if (emailBody) {
      text = emailBody.innerText.trim();
    }
    
    // If still no text, try to get any visible text from main area
    if (!text || text.length < 10) {
      const mainArea = document.querySelector("div[role='main']");
      if (mainArea) {
        text = mainArea.innerText.trim();
      }
    }
    
    if (!text || text.length < 10) {
      text = "No email content found. Please make sure you have an email open and visible in Gmail.";
    }
    
    console.log("EventSense AI: Extracted text length:", text.length);
    sendResponse({ emailText: text });
  }
  return true; // Required for async message handling
});
