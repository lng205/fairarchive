// Function to update all timestamps on the page
function updateTimestamps() {
    // Find all elements with the 'data-timestamp' attribute
    const timestampElements = document.querySelectorAll('[data-timestamp]');

    function formatTime(dbTimestamp) {
        // Calculate the time difference in seconds
        const delta = Math.floor(Date.now() / 1000) - dbTimestamp;
    
        // Convert the time delta to a human-readable format
        const minutes = Math.floor(delta / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
    
        if (days > 0) {
            return `${days}天前`;
        } else if (hours > 0) {
            return `${hours}小时前`;
        } else if (minutes > 0) {
            return `${minutes}分钟前`;
        } else {
            return "刚刚";
        }
    }

    timestampElements.forEach(element => {
        // Get the timestamp from the data attribute
        const rawTimestamp = parseInt(element.getAttribute('data-timestamp'));

        // Format it and update the element's text
        element.textContent = formatTime(rawTimestamp);
    });
}


// Function to convert numbers to shorthand notation
function convertStats() {
    // Get all elements with the class 'float-end'
    var stats = document.querySelectorAll('.stats');
  
    function convertToShorthand(num) {
      if (num >= 1000 && num < 10000) {
        return (num / 1000).toFixed(1) + 'k'; // For thousands
      } else if (num >= 10000 && num < 1000000) {
        return (num / 1000).toFixed(0) + 'k'; // For tens of thousands
      }
      else if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'; // For millions
      } else {
        return num.toString(); // For numbers less than 1000
      }
    }

    // Loop through each element
    stats.forEach(function(stat) {
      var text = stat.innerText; // Get the text of the element
      var number = parseInt(text, 10); // Convert the text to a number
      var shorthand = convertToShorthand(number); // Convert number to shorthand notation
      stat.innerText = shorthand; // Update the element's text with shorthand notation
    });
  }


// Run the update function when the page loads
document.addEventListener('DOMContentLoaded', updateTimestamps);
document.addEventListener('DOMContentLoaded', convertStats);