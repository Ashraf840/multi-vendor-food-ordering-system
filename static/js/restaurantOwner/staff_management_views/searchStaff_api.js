// Search functionality for the staff-list & staff-pending-list


// Axios will be used in both method. Thus the frontend HTML will be using the 
// If searched by using the 'searchField', then make the query & result currently.
// If the 'searchIcon' icon is created, then use the POST method im the axios.



// ---------------------------------------- NB
// Before using axios, we need to import the axios-script from the cloud. Using "cdnjs" for referencing the axios-library.
// The axios-script should be better to be referenced inside the "foodsystem/templates/base_restaurant_owner.html" file. Thus we can make axios calls in any separate files without bothering about referencing to every individual HTML page which is extending the "foodsystem/templates/base_restaurant_owner.html" file.
// ---------------------------------------- NB



// [ Assing DOM Tags into JS variable ]
// Took the 'searchField' input-field from HTML page to JS-script.
const searchField = document.getElementById('searchField');
const searchBtn_holder = document.getElementById('searchIcon_holder');

// Staff-table HTML tags
const tableDefualt = document.getElementById('tableDefualt');
const tableSearchOutput = document.getElementById('tableSearchOutput');
const tableSearchOutputBody = document.getElementById('tableSearchOutputBody');



// [ Global Variables ]
let searchValue;  // Global var of search-field-input
let staff_search_url = 'http://127.0.0.1:8080/restaurant-owner/staff_search/';
let rest_id = restaurant_id   // ********'restaurant_id' is got from the js-script of 'base_restaurant_owner.html' file. It's a base template inside the both ("restaurantOwner\staff_list.html" & "restaurantOwner\staff_list_pending.html") file.




// Fetch the user of this pages session. Store the django-template-variable into a JS variable.
// Got the "restaurant_id" from the js-script of "foodsystem/templates/base_restaurant_owner.html", 
// cause the "restaurant_id" is thrown from the backend view "search_staff" to the "base_restaurant_owner.html" file, 
// which is then stored as JS-objetc from the django-template-variable, lastly the JS-objct-var is achieved cause 
// this JS-script-file ("searchStaff_api.js") is also exist along with the base-template's script. the base-restaurant-owner template 
// is extended inside the both "staff_list_pending.html" & "staff_list.html".


// console.log(restaurant_id);

function axiosPost(url, searchVal, res_id) {
    axios.post(
        // Hit the search-staff endpoint
        url,
        // '../staff_search/',
        // pass the 'searchField' value to the backend view "search_staff", along with the "restaunrant_id"
        {
            'searchValue':searchVal,
            'restaurant_id':res_id,
        }
    )
    .then(res => {
        // res = res.data.searchFieldVal
        // res = res.dict_data.searchValue
        console.log(res);
        // console.log(res.data.searchFieldVal);
        // console.log(res.dict_data.restaurant_id);

        // ******************************
        // Make HTML-table manipulation code here

        // [ DOM Manipulation ]
        // Clear the 'tableSearchOutput' table's data-row.
        tableSearchOutputBody.innerHTML = "";
        // One something is searched, hide the default staff-table & display the 'tableSearchOutput' table.
        tableDefualt.style.display = "none";
        tableSearchOutput.style.display = "block";





        // [ PROBLEM ]: <td> is being rendered as double in quntity.
        if (res.data.length !== 0) {
            // tableSearchOutputBody.innerHTML = ``;
            res.data.forEach((item) => {
                tableSearchOutputBody.innerHTML += `
                    <tr scope="row">
                        <td>${item.id}<td/>
                        <td>${item.first_name + ' ' + item.last_name}<td/>
                        <td>${item.phone}<td/>
                        <td>${item.email}<td/>
                        <td>${item.gender}<td/>
                        <td>${item.is_approved}<td/>
                    </tr>`;
            });
        }else{
            tableSearchOutputBody.innerHTML = "<tr> <td style='font-weight: bold; text-align:center'> No Result Found! <td/> <tr/>";
        }
        // ******************************
    })
    .catch(errors => {
        console.log(errors);
    });
}




// // [ Search-field function ]
// Keyup Listener: when the user presses a key & put the fingers up while inside the search-box, 
// the event-listener will work then.
searchField.addEventListener('keyup', (e) => {
    searchValue = e.target.value;
    // console.log(searchValue);   // View the typing test

    searchField.innerHTML = searchValue;  // Display the text which is typed inside the 'searchField'.

    // Check if the Staff-Search-Field is not empty
    if (searchValue.length > 0) {
        // Clear the search-field first
        // searchField.innerHTML = "";

        // [ AXIOS.POST request ]
        // Use the "axios.POST" to send the searchField data to the backend view ("search_staff") inside the "restaurantOwner/views/staff_management_views/staff_recruit_remove_views.py" file.
        // Using the endpoint of "staff_search/" inside the "foodsystem/restaurantOwner/urls.py" file.
        // staff_search_url = 'http://127.0.0.1:8080/restaurant-owner/staff_search/'
        searchField_value = searchValue;


        // Call the func to make axios-post-req
        axiosPost(url=staff_search_url, 
                searchVal=searchField_value, 
                res_id=rest_id);
    }else{
        tableDefualt.style.display = "block";
        tableSearchOutput.style.display = "none";
    }
});






// [ Search-button function ]
searchBtn_holder.addEventListener('click', (e) => {
    // alert('Hellow');
    // alert(searchValue);

    try {
        // Check if the "searchValue" has a value
        if (searchValue) {
            axiosPost(url=staff_search_url, 
                searchVal=searchField_value, 
                res_id=rest_id)
    
        }else {
            alert('Empty search-box!')
        }
    } catch (error) {
        alert(error);
    }
});