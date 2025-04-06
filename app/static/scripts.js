//the javascript file for if we do anything like animated tabs
//use the following in your html if you want to link it: <script src="{{ url_for('static', filename='script.js') }}"></script>

// Fade tabs on switch
// document.querySelectorAll('button[data-bs-toggle="tab"]').forEach(tab => {
//     tab.addEventListener('shown.bs.tab', function (e) {
//         const tabPane = document.querySelector(e.target.dataset.bsTarget);
//         tabPane.classList.add('fade-in');

//         setTimeout(() => {
//             tabPane.classList.remove('fade-in');
//         }, 500);
//     });
// });

//live drop-down for the autocomplete controller:
document.addEventListener("DOMContentLoaded", function () {
    const speciesInput = document.getElementById("species");
    const speciesSciInput = document.getElementById("species-sci");
    const autocompleteList = document.getElementById("autocomplete-list");

    let currentSuggestions = [];

    speciesInput.addEventListener("input", function () {
        const query = speciesInput.value.trim();
        if (query.length < 2) {
            autocompleteList.innerHTML = "";
            autocompleteList.style.display = "none";
            return;
        }
        //get the autcomplete query
        fetch(`/autocomplete?q=${query}`)
            .then(res => res.json())
            .then(data => {
                //add fetched data to suggestions dropdown
                currentSuggestions = data;
                autocompleteList.innerHTML = "";
                if (data.length === 0) {
                    autocompleteList.style.display = "none";
                    return;
                }
                //label each suggestion so it shows the common and scientific names
                data.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = item.label;
                    li.classList.add("list-group-item");
                    li.addEventListener("click", () => {
                        speciesInput.value = item.label;
                        speciesSciInput.value = item.value;
                        autocompleteList.innerHTML = "";
                        autocompleteList.style.display = "none";
                    });
                    autocompleteList.appendChild(li);
                });
                autocompleteList.style.display = "block";
            });
    });

    //hide list when clicking outside
    document.addEventListener("click", function (e) {
        if (!autocompleteList.contains(e.target) && e.target !== speciesInput) {
            autocompleteList.innerHTML = "";
            autocompleteList.style.display = "none";
        }
    });
});
