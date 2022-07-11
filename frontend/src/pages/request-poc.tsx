import React from "react";

const authenticatedRequest = (url: string) => {
    fetch(url)
    .then(res => res.json())
    .then(text => console.log(text))
}

const RequestPOC = () => {
    return (
        <div>
            <h1>Authenticated Request POC</h1>
            <p>
                This is a POC for sending authenticated requests to the API. We consolidated the frontend and backend
                on a single ingress domain to get around CORS limitations that come with CorpSecure authentication in Kanopy.
            </p>

            <p>
                Click the button to send a request to the API. Check the console for the response. It should be a JSON object with the message "Hello World".
            </p>
            <button onClick={() => authenticatedRequest(`${process.env.GATSBY_API_URL}/hello`)}>Send authenticated request</button>
        </div>
    )
};

export default RequestPOC;