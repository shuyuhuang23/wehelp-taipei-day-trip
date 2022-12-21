var attractionId = document.URL.split('/')[document.URL.split('/').length - 1];
var baseURL = window.location.origin;

var slideIndex = 0;
var slideImages = [];

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

function showSlide(idx) {
    if (idx < 0) {
        return 0;
    }
    if (idx >= slideImages.length) {
        return slideImages.length - 1;
    }

    let imgDiv = document.getElementsByClassName('profile-slideshow-slide')[0];
    imgDiv.innerHTML = '';
    let img = document.createElement('img');
    img.src = slideImages[idx];
    imgDiv.appendChild(img);
    let slideshowCircle = document.getElementsByClassName('profile-slideshow-circle');
    for (let i = 0; i < slideshowCircle.length; i++) {
        if (i === idx) {
            slideshowCircle[i].className = 'profile-slideshow-circle selected';
        } else {
            slideshowCircle[i].className = 'profile-slideshow-circle';
        }

    }
    return idx
};

function showAttraction(callback) {

    return fetch(`${baseURL}/api/attraction/${attractionId}`)
        .then(res => res.json())
        .then(result => {
            let data = result['data'];

            slideImages = data['images'];

            let slideCircleDiv = document.getElementsByClassName('profile-slideshow-bottom')[0];
            for (let i = 0; i < slideImages.length; i++) {
                let circleDiv = document.createElement('div');
                circleDiv.className = 'profile-slideshow-circle';
                circleDiv.id = `image-${i}`;
                slideCircleDiv.appendChild(circleDiv);
            }

            slideIndex = showSlide(slideIndex);

            let nameDiv = document.getElementById('profile-content-title');
            nameDiv.innerText = data['name'];

            let detailDiv = document.getElementById('profile-content-detail');
            detailDiv.innerText = `${data['category']} at ${data['mrt']}`;

            let descDiv = document.getElementById('description');
            descDiv.innerText = data['description'];

            let locDiv = document.getElementById('location-content');
            locDiv.innerText = data['address'];

            let transDiv = document.getElementById('transportation-content');
            transDiv.innerText = data['transport'];

        })
        .then(() => {
            if (callback) {
                callback();
            };
        })
        .catch(err => console.log(err));
};

window.addEventListener("load", function (event) {
    let today = new Date();
    today = new Date(today.setDate(today.getDate() + 1)).toISOString().split('T')[0];
    document.getElementById("profile-content-date-input-box").setAttribute('min', today);

    identifyAuth()
        .then(() => {
            return showAttraction();
        })
});

document.getElementById('profile-slideshow-prev').addEventListener('click', function (event) {
    slideIndex = showSlide(slideIndex - 1);
});

document.getElementById('profile-slideshow-next').addEventListener('click', function (event) {
    slideIndex = showSlide(slideIndex + 1);
});

document.getElementById('profile-content-btn').addEventListener('click', function (event) {
    identifyAuth().then((user) => {
        // not log in
        if (Object.keys(user['data']).length === 0) {
            let loginDiv = document.getElementById('login-container');
            loginDiv.style.display = 'block';
            return
        }

        let date = document.getElementById('profile-content-date-input-box').value;
        let time = Array.from(document.getElementsByName("time")).find(r => r.checked).value
        let price = document.getElementById('profile-content-tour').getElementsByTagName('span')[0].innerText;

        if (date === '') {
            document.getElementById('profile-content-msg').innerText = '日期為必填欄位';
            return
        }

        let currentDate = new Date();
        let bookingDate = new Date(date);

        if (currentDate >=  bookingDate) {
            document.getElementById('profile-content-msg').innerText = '僅開放明天之後的日期';
            return 
        }

        let data = {
            attractionId,
            date,
            time,
            price
        }
        
        fetch(`${baseURL}/api/booking`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                window.location.href = `${baseURL}/booking`;
            })
            .catch(err => console.log(err));

    })
})