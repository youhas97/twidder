displayView = function () {
    // the code required to display a view
    var token = localStorage.getItem("token");
    var loginscreen = document.getElementById('login-screen');
    var profilescreen = document.getElementById('logged-in-screen');

    if (serverstub.getUserDataByToken(token).success) {
        profilescreen.style.display = "block";
        loginscreen.style.display = "none";
        updateProfileInfo();
        updateWall();
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

updateWall = function (email) {
    var token = localStorage.getItem("token");

    if (email) {
        var result = serverstub.getUserMessagesByEmail(token, email);
        if (!result.success) {
            createModal();
            changeModalHeader("Error");
            changeModalText(result.message);
        }
        document.getElementById("browse-messages").innerHTML = "";
        var messages = result.data;

        if (messages.length == 0) {
            document.getElementById("browse-messages").innerHTML +=
                "<textarea readonly class='message'/>No tweeds at this moment</textarea>"
        }
        else {
            for (let message of messages) {
                document.getElementById("browse-messages").innerHTML +=
                    "<textarea readonly class='message'/>" + message.writer.toUpperCase() +
                    ":\n\n" + message.content + "</textarea>"
            }
        }
    }
    else {
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
        else {
            for (let message of messages) {
                document.getElementById("messages").innerHTML +=
                    "<textarea readonly class='message'/>" + message.writer.toUpperCase() +
                    ":\n\n" + message.content + "</textarea>"
            }
        }
    }

}

tweed = function (message, self) {
    var token = localStorage.getItem("token");

    if (self) {
        email = document.getElementById("pi-uname").innerHTML;
    }
    else {
        email = document.getElementById("browse-pi-uname").innerHTML;
    }

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

        updateWall();
    }
    else {
        changeModalHeader("Error");
        changeModalText("You cannot tweed an empty message.");
    }

}

findUser = function () {
    var token = localStorage.getItem("token");
    var email = document.getElementById("find-user").value;
    var result = serverstub.getUserDataByEmail(token, email);


    if (result.success) {
        document.getElementById("user-search-form").reset();

        var view = document.getElementById("Browse");
        view.innerHTML = "";
        view.innerHTML += document.getElementById("browse-std").innerHTML;
        view.innerHTML += document.getElementById("user-info").innerHTML;

        var data = serverstub.getUserDataByEmail(token, email).data;
        var genderIcon = "<i class='fa fa-venus-mars'></i>"
        var locationIcon = "<i class='fa fa-map-marker'></i>"

        document.getElementById('browse-pi-name').innerHTML = data.firstname + " " + data.familyname;
        document.getElementById('browse-pi-uname').innerHTML = email;
        document.getElementById('browse-pi-gender').innerHTML = genderIcon + data.gender;
        document.getElementById('browse-pi-location').innerHTML = locationIcon + data.city + ", " + data.country;
        document.getElementById('browse-profile-header').innerHTML = data.firstname + "'s Profile"

        updateWall(email);
    }
    else {
        createModal();
        changeModalHeader("Error");
        changeModalText(result.message)
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

    // load different views using html inside of script tag
    var loginscreen = document.getElementById('login-screen');
    loginscreen.innerHTML = document.getElementById('welcomeview').innerHTML;

    var profilescreen = document.getElementById('logged-in-screen');
    profilescreen.innerHTML = document.getElementById('logged-in').innerHTML;

    var browsescreen = document.getElementById('Browse');
    browsescreen.innerHTML = document.getElementById('browse-std').innerHTML;
    displayView()
    //window.alert() is not allowed to be used in your implementation.
};
