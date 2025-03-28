let selectedEntry = null;
let highlightedText = "";
const entryDetailsPopup = document.getElementById("entry-details-popup");
const popupEntryDate = document.getElementById("popup-entry-date");
const popupEntryAmount = document.getElementById("popup-entry-amount");
const popupEntryDescription = document.getElementById(
  "popup-entry-description"
);
const categorySelect = document.getElementById("popup-category-select");
const uncategorizedEntriesList = document.getElementById(
  "uncategorized-entries-list"
);
const noEntriesMessage = document.getElementById("no-entries-message");
// --- Dummy Data (Replace with actual data fetching) ---
var uncategorizedEntriesData = [
  {
    id: "entry1",
    date: "2025-03-15",
    description: "Coffee at Starbucks",
    amount: "$5.50",
  },
  {
    id: "entry2",
    date: "2025-03-16",
    description: "Grocery shopping at the market for dinner",
    amount: "$45.20",
  },
  {
    id: "entry3",
    date: "2025-03-17",
    description: "Payment from Freelance Project - Website Design",
    amount: "$500.00",
  },
  // ... more entries
];

var categoriesData = [
  { id: 0, name: "category1" },
  { id: 1, name: "category2" },
  // ... more categories
];
// --- End of Dummy Data ---

// Function to load uncategorized entries into the list
function loadUncategorizedEntries() {
  fetch("/UncategorizedEntries", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      uncategorizedEntriesData = data;
      console.log(uncategorizedEntriesData);
      uncategorizedEntriesList.innerHTML = "";
      if (uncategorizedEntriesData.length === 0) {
        noEntriesMessage.style.display = "block";
        return;
      }
      noEntriesMessage.style.display = "none";
      uncategorizedEntriesData.forEach((entry) => {
        const entryDiv = document.createElement("div");
        entryDiv.classList.add("entry-item");
        entryDiv.dataset.entry = JSON.stringify(entry);
        entryDiv.innerHTML = `<span>Date: ${entry.date}</span> - <span>Description: ${entry.description}</span>`;
        entryDiv.addEventListener("click", () => showEntryDetails(entry));
        uncategorizedEntriesList.appendChild(entryDiv);
      });
    });
}

// Function to load categories into the select dropdown
function loadCategories() {
  fetch("/categories", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      categoriesData = data;
      categoriesData.forEach((category) => {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;
        categorySelect.appendChild(option);
      });
    });
}

// Function to show the entry details pop-up
function showEntryDetails(entry) {
  selectedEntry = entry;
  popupEntryDate.innerText = `Date: ${entry.date}`;
  popupEntryAmount.innerText = `Amount: ${entry.amount}`;
  popupEntryDescription.innerText = entry.description;
  highlightedText = ""; // Reset highlight
  entryDetailsPopup.style.display = "block";
}

// Function to close the pop-up
function closePopup() {
  entryDetailsPopup.style.display = "none";
  selectedEntry = null;
}

// Function to handle text highlighting
function highlightText() {
  const selection = window.getSelection();
  highlightedText = selection.toString().trim();
  if (highlightedText) {
    console.log("Highlighted text:", highlightedText);
    // In a real application, you might want to visually highlight the selected text in the DOM.
  }
}

// Function to add the highlighted text as a keyword
function addHighlightedKeyword() {
  if (!selectedEntry) {
    alert("No entry selected.");
    return;
  }
  const selectedCategory = categorySelect.value;
  if (selectedCategory && highlightedText) {
    addedKeyword = {
      keyword: highlightedText,
      category: selectedCategory,
    };
    console.log(
      `Adding keyword "${highlightedText}" to category "${selectedCategory}" for entry ID: ${selectedEntry.id}`
    );
    // --- IMPLEMENT CONNECTION TO BACKEND HERE ---
    // Make an API call to update the keywords for the selected category.
    // You would likely send the selectedCategory and highlightedText.
    // After successful update, you might want to remove the entry from the list
    // or mark it as categorized.
    // Example API call (conceptual):
    fetch('/addKeywords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(addedKeyword),
    })
    .then(response => {
        // Update UI accordingly (e.g., remove entry)
        const index = uncategorizedEntriesData.findIndex(entry => entry.id === selectedEntry.id);
        if (index > -1) {
            uncategorizedEntriesData.splice(index, 1);
            loadUncategorizedEntries();
        }
        closePopup();
    })
    .catch(error => console.error('Error adding keyword:', error));

  } else {
    alert("Please select a category and highlight text in the description.");
  }
}

// Function to download the updated keywords file
function downloadKeywords() {
  console.log("Added keywords:", addedKeyword);
  console.log("Download updated keywords file (Implementation needed)");
  // --- IMPLEMENT CONNECTION TO BACKEND HERE ---
  // Make an API call to get the updated keywords file content.
  // Then trigger a download in the browser.
  // Example API call (conceptual):
  // fetch('/api/keywords/download')
  //     .then(response => response.blob())
  //     .then(blob => {
  //         const url = window.URL.createObjectURL(blob);
  //         const a = document.createElement('a');
  //         a.href = url;
  //         a.download = 'updated_keywords.yaml';
  //         document.body.appendChild(a);
  //         a.click();
  //         document.body.removeChild(a);
  //         window.URL.revokeObjectURL(url);
  //     })
  //     .catch(error => console.error('Error downloading keywords:', error));
  alert("Download functionality not yet implemented.");
}

// Load initial data
loadUncategorizedEntries();
loadCategories();

// Close the pop-up if the user clicks outside of it
window.onclick = function (event) {
  if (event.target == entryDetailsPopup) {
    closePopup();
  }
};
