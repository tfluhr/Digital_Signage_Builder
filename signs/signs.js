//Script to generate current time and date

// create a function to update the date and time
function updateDateTime() {
    // create a new `Date` object
    const now = new Date();

    // get the current date and time as a string
    const currentDate = now.toLocaleString(
        'en-us', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
           // timeZone: 'cst'
        }
    );

    const currentTime = now.toLocaleString(
        'en-us', {
            hour: 'numeric',
            minute: '2-digit'
        }
    );

    // update the `textContent` property of the `span` element with the `id` of `datetime`
    document.querySelector('#datetime').textContent = currentDate + '        ' + currentTime;
}

// call the `updateDateTime` function every second
setInterval(updateDateTime, 1000);
