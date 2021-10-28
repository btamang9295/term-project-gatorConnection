/**
 * After the window loads, make a fetch request to backend to see if user
 * has any unread notifications and update the notification indicator
 * depending on if the user has any unread notifications or not
 */
window.onload = async () => {
    const hasNotifications = await checkNotifications();
    
    renderNotificationIndicator(hasNotifications)
  };




/**
 * Async Function that makes fetch request to backend.
 */
async function checkNotifications() {
    const response = await fetch('/notifications/user')
        .then((res) => res.json());

    return response.hasNotifications;
}


function renderNotificationIndicator(hasNotifications) {
    notificationIndicator = document.querySelector('#notification-indicator')

    if(hasNotifications) {
    notificationIndicator.classList.remove("hidden");
    } else {
    notificationIndicator.classList.add("hidden");
    }
}