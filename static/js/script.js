document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData);

    const response = await fetch('/login', {
        method: 'POST',
        body: data,
        credentials: 'include'
    });

    if (response.ok) {
        console.log('response.ok');
        window.location.href = '/get_all_product_params';
    } else {
        console.log('error');
    }
});

function searchParams() {
    let searchValue = document.getElementById('searchInput').value;
    const search = encodeURIComponent(searchValue);
    getAllProductParams(0, 6, search);
}

function searchUsers() {
    let searchValue = document.getElementById('searchUserInput').value;
    const search = encodeURIComponent(searchValue);
    console.log(searchValue);
    getAllUsers(0, 6, search);
}




async function getAllProductParams(skip, limit, search) {
    console.log(skip, limit)
    let url = `/get_all_product_params?n=${skip}&m=${limit}`;

    if (search && search != 'None') {
        url += `&search=${encodeURIComponent(search)}`;
    }

    const response = await fetch(url, {
        method: 'GET',
        credentials: 'include'
    });

    if (response.ok) {
        const data = await response.text();
        document.body.innerHTML = data;
    } else if (response.status === 401) {
        window.location.href = '/login';
    } else {
        alert(response.json());
    }
}

async function getAllUsers(skip, limit, search) {
    console.log(skip, limit)
    let url = `/get_users?n=${skip}&m=${limit}`;

    if (search && search != 'None') {
        url += `&search=${encodeURIComponent(search)}`;
    }

    const response = await fetch(url, {
        method: 'GET',
        credentials: 'include'
    });

    if (response.ok) {
        const data = await response.text();
        document.body.innerHTML = data;
    } else if (response.status === 401) {
        window.location.href = '/login';
    } else {
        alert(response.json());
    }
}


async function previous_btn(skip, limit, search) {
    skip = Number(skip);
    limit = Number(limit);
    skip = Math.max(0, skip - limit);
    getAllProductParams(skip, limit, search);
}

async function next_btn(skip, limit, search, isLast) {
    skip = Number(skip);
    limit = Number(limit);
    console.log('next_btn');
    if (isLast === true){
        console.log('isLast: ' + skip);
        getAllProductParams(skip, limit, search);
    }
    else {
        skip += limit;
        console.log('isntLast: ' + skip);
        getAllProductParams(skip, limit, search);
    }
}

async function previous_users_btn(skip, limit, search) {
    skip = Number(skip);
    limit = Number(limit);
    skip = Math.max(0, skip - limit);
    getAllUsers(skip, limit, search);
}

async function next_users_btn(skip, limit, search, isLast) {
    skip = Number(skip);
    limit = Number(limit);
    console.log('next_btn');
    if (isLast === true){
        console.log('isLast: ' + skip);
        getAllUsers(skip, limit, search);
    }
    else {
        skip += limit;
        console.log('isntLast: ' + skip);
        getAllUsers(skip, limit, search);
    }
}


async function createUser() {
    const response = await fetch('/create_user', {
        method: 'GET',
        credentials: 'include' 
    });
    if (response.redirected) {
        window.location.href = response.url;
    }
    else if(response.ok) {
        const data = await response.text();
        document.body.innerHTML = data;
    } else {
        window.location.href = '/login';
    }
}

function login(){
    window.location.href = '/login';
}


async function delete_user(userId) {
    console.log(userId);
    const response = await fetch('/delete_user', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId }),
    });

    if(response.ok) {
        window.location.href = '/get_users';
    }
}

async function delete_product_param(paramId) {
    console.log(paramId);
    const response = await fetch('/delete_product_param', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ param_id: paramId }),
    });

    if(response.ok) {
        window.location.href = '/get_all_product_params';
    }
}


async function productParamsBtn(){
    window.location.href = '/get_all_product_params';
}

async function usersBtn(){
    window.location.href = '/get_users';
}

