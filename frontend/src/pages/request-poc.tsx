import React from "react";

const unauthenticatedRequest = (url: string) => {
    fetch(url)
        .then(res => res.text())
        .then(text => console.log(text))
}

const authenticatedRequest = (url: string) => {
    fetch(url)
    .then(res => res.json())
    .then(text => console.log(text))
}

const RequestPOC = () => {
    return (
        <div>
            <h1>Request POC</h1>
            <p>
                This is a POC for sending authenticated requests to the API.
            </p>
            
            <h2>Without including cookies in request:</h2>
            <p>
                Click the button to send a request to the API without cookies. Check the console for the response. It should be raw HTML for the MongoDB corp sign in page.
            </p>
            <button onClick={() => unauthenticatedRequest("https://hapley-api.docs.staging.corp.mongodb.com/hello")}>Send unauthenticated request</button>

            <h2>With including cookies in request:</h2>
            <p>
                Click the button to send a request to the API with cookies. Check the console for the response. It should be a JSON object with the message "Hello World".
            </p>
            <button onClick={() => authenticatedRequest("http://localhost:8000/hello")}>Send authenticated request</button>  
        </div>
    )
};

export default RequestPOC;