
const getJSON = (path, options) => 
    fetch(path, options).then(res => res.json());

const api = {
    getJSON
}

export default api;