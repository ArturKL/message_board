let page = 1;

document.addEventListener('DOMContentLoaded', () => {
    const form_body = document.getElementById('form-body');
    const submit = document.getElementById('submit');
    submit.disabled = true;
    form_body.onkeyup = () => {
        if (form_body.value.length === 0) {
            submit.disabled = true;
        }
        else {
            submit.disabled = false;
        }
    }
    address();
}); 

function posts(page, user) {
    const posts_box = document.getElementById('posts')
    let num_pages;
    posts_box.innerHTML = '';
    fetch(`/posts/${page}/${user}`)
    .then(response => response.json())
    .then(posts => {
        for (let post of posts) {
            if (post.num_pages !== undefined) {
                num_pages = post.num_pages;
                break;
            }
            const post_div = document.createElement('div');
            post_div.classList.add('post');
            post_div.innerHTML = `<h5><strong><a href="/u/${post.author}">${post.author}</a></strong></h5>`;
            post_body = document.createElement('span');
            post_body.classList.add('post-body');
            post_body.innerHTML = post.body;
            post_div.append(post_body);
            post_div.innerHTML += `<span class="text-muted">${post.timestamp}</span>
                                   Likes: ${post.liked}`;
            posts_box.append(post_div);
        };
        if (posts.length === 1) {
            posts_box.innerHTML = '<h3>No posts</h3>';
        }
        else if (num_pages > 1) {
            pagination_btns(num_pages);
        }
    });
}

function pagination_btns(num_pages) {
    const buttons =  document.createElement('nav');
    let prev_disabled, next_disabled;
    if (page > 1) {
        prev_disabled = '';
    }
    else {
        prev_disabled = 'disabled';
    }
    if (page === num_pages) {
        next_disabled = 'disabled';
    }
    else {
        next_disabled = '';
    }
    buttons.innerHTML = `<ul class="pagination justify-content-center">
                            <li class="page-item ${prev_disabled}" id="previous">
                                <a class="page-link" href="#${page-1}" aria-disabled="true">Previous</a>
                            </li>
                            <li class="page-item ${next_disabled}" id="next">
                                <a class="page-link" href="#${page+1}">Next</a>
                            </li>
                        </ul>`
    document.getElementById('posts').append(buttons);
    const next = document.getElementById('next');
    const previous = document.getElementById('previous');
    function next_event() {
        if (page < num_pages) {
            page ++;
            address();
        }
    }
    function previous_event() {
        if (page > 1) {
            page --;
            address();
        }
    }
    next.addEventListener('click', next_event);
    previous.addEventListener('click', previous_event);
}

function address() {
    const path = window.location.pathname;
    if (path === '/') {
        posts(page, '*');
    }
    else if (path === '/following') {
        posts(page, '**');
    }
    else if (path.match(/u\//)) {
        posts(page, path.slice(3));
    }
}
