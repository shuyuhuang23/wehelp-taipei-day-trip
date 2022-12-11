var isLoading = false;
var nextPage = 0;
var keyword = '';

function identifyAuth(callback) {
    return fetch('api/user/auth')
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

function loadAttractions(page, keyword, callback) {

    if (page === null) {
        return;
    }

    isLoading = true;

    let url = `api/attractions?page=${page}`
    if (keyword !== '') {
        url = `${url}&keyword=${keyword}`
    }

    return fetch(url)
        .then(res => res.json())
        .then(result => {
            var anchorDiv = document.getElementById('attractions-grp');

            if (page === 0 && result['data'].length === 0) {
                anchorDiv.textContent = '查無景點';
            }

            for (let i = 0; i < result['data'].length; i++) {
                let element = result['data'][i];

                let linkTag = document.createElement('a');
                linkTag.setAttribute('href', `/attraction/${element['id']}`);

                let attractionDiv = document.createElement("div");
                attractionDiv.className = 'attraction';

                let img = document.createElement('img');
                img.src = element['images'][0];

                let nameDiv = document.createElement('div');
                nameDiv.className = 'attraction-name';
                let nameTextDiv = document.createElement('div');
                nameTextDiv.textContent = element['name'];
                nameDiv.appendChild(nameTextDiv);

                let detailsDiv = document.createElement('div');
                detailsDiv.className = 'attraction-details';
                let detailsMrtDiv = document.createElement('div');
                detailsMrtDiv.className = 'attraction-details-info';
                detailsMrtDiv.textContent = element['mrt'];
                let detailsCatDiv = document.createElement('div');
                detailsCatDiv.className = 'attraction-details-info';
                detailsCatDiv.textContent = element['category'];

                detailsDiv.appendChild(detailsMrtDiv);
                detailsDiv.appendChild(detailsCatDiv);

                attractionDiv.appendChild(img);
                attractionDiv.appendChild(nameDiv);
                attractionDiv.appendChild(detailsDiv);

                linkTag.appendChild(attractionDiv);
                anchorDiv.appendChild(linkTag);
            }
            nextPage = result['nextPage'];
            isLoading = false;
        })
        .catch(err => {
            isLoading = false;
            console.log(err);
        });

};

function loadCategories(callback) {

    return fetch('api/categories')
        .then(res => res.json())
        .then(result => {
            var anchorDiv = document.getElementById('hero-searchbar-dropdown');

            for (let i = 0; i < result['data'].length; i++) {
                let catDiv = document.createElement("div");
                catDiv.className = 'hero-searchbar-dropdown-option';
                catDiv.textContent = result['data'][i];

                catDiv.addEventListener('click', function (event) {
                    document.getElementById('hero-searchbar-keyword').value = catDiv.textContent;
                })

                anchorDiv.appendChild(catDiv);
            }
        })
        .catch(err => console.log(err));
};

window.addEventListener("load", function (event) {
    identifyAuth()
        .then(() => {
            return loadAttractions(nextPage, keyword);
        })
        .then(() => {
            return loadCategories();
        })
});

document.addEventListener('scroll', function (event) {

    if (document.body.scrollHeight <= document.documentElement.scrollTop + window.innerHeight) {

        if (!isLoading) {
            loadAttractions(nextPage, keyword);
        }
    }
});

document.getElementById('hero-searchbar-keyword').addEventListener('click', function (event) {

    let dropdownUl = document.getElementById('hero-searchbar-dropdown');

    if (dropdownUl.getElementsByTagName('div').length !== 0) {
        dropdownUl.style.visibility = "visible";
    }

});


document.getElementById('hero-searchbar-btn').addEventListener('click', function (event) {

    let inputValue = document.getElementById('hero-searchbar-keyword').value;

    if (inputValue === '') {
        return;
    }

    nextPage = 0;
    keyword = inputValue;
    let anchorDiv = document.getElementById('attractions-grp');
    anchorDiv.innerHTML = '';

    loadAttractions(nextPage, keyword);

});

document.addEventListener('click', function (event) {
    let targetId = event.target.id;
    if (targetId !== 'hero-searchbar-keyword' && targetId !== 'hero-searchbar') {
        let dropdownUl = document.getElementById('hero-searchbar-dropdown');
        dropdownUl.style.visibility = "hidden";
    }
});