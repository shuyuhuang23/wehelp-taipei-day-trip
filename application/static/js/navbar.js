var baseURL = window.location.origin;

function identifyAuth(callback) {
    return fetch(`${baseURL}/api/user/auth`)
        .then((response) => response.json())
        .then((data) => {
            let navbarDiv = document.getElementById('navbar-login');
            if ('email' in data['data']) {
                navbarDiv.innerText = '登出系統';
            } else {
                navbarDiv.innerText = '登入/註冊';
            }
            return data
        })
        .catch(err => console.log(err));
};

function resetForm() {

    document.getElementById('login-container').style.display = 'none';
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('login-msg').innerText = '';

    document.getElementById('register-container').style.display = 'none';
    document.getElementById('register-name').value = '';
    document.getElementById('register-email').value = '';
    document.getElementById('register-password').value = '';
    document.getElementById('register-msg').innerText = '';
};

document.getElementById('navbar-booking').addEventListener('click', function(event) {
    identifyAuth().then((data) => {
        if ('email' in data['data']) {
            window.location.href = `${baseURL}/booking`;
        } else {
            let loginDiv = document.getElementById('login-container');
            loginDiv.style.display = 'block';
        }
    })
})

document.getElementById('navbar-login').addEventListener('click', function (event) {
    identifyAuth().then((data) => {
        if ('email' in data['data']) {
            fetch(`${baseURL}/api/user/auth`, { method: 'DELETE' })
                .then((response) => window.location.reload())
                .catch(err => console.log(err));
        } else {
            let loginDiv = document.getElementById('login-container');
            loginDiv.style.display = 'block';
        }
    })

});

document.getElementById('login-close').addEventListener('click', resetForm);

document.getElementById('register-close').addEventListener('click', resetForm);

document.getElementById('login-submit').addEventListener('click', function (event) {
    let email = document.getElementById('login-email').value;
    let password = document.getElementById('login-password').value;

    let validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if (email === '' || password === '') {
        document.getElementById('login-msg').innerText = '所有欄位都是必填欄位';
        return;
    }

    if (email.match(validRegex) === null) {
        document.getElementById('login-msg').innerText = '電子信箱格式錯誤';
        return;
    }

    let data = { email, password };

    fetch(`${baseURL}/api/user/auth`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['error']) {
                document.getElementById('login-msg').innerText = data['message'];
            } else {
                document.getElementById('login-msg').innerText = '';
                window.location.reload();
            }
        })
        .catch(err => console.log(err));
});

document.getElementById('login-register').addEventListener('click', function (event) {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'block';
});

document.getElementById('register-login').addEventListener('click', function (event) {
    document.getElementById('register-container').style.display = 'none';
    document.getElementById('login-container').style.display = 'block';
});

document.getElementById('register-submit').addEventListener('click', function (event) {
    let name = document.getElementById('register-name').value;
    let email = document.getElementById('register-email').value;
    let password = document.getElementById('register-password').value;

    let validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

    if (name === '' || email === '' || password === '') {
        document.getElementById('register-msg').innerText = '所有欄位都是必填欄位';
        return;
    }

    if (email.match(validRegex) === null) {
        document.getElementById('register-msg').innerText = '電子信箱格式錯誤';
        return;
    }

    let data = { name, email, password };

    fetch(`${baseURL}/api/user`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {

            if (data['error']) {
                document.getElementById('register-msg').innerText = data['message'];
            } else {
                document.getElementById('register-msg').innerText = '註冊成功';
            }
        })
        .catch(err => console.log(err));
});