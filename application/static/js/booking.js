var baseURL = window.location.origin;
var bookingAttraction;

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
                document.getElementById('no-booking').style.visibility = 'visible';
                return
            }
            // let data = result['data'];
            bookingAttraction = result['data'];
            document.getElementById('booking-img').getElementsByTagName('img')[0].src = bookingAttraction['attraction']['image'];
            document.getElementById('booking-info-title').getElementsByTagName('span')[0].innerText = bookingAttraction['attraction']['name'];
            document.getElementById('booking-info-date').getElementsByTagName('span')[0].innerText = bookingAttraction['date'];

            let bookingTime = '';
            if (bookingAttraction['time'] == 'afternoon') {
                bookingTime = '下午 2 點到下午 4 點';
            } else {
                bookingTime = '早上 9 點到早上 11 點';
            }

            document.getElementById('booking-wrapper').style.visibility = 'visible';
            document.getElementById('contact-wrapper').style.visibility = 'visible';
            document.getElementById('payment-wrapper').style.visibility = 'visible';
            document.getElementById('booking-confirm').style.visibility = 'visible';
            document.querySelectorAll('hr').forEach(element => {
                element.style.visibility = 'visible'
            });
            document.getElementById('booking-info-time').getElementsByTagName('span')[0].innerText = bookingTime;
            document.getElementById('booking-info-price').getElementsByTagName('span')[0].innerText = bookingAttraction['price'];
            document.getElementById('booking-info-address').getElementsByTagName('span')[0].innerText = bookingAttraction['attraction']['address'];
            document.getElementById('booking-total-amount').getElementsByTagName('span')[0].innerText = bookingAttraction['price'];
        })
        .catch(err => console.log(err));
}

window.addEventListener("load", function (event) {
    identifyAuth()
        .then((data) => {
            if (Object.keys(data['data']).length === 0) {
                window.location.href = `${baseURL}`;
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


const APP_ID = 127003
const APP_KEY = 'app_9LZBTXmkHD2wONL7PgjzIVpdIQGYEABIoky5LZjvLzlqIG8kkRf7ImnRBsOM'
TPDirect.setupSDK(APP_ID, APP_KEY, "sandbox")
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'CVV'
    }
}

TPDirect.card.setup({

    fields: fields,
    styles: {
        'input': {
            'color': 'gray',
            'font-size': '16px'
        },
        'input.ccv': {
            // 'font-size': '16px'
        },
        'input.expiration-date': {
            // 'font-size': '16px'
        },
        'input.card-number': {
            // 'font-size': '16px'
        },
        ':focus': {
            //'color': 'black'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})

document.getElementById('booking-submit').addEventListener('click', function (event) {
    event.preventDefault()

    TPDirect.card.getPrime((result) => {
        user_name = document.getElementById('contact-name').value;
        user_email = document.getElementById('contact-email').value;
        user_phone = document.getElementById('contact-phone').value;
        if (user_name == '' | user_email == '' | user_phone == '') {
            alert('所有欄位均為必填');
            return
        }
        if (result.status !== 0) {
            alert('信用卡資訊錯誤')
            return
        }

        let data = {
            "prime": result.card.prime,
            "order": {
                "price": bookingAttraction['price'],
                "trip": {
                    "attraction": {
                        "id": bookingAttraction['attraction']['id'],
                        "name": bookingAttraction['attraction']['name'],
                        "address": bookingAttraction['attraction']['address'],
                        "image": bookingAttraction['attraction']['image']
                    },
                    "date": bookingAttraction['date'],
                    "time": bookingAttraction['time']
                },
                "contact": {
                    "name": user_name,
                    "email": user_email,
                    "phone": user_phone
                }
            }
        }

        fetch(`${baseURL}/api/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .then((data) => {
                window.location.href = `${baseURL}/thankyou/${data['data']['number']}`
            })
            .catch(err => console.log(err));

    })
})