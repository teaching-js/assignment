// change this when you integrate with the real API
const API_URL = 'http://127.0.0.1:8080/data'

const getJSON = (path, options) => 
    fetch(path, options).then(res => res.json());

/**
 * This is a sample class API which you may base your code on.
 */
export default class API {

    constructor(url = API_URL, credentials = {}) {
        this.url = url;
        this.credentials = credentials;
    } 

    makeAPIRequest(path) {
        return getJSON(`${this.url}/${path}`, this.credentials);
    }

    /**
     * @returns feed array in json format
     */
    getFeed() {
        return this.makeAPIRequest('feed.json');
    }

    /**
     * @returns auth'd user in json format
     */
    getMe() {
        return this.makeAPIRequest('me.json');
    }


}