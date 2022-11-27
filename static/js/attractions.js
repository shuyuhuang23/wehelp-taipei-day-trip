var isLoading = false;
var nextPage = 0;
var keyword = '';

function loadData(page, keyword) {
    console.log(nextPage);

    if (nextPage === null) {

        return;

    }
    let url = `api/attractions?page=${nextPage}`
    if (keyword !== ''){
        url = `${url}&keyword=${keyword}`
    }

    fetch(url)
        .then(res => res.json())
        .then(result => {
            
            var anchorDiv = document.getElementById('attractions-grp');
            
            if (nextPage === 0 && result['data'].length === 0) {
                anchorDiv.textContent = '查無景點';
            }
            
            for (let i = 0; i < result['data'].length; i++) {
                let element = result['data'][i];

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

                anchorDiv.appendChild(attractionDiv);
            }
            nextPage = result['nextPage'];
            isLoading = false;
        })
        .catch(err => console.log(err));
}

window.addEventListener("load", loadData(nextPage, keyword));
  
document.addEventListener('scroll', function (event) {

    if (document.body.scrollHeight <= document.documentElement.scrollTop + window.innerHeight) {

        if (!isLoading) {
            console.log('bottom')
            loadData(nextPage, keyword);
        }
    }
});

document.getElementById('hero-searchbar-btn').addEventListener('click', function(event) {
    
    let inputValue = document.getElementById('hero-searchbar-keyword').value;
    
    if (inputValue === '') {

        return;

    }

    nextPage = 0;
    keyword = inputValue;
    let anchorDiv = document.getElementById('attractions-grp');
    anchorDiv.innerHTML = '';

    loadData(nextPage, keyword);
    
});

// console.log(123)


// class Attraction extends React.Component {
//     render() {
//         return <div class="attraction">
//             <img src="https:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/pic\/11002891.jpg"/>
//                 <div class="attraction-name">
//                     <div>this.props.name</div>
//                 </div>
//                 <div class="attraction-details">
//                     <div class="attraction-details-info">this.props.mrt</div>
//                     <div class="attraction-details-info">{this.props.category}</div>
//                 </div>
//         </div>

//     }
// }



// if (document.readyState === "complete") {
//     console.log(document.getElementById('attractions-grp'));
//         // ReactDOM.render(<Attraction/>, document.getElementById("attractions-grp"));
//   } else {
//     // window.addEventListener('load', handler);
//     // return () => document.removeEventListener('load', handler);

//     window.addEventListener("load", () => {
//         // ReactDOM.render(<Switch />, document.body);
        

//         fetch('api/attractions?page=0')
//         .then(res => res.json())
//         .then(result => {

//             // console.log(result);
//             let anchorDiv = document.getElementById('attractions-grp');

//             // console.log(anchorDiv)
//         })
//         .catch(err => console.log(err));
//         console.log(document.getElementById('attractions-grp'));
//         ReactDOM.render(<Attraction/>, document.getElementById("attractions-grp"));
//         // ReactDOM.render(<Switch/>, document.getElementById("switch-1"));
//     })
//   }


// class Switch extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = { on: false };
//     }
//     render() {
//         let className = "switch";
//         if (this.state.on) {
//             className += " switch-on";
//         }
//         return <div onClick={this.update.bind(this)} className={className}>
//             <div className="btn"></div>
//         </div>
//     }
//     update() {
//         this.setState((currentState) => ({ on: !currentState.on }));
//     }
// }
// window.addEventListener("load", () => {
//     // ReactDOM.render(<Switch />, document.body);
//     ReactDOM.render(<Switch/>, document.getElementById("switch-0"));
//     ReactDOM.render(<Switch/>, document.getElementById("switch-1"));
// })
