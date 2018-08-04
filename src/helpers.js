
export const range = (max) => Array(max).fill(null);
export const randomInteger = (max = 1) => Math.floor(Math.random()*max);
const randomHex = () => randomInteger(256).toString(16)
export const randomColor = () => '#'+range(3).map(randomHex).join('')

export function createElement(tag, data, options = {}) {
    const el = document.createElement(tag)
    el.innerText = data
   
    return Object.entries(options).reduce(
        (element, [field, value]) => {
            element.setAttribute(field, value)
            return element;
        }, el);
}