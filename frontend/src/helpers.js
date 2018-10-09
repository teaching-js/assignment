export const range = (max) => Array(max).fill(null);
export const randomInteger = (max = 1) => Math.floor(Math.random()*max);
const randomHex = () => randomInteger(256).toString(16)
export const randomColor = () => '#'+range(3).map(randomHex).join('')

// you don't have to use this but it may or may not simplify element creation
export function createElement(tag, data, options = {}) {
    const el = document.createElement(tag)
    el.textContent = data
   
    // sets the attributes in the options object to the element
    return Object.entries(options).reduce(
        (element, [field, value]) => {
            element.setAttribute(field, value)
            return element;
        }, el);
}

// Given an input element of type=file, grab the data uploaded for use
export function postImage(event) {
    const [ file ] = event.target.files;

    const validFileTypes = [ 'image/jpeg', 'image/png', 'image/jpg' ]
    const valid = validFileTypes.find(type => type === file.type);

    // bad data, let's walk away
    if (!valid)
        return false;
    
    // if we get here we have a valid image
    const reader = new FileReader();
    
    reader.onload = (e) => {
        // do something with the data result
        const dataURL = e.target.result;
        const image = createElement('img', null, { src: dataURL });
        document.body.appendChild(image);
    };

    // this returns a base64 image
    reader.readAsDataURL(file);
}