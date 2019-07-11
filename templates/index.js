 // index page | get a user's name input and store it in localStorage
 document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#form").onsubmit = () => {
        const name = document.querySelector("#name").value;
        // save name variable to localStorage
        localStorage.setItem('name', name);
    };
});
