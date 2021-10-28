/// ==============================================
// EVENT LISTENERS
/// ==============================================

/**
 * Handle Accept/Reject Button Click events on the Request Column Side
 * @param {number} id The ID of the element 
 * @param {Node} element The element that the event acted on
 * @param {boolean} accept Whether or not the accept button was pressed or not
 * @param {String} type Should be between {"superUser", "admin", "restaurant"}
 * @returns 
 */
async function handleRequestEvent(id, element, accept, type) {
    // Because needed to append "{type}-" to get a unique id, need to just get the ID
    id = id.split("-").pop();

    var response = null;

    switch(type) {
      case "superUser":
        response = await handleSuperUserRequest(id, accept);
        break;
      case "admin":
        response = await handleAdminRequest(id, accept);
        break;
      case "restaurant":
        response = await handleRestaurantRequest(id, accept);
        break;
    }


    // Get the Request Card that this button is in: this -> .accept-btns -> .request-description-section -> .request-card
    elementToDelete = element.parentElement.parentElement.parentElement;

    return renderAlertMessage(response, elementToDelete);
}



/// ==============================================
// COMMUNICATING WITH THE BACKEND API
/// ==============================================

/**
 * Sends an Accept or Reject Request to the Backend to handle the Super User Account Request
 * @param {number} superUserID The Super User ID that corresponds to the Super User Account that needs to be approved
 * @param {boolean} accept Send accept request to backend or reject request
 * @returns JSON data structure with keys ("status", "message")
 */
async function handleSuperUserRequest(superUserID, accept) {
    
    // Make request to backend to accept/reject Super User with superUserID
    const response = await fetch(`/super-user-tools/super-user-requests/${accept ? "accept" : "reject"}/${superUserID}`).then(res => res.json());

    return response;
}

/**
 * Sends an Accept or Reject Request to the Backend to handle the Admin Account Request
 * @param {number} adminID The Admin ID that corresponds to the Admin Account that needs to be approved
 * @param {boolean} accept Send accept request to backend or reject request
 * @returns JSON data structure with keys ("status", "message")
 */
async function handleAdminRequest(adminID, accept) {
  // Make request to backend to accept/reject Admin with adminID
  const response = await fetch(`/super-user-tools/admin-requests/${accept ? "accept" : "reject"}/${adminID}`).then(res => res.json());

  return response;
}

/**
 * Sends an Accept or Reject Request to the Backend to handle the Restaurant Request
 * @param {number} restaurantRequestID The Restaurant Request ID that corresponds to the Restaurant Request that needs to be approved
 * @param {boolean} accept Send accept request to backend or reject request
 * @returns JSON data structure with keys ("status", "message")
 */
async function handleRestaurantRequest(restaurantRequestID, accept) {
  console.log(`/super-user-tools/restaurant-requests/${accept ? "accept" : "reject"}/${restaurantRequestID}`)
  // Make request to backend to accept/reject Restaurant Request with restaurantRequestID
  const response = await fetch(`/super-user-tools/restaurant-requests/${accept ? "accept" : "reject"}/${restaurantRequestID}`).then(res => res.json());

  return response;
}



/// ==============================================
// DYNAMIC RENDERING FUNCTIONS
/// ==============================================

/**
 * Renders an alert message at the top of the page with the message given from the backend. Also deletes a DOM element.
 * @param {JSON} response The JSON response returned from the backend, should have a "status" and "message" key
 * @param {Node} element An element that you want to be deleted from the DOM (Input "null" if you do not want a DOM element to be deleted)
 */
function renderAlertMessage(response, element) {
    console.log(response)

    // Build HTML to render Alert Message
    var alertHTML = `
    <div class="container-fluid p-0">
      <div class="alert ${response.status === "success" ? "alert-success" : "alert-danger" } alert-dismissible" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
        ${response.message}
      </div>
    </div>
    `;

    // Append message to the messages container
    document.querySelector("#alert-messages-container").insertAdjacentHTML('afterbegin', alertHTML);

    // Delete element if given and the response.status is a success
    if(response.status && element) {
      element.remove();
    }
}