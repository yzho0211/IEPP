document.addEventListener('DOMContentLoaded', function() {
    var popupContainer = document.getElementById('popup-container');
    var popupButton = document.getElementById('popup-button');

    // Check if the popup has been shown before
    var popupShown = getCookie('popupShown');

    // If the popup has not been shown before, display it
    if (!popupShown) {
        popupContainer.style.display = 'block';
        // Set a cookie to indicate that the popup has been shown
        setCookie('popupShown', true, 1); // Expires in 1 days
    }

    // Close the popup when the popup button is clicked
    popupButton.addEventListener('click', function() {
        popupContainer.style.display = 'none';
    });

    // Include CSRF token in AJAX requests
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

// Function to set a cookie
function setCookie(name, value, days) {
    var expires = '';
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '')  + expires + '; path=/';
}

// Function to get a cookie
function getCookie(name) {
    var nameEQ = name + '=';
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }

    return null;
}
