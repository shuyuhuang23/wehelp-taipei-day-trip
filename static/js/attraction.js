var attractionId = document.URL.split('/')[document.URL.split('/').length - 1];
var baseURL = window.location.origin;

var slideIndex = 0;
var slideImages = [];

var apiURL = `${baseURL}/api/attraction/${attractionId}`;
fetch(apiURL)
        .then(res => res.json())
        .then(result => {
            let data = result['data'];

            // let profileDiv = document.getElementById('profile-img');
            // let img = document.createElement('img');
            // img.src = data['images'][0];
            // profileDiv.appendChild(img);
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

            // result['images'][0]

        })
        .then(() => {
            if (callback) {
                callback();
            };
        })
        .catch(err => console.log(err));

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
}

document.getElementById('profile-slideshow-prev').addEventListener('click', function(event) {
    console.log(event.target)
    slideIndex = showSlide(slideIndex - 1);
})

document.getElementById('profile-slideshow-next').addEventListener('click', function(event) {
    console.log(event.target)
    slideIndex = showSlide(slideIndex + 1);
})