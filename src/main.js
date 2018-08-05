// importing named exports we use brackets
import { createElement } from './helpers.js';

// when importing 'default' exports, use below syntax
import API from './api.js';

const api  = new API();

// we can use this single api request multiple times
const feed = api.getFeed();

feed
.then(posts => {
    posts.reduce((parent, post) => {
        const img = createElement('img', null, 
            { src: 'images/'+post.thumbnail, alt: post.meta.description_text, class: 'post-thumb' });
        parent.appendChild(img);
        return parent;

    }, document.getElementById('feed'));
});

feed
.then(posts => {
    posts.reduce((parent, post) => {
        const section = createElement('section', null, { class: 'post' });
        section.appendChild(createElement('h2', post.meta.author, { class: 'post-title' }))
        section.appendChild(createElement('img', null, 
        { src: 'images/'+post.src, alt: post.meta.description_text, class: 'post-image' }))
        parent.appendChild(section)
        return parent;
    }, document.getElementById('large-feed'))
    posts.map(console.log);
});