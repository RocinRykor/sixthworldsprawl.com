class APIRequest {
    constructor(api_request) {
        this.endpoint_url = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/`;
        this.headers = {
            'Content-Type': 'application/json',
        };
        this.response = {};
        this.api_request = this.endpoint_url + api_request;
    }

    async get_request() {
        this.response = await fetch(this.api_request, {
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: this.headers,
            redirect: 'follow',
        });
        return this.response.json();
    }
}

// Frontend admin API endpoint implementation
async function portrait_search(portrait_id) {
    /*
     * Searches for portrait on the server.
     * keywords should be a json list of keywords to search for
     *
     * Returns a JSON dict containing the portrait
     */
    const api_request = `portrait/${portrait_id}`;
    const request = new APIRequest(api_request);
    return await request.get_request();
}

function openPortraitModal() {
    $('#characterPortraitModal').modal('show');
}

function setCharacterPortrait(portraitID) {
    portrait_search(portraitID).then((portrait) => {
        console.log(portraitID);

        //Add Selected portrait information to hidden form fields
        formPortraitID = $('#portrait_id');
        formPortraitID.val(portraitID);

        formPortraitFileName = $('#portrait_filename');
        formPortraitFileName.val(portrait.filename);

        // Show Selected Picture
        img_url = '../../../static/img/portraits/' + portrait.filename;
        $('#selectedCharacterPortrait').attr('src', img_url);

        //Hide
        $('#characterPortraitModal').modal('hide');
    });
}
