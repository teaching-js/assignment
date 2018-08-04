// importing named exports we use brackets
import { range, createElement, randomColor } from './helpers.js';

// when importing 'default' exports, use below syntax
// import API from './api.js';

range(20).reduce((el) => {
    const p = createElement('p', 'hi', { title: 'text', class: 'post', style: `background-color: ${randomColor()}` });
    el.appendChild(p);
    return el;
}, document.querySelector('main'));

// API.doThing();