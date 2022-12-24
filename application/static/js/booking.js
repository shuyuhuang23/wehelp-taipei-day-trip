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

function loadBooking() {
    return fetch(`${baseURL}/api/booking`)
        .then((response) => response.json())
        .then((result) => {
            if (Object.keys(result['data']).length === 0) {
                document.getElementById('headline').innerText = '沒有任何預約';
                document.getElementById('booking-wrapper').style.display = 'none';
                document.getElementById('contact-wrapper').style.display = 'none';
                document.getElementById('payment-wrapper').style.display = 'none';
                document.getElementById('booking-confirm').style.display = 'none';
                document.querySelectorAll('hr').forEach(element => {
                    console.log(element)
                    element.style.display = 'none'
                });
                return
            }
            let data = result['data'];
            console.log(data)
            document.getElementById('booking-img').getElementsByTagName('img')[0].src = data['attraction']['image'];
            document.getElementById('booking-info-title').getElementsByTagName('span')[0].innerText = data['attraction']['name'];
            document.getElementById('booking-info-date').getElementsByTagName('span')[0].innerText = data['date'];

            let bookingTime = '';
            if (data['time'] == 'afternoon') {
                bookingTime = '下午 2 點到下午 4 點';
            } else {
                bookingTime = '早上 9 點到早上 11 點';
            }
            document.getElementById('booking-info-time').getElementsByTagName('span')[0].innerText = bookingTime;
            document.getElementById('booking-info-price').getElementsByTagName('span')[0].innerText = data['price'];
            document.getElementById('booking-info-address').getElementsByTagName('span')[0].innerText = data['attraction']['address'];
            document.getElementById('booking-total-amount').getElementsByTagName('span')[0].innerText = data['price'];
        })
        .catch(err => console.log(err));
}

window.addEventListener("load", function (event) {
    identifyAuth()
        .then((data) => {
            if (Object.keys(data['data']).length === 0) {
                window.location.href = `${baseURL}`;
                // let loginDiv = document.getElementById('login-container');
                // loginDiv.style.display = 'block';
            }

            document.getElementById('headline').getElementsByTagName('span')[0].innerText = data['data']['name'];

            document.getElementById('contact-name').value = data['data']['name'];
            document.getElementById('contact-email').value = data['data']['email'];
            return loadBooking();
        })
});

document.getElementById('booking-delete').addEventListener('click', function (event) {
    fetch(`${baseURL}/api/booking`, { method: 'DELETE' })
        .then((response) => response.json())
        .then(() => {
            window.location.reload();
        })
        .catch(err => console.log(err));
})