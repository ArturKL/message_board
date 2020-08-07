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
            posts_box.append(render_post(post));
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

function edit_post(post) {
    let post_div = document.getElementById(`post${post.id}`);
    
    const csrftoken = Cookies.get('csrftoken');
    let form = document.createElement('form');
    form.innerHTML = `<h5><strong>Edit Post</strong></h5>
                      <textarea name="body" rows="3" maxlength="300" id="form-body">${post.body}</textarea><br>
                      <input type="submit" value="Save" class="btn btn-primary" id="submit">`;
    form.onsubmit = () => {
        let data = new FormData(form);
        console.log(JSON.stringify({"body": data.get("body")}))
        fetch(`edit/${post.id}`, {
            method: "PUT",
            body: JSON.stringify({"body": data.get("body")}),
            headers: { "X-CSRFToken": csrftoken },
        })
        .then(response => response.status)
        .then(status => {
            if (status === 204) {
                post.body = data.get("body");
                post_div.parentNode.replaceChild(render_post(post), post_div);
            }
        })
        return false;
    };
    post_div.innerHTML = "";
    post_div.append(form)
}

function render_post(post) {
    let post_div = document.createElement('div');
    post_div.classList.add('post');
    post_div.id = `post${post.id}`;
    post_div.innerHTML = `<h5><strong><a href="/u/${post.author}">${post.author}</a></strong></h5>`;

    // Post body
    let post_body = document.createElement('span');
    post_body.classList.add('post-body');
    post_body.innerText = post.body;

    // Edit button
    post_div.append(post_body);
    if (current_user == post.author) {
        let edit = document.createElement('a');
        edit.href = "javascript:void(0)";
        edit.classList.add("edit");
        edit.innerHTML = "Edit";
        edit.addEventListener('click', () => {
            fetch(`posts/${post.id}`)
            .then(response => response.json())
            .then(post => {
                edit_post(post);
            });
        });
        post_div.append(document.createElement('br'), edit); 
    }

    // Timestamp
    let date = document.createElement('span');
    date.classList.add('text-muted');
    date.innerHTML = post.timestamp;
    post_div.append(date)

    // Likes
    let likes = document.createElement('span');
    likes.innerHTML = `Likes: ${post.liked}`;
    post_div.append(likes);

    return post_div;
}