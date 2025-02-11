document.addEventListener("DOMContentLoaded", function() {
    const aboutMeButton = document.getElementById("aboutMeButton");

    aboutMeButton.addEventListener("click", function() {
        const pk = this.getAttribute("data-pk"); // get the pk from the button
        const url = "/aboutme/${pk}/"; // forming a URL
        window.location.href = url; // redirect to URL
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('logoutButton').onclick = function () {
        window.location.href = "/accounts/logout/";
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginButton').onclick = function () {
        window.location.href = "/accounts/login/";
    }
});
