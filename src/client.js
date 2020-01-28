displayView = function () {
    // the code required to display a view
    var token = localStorage.getItem("token");
    var loginscreen = document.getElementById('login-screen');
    var profilescreen = document.getElementById('profile-screen');

    if (serverstub.getUserDataByToken(token).success) {
        profilescreen.style.display = "block";
        loginscreen.style.display = "none";
        updateProfileInfo();
        document.getElementById("default-tab").click();
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

checkPasswords = function (pw1, pw2) {
    if (pw1.value != pw2.value) {
        pw2.setCustomValidity("Passwords do not match.");
    }
    else {
        pw2.setCustomValidity("");
    }
}

updateProfileInfo = function () {
    var token = localStorage.getItem("token");
    var data = serverstub.getUserDataByToken(token).data;
    var genderIcon = "<i class='fa fa-venus-mars'></i>"
    var locationIcon = "<i class='fa fa-map-marker'></i>"

    document.getElementById('pi-name').innerHTML = data.firstname + " " + data.familyname;
    document.getElementById('pi-uname').innerHTML = data.email;
    document.getElementById('pi-gender').innerHTML = genderIcon + data.gender;
    document.getElementById('pi-location').innerHTML = locationIcon + data.city + ", " + data.country;

}

createModal = function () {
    /**
     * Open modal window
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

updateWall = function () {
    var token = localStorage.getItem("token");
    var result = serverstub.getUserMessagesByToken(token);
    if (!result.success) {
        createModal();
        changeModalHeader("Error");
        changeModalText(result.message);
    }

    document.getElementById("messages").innerHTML = "";
    var messages = result.data;

    if (messages.length == 0) {
        document.getElementById("messages").innerHTML +=
            "<textarea readonly class='message'/>No tweeds at this moment</textarea>"
    }
    // <textarea readonly class="message"/>Update to show your tweeds</textarea>
    for (let message of messages) {
        document.getElementById("messages").innerHTML +=
            "<textarea readonly class='message'/>" + message.writer.toUpperCase() +
            ":\n\n" + message.content + "</textarea>"
    }

}

tweed = function () {
    var token = localStorage.getItem("token");
    var email = serverstub.getUserDataByToken(token).data.email;
    var message = document.getElementById('tweed-msg').value;

    createModal();
    if (message) {
        var result = serverstub.postMessage(token, message, email);

        if (result.success) {
            changeModalHeader("Success");
            document.getElementById("tweed-form").reset();
        } else {
            changeModalHeader("Error");
        }
        changeModalText(result.message)
    }
    else {
        changeModalHeader("Error");
        changeModalText("You cannot tweed an empty message.");
    }

}

submitLogin = function () {
    var email = document.getElementById("login-email").value;
    var pw = document.getElementById("login-pw").value;
    var result = serverstub.signIn(email, pw);

    if (result.success) {
        localStorage.setItem("token", result.data);
        document.getElementById("login-form").reset();
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

changePassword = function () {
    var token = localStorage.getItem("token");
    var oldPassword = document.getElementById("old-pw").value;
    var newPassword = document.getElementById("new-pw").value;
    var result = serverstub.changePassword(token, oldPassword, newPassword);

    createModal();

    if (result.success) {
        changeModalHeader("Success");
        document.getElementById("pw-form").reset();
    } else {
        changeModalHeader("Error");
    }
    changeModalText(result.message)
}

signOut = function () {
    var token = localStorage.getItem("token");
    serverstub.signOut(token);
    localStorage.removeItem("token");
    displayView();
}

openTab = function (name, elem) {
    // Hide all elements with class="tabcontent" by default.
    var tabs = document.getElementsByClassName("tabcontent");
    for (let tab of tabs) {
        tab.style.display = "none";
    }

    // Remove background color of all tablinks and buttons.
    var tablinks = document.getElementsByClassName("tablink");
    for (let tablink of tablinks) {
        tablink.style.backgroundColor = "";
    }

    // Change title to fit which tab is selected
    document.getElementById('title').innerHTML = name + " / Twidder";

    // Show selected tab content
    document.getElementById(name).style.display = "block";

    // Add color to the button
    elem.style.backgroundColor = "rgb(21, 32, 43)";

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
