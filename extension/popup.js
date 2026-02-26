// Function to detect multiple date formats in the email text
function extractDeadline(text) {
  // Array of date patterns to match different formats
  const datePatterns = [
    // Format: "15th January 2026" or "15 January 2026"
    /\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4}/i,
    // Format: "January 15, 2026" or "Jan 15, 2026"
    /\w+\s+\d{1,2},?\s+\d{4}/i,
    // Format: "15/01/2026" or "15-01-2026" or "15.01.2026"
    /\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4}/,
    // Format: "2026-01-15" (ISO format)
    /\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}/,
    // Format: "15th Jan 2026"
    /\d{1,2}(?:st|nd|rd|th)?\s+\w{3}\s+\d{4}/i,
    // Format: "Deadline: 15 January" (without year, assumes current or next year)
    /deadline[:\s]+\d{1,2}(?:st|nd|rd|th)?\s+\w+/i,
  ];

  // Time patterns to match various time formats
  const timePatterns = [
    // Format: "12:00 PM" or "12:00PM" or "12:00 p.m." or "12:00p.m."
    /\d{1,2}:\d{2}\s*(?:AM|PM|a\.m\.|p\.m\.|am|pm)/i,
    // Format: "12 PM" or "12PM" or "12 p.m." or "12p.m."
    /\d{1,2}\s*(?:AM|PM|a\.m\.|p\.m\.|am|pm)/i,
    // Format: "12:00:00" (24-hour format with seconds)
    /\d{1,2}:\d{2}:\d{2}/,
    // Format: "12:00" (24-hour format)
    /\d{1,2}:\d{2}(?!\d)/,
  ];

  // Try each date pattern and return the first match with time if available
  for (let pattern of datePatterns) {
    const match = text.match(pattern);
    if (match) {
      let dateStr = match[0].trim();
      const dateIndex = match.index;

      // Look for time pattern near the date (within 50 characters after the date)
      const textAfterDate = text.substring(
        dateIndex + match[0].length,
        dateIndex + match[0].length + 50
      );

      for (let timePattern of timePatterns) {
        const timeMatch = textAfterDate.match(timePattern);
        if (timeMatch) {
          // Format: "Date, Time"
          return `${dateStr}, ${timeMatch[0].trim()}`;
        }
      }

      // If no time found, return just the date
      return dateStr;
    }
  }

  return "Not Found";
}

// Function to categorize the email
function categorizeEmail(text) {
  const lowerText = text.toLowerCase();

  // Check for specific categories in order of priority
  if (lowerText.includes("placement")) {
    return "Placement";
  } else if (lowerText.includes("internship")) {
    return "Internship";
  } else if (lowerText.includes("recruitment")) {
    return "Recruitment";
  } else if (lowerText.includes("job")) {
    return "Job";
  } else if (
    lowerText.includes("workshop") ||
    lowerText.includes("training") ||
    lowerText.includes("seminar")
  ) {
    return "Workshop";
  }

  return "General";
}

// Function to send message to content script with retry
function sendMessageToContentScript(tabId, retryCount = 0) {
  chrome.tabs.sendMessage(tabId, { action: "getEmailText" }, (response) => {
    // If connection failed, try injecting the script first
    if (chrome.runtime.lastError) {
      if (retryCount === 0) {
        // Try to inject the content script manually
        chrome.scripting.executeScript(
          {
            target: { tabId: tabId },
            files: ["content.js"],
          },
          () => {
            // Wait a bit for script to load, then retry
            setTimeout(() => {
              sendMessageToContentScript(tabId, 1);
            }, 100);
          }
        );
      } else {
        document.getElementById("output").textContent =
          "Error: Could not connect to Gmail page.\n\n" +
          "SOLUTION:\n" +
          "1. Refresh the Gmail page (press F5 or Cmd+R)\n" +
          "2. Open an email\n" +
          "3. Click the extension icon again\n" +
          "4. Click Analyze Email";
      }
      return;
    }

    if (!response || !response.emailText) {
      document.getElementById("output").textContent =
        "Error: Could not extract email content.\n\nMake sure you have an email open in Gmail.";
      return;
    }

    const text = response.emailText;
    const category = categorizeEmail(text);
    const deadline = extractDeadline(text);

    // Display the results
    document.getElementById(
      "output"
    ).textContent = `Category: ${category}\nDeadline: ${deadline}\n\n---\nEmail Preview:\n${text.substring(
      0,
      200
    )}...`;
  });
}

// When the analyze button is clicked
document.getElementById("analyze").addEventListener("click", () => {
  // Get the currently active tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    // Check if we're on Gmail
    if (!tabs[0].url.includes("mail.google.com")) {
      document.getElementById("output").textContent =
        "Error: Please open Gmail (mail.google.com) and select an email first.";
      return;
    }

    // Try to send message to content script
    sendMessageToContentScript(tabs[0].id);
  });
});
