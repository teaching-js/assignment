// importing named exports we use brackets
import { createElement } from './helpers.js';

// when importing 'default' exports, use below syntax
import API from './api.js';

const api  = new API();

api.getFeed()
.then(posts => {
    posts.reduce((parent, post) => {
        const img = createElement('img', null, 
            { src: 'images/'+post.thumbnail, alt: post.meta.description_text, class: 'post' });
        parent.appendChild(img);
        return parent;

    }, document.getElementById('feed'));
});