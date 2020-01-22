displayView = function () {
    // the code required to display a view
    var token = localStorage.getItem("token");
    var loginscreen = document.getElementById('login-screen');
    var profilescreen = document.getElementById('profile-screen');

    //token = "dwa"
    if (serverstub.getUserDataByToken(token).success) {
        profilescreen.style.display = "block";
        loginscreen.style.display = "none";
        localStorage.setItem('selectedTab', 'home')
        selectTab();
    } else {
        loginscreen.style.display = "block";
        profilescreen.style.display = "none";
    }
};


changeText = function (id, text) {
    // text is a string
    document.getElementById(id).innerHTML = text
}

changeColor = function (id, color) {
    // color is a string
    document.getElementById(id).style.color = color
}

checkPasswords = function () {
    var pw1 = document.getElementById("pw");
    var pw2 = document.getElementById("pw-repeat");

    if (pw1.value != pw2.value) {
        pw2.setCustomValidity("Passwords do not match.");
    }
    else {
        pw2.setCustomValidity("");
    }
}

createModal = function () {
    /**
     * Open modal window
     * @param btn Button that was pressed to open the modal. String
     */

    // get the modal
    var modal = document.getElementById("modal-window");

    // Get the <span> element that closes the modal
    var span = document.getElementById("x-btn");
    var close = document.getElementById("close-modal");

    // Show the modal
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks on the close button, close the modal
    close.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

changeModalHeader = function (str) {
    document.getElementById("modal-header-text").innerHTML = str;
}

changeModalText = function (str) {
    document.getElementById("modal-body-text").innerHTML = str;
}

submitLogin = function () {
    var email = document.getElementById("login-email").value;
    var pw = document.getElementById("login-pw").value;
    var result = serverstub.signIn(email, pw);

    if (result.success) {
        localStorage.setItem("token", result.data);
        displayView();
    } else {
        createModal();
        changeModalHeader("Failed");
        changeModalText(result.message);
    }

}

submitSignup = function () {
    var dataObject = {
        email: document.getElementById("email").value,
        password: document.getElementById("pw").value,
        firstname: document.getElementById("first-name").value,
        familyname: document.getElementById("family-name").value,
        city: document.getElementById("city").value,
        country: document.getElementById("country").value,
        gender: document.getElementById("gender").value,
    }

    var result = serverstub.signUp(dataObject);
    createModal();

    if (result.success) {
        changeModalHeader("Success");
        document.getElementById("signup-form").reset();
    } else {
        changeModalHeader("Error");
    }
    changeModalText(result.message)
}

selectTab = function () {
    var tabs = document.getElementsByClassName('tab');

    for (let tab of tabs) {
        tab.style.backgroundColor = "white";
    }

    if (event.type == "click") {
        event.srcElement.style.backgroundColor = "lightsteelblue";
        localStorage.setItem("selectedTab", event.srcElement.id);
    }
    else {
        document.getElementById(localStorage.getItem('selectedTab')).style.backgroundColor = "lightsteelblue"
    }

    window.console.log(localStorage.getItem("selectedTab"))
}

window.onload = function () {
    //code that is executed as the page is loaded.
    //You shall put your own custom code here.

    // load modal window with modal view script html
    var modal = document.getElementById("modal-window");
    modal.innerHTML = document.getElementById("modalview").innerHTML;

    var loginscreen = document.getElementById('login-screen');
    loginscreen.innerHTML = document.getElementById('welcomeview').innerHTML

    var profilescreen = document.getElementById('profile-screen');
    profilescreen.innerHTML = document.getElementById('profileview').innerHTML
    // load login screen with login view script html
    displayView()
    //window.alert() is not allowed to be used in your implementation.
};
